import requests
import os
import psycopg2

def fetch_and_store(symbol='IBM'):
    """
    Fetches daily stock data from Alpha Vantage API, parses JSON, and upserts into PostgreSQL.
    Handles errors and missing data gracefully.
    """

    api_key=os.getenv("API_KEY")
    if not api_key:
        raise ValueError("API_KEY environment variable is not set.")
    
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}&outputsize=compact"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise Exception(f"API request failed: {e}")

    try:
        data = response.json()
        time_series = data.get('Time Series (Daily)')
        if not time_series:
            raise ValueError("No 'Time Series (Daily)' in API response or invalid data.")
    except ValueError as e:
        raise Exception(f"JSON parsing failed: {e}")
    
    db_host = os.getenv('DB_HOST', 'postgres')
    db_name = os.getenv('DB_NAME', 'airflow')
    db_user = os.getenv('DB_USER', 'airflow')
    db_pass = os.getenv('DB_PASS', 'airflow')

    conn = None
    try:
        conn = psycopg2.connect(
            host=db_host,
            database=db_name,
            user=db_user,
            password=db_pass
        )
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS stock_data (
                symbol VARCHAR(10),
                date DATE,
                open NUMERIC,
                high NUMERIC,
                low NUMERIC,
                close NUMERIC,
                volume BIGINT,
                PRIMARY KEY (symbol, date)
            )
        """)
        conn.commit()

        inserted_count = 0
        for date_str, values in time_series.items():
            try:
                required_keys = ['1. open', '2. high', '3. low', '4. close', '5. volume']
                if any(key not in values for key in required_keys):
                    print(f"Skipping {date_str} due to missing data.")
                    continue

                cur.execute("""
                    INSERT INTO stock_data (symbol, date, open, high, low, close, volume)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (symbol, date) DO UPDATE SET
                        open = EXCLUDED.open,
                        high = EXCLUDED.high,
                        low = EXCLUDED.low,
                        close = EXCLUDED.close,
                        volume = EXCLUDED.volume
                """, (
                    symbol,
                    date_str,
                    float(values['1. open']),
                    float(values['2. high']),
                    float(values['3. low']),
                    float(values['4. close']),
                    int(values['5. volume'])
                ))
                conn.commit()
                inserted_count += 1
            except (KeyError, ValueError) as e:
                conn.rollback()
                print(f"Data error for {date_str}: {e}. Skipping.")
            except Exception as e:
                conn.rollback()
                raise Exception(f"Database insert failed for {date_str}: {e}")

        print(f"Successfully processed {inserted_count} data points.")
    except psycopg2.Error as e:
        raise Exception(f"Database connection/error: {e}")
    finally:
        if conn:
            conn.close()

# Stock Data Pipeline with Apache Airflow 🗠

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Docker](https://img.shields.io/badge/Docker-Compose-blue)
![Airflow](https://img.shields.io/badge/Apache%20Airflow-2.10.0-orange)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

A **Dockerized data pipeline** built with Apache Airflow to automate fetching, processing, and storing daily stock market data from the Alpha Vantage API into a PostgreSQL database. This project demonstrates a robust ETL (Extract-Transform-Load) workflow with scheduled execution, error handling, and containerized deployment.

## 📋 Project Overview

This pipeline:
- **Fetches** daily stock data (open, high, low, close, volume) for a stock (e.g., IBM) from the Alpha Vantage API.
- **Processes** JSON data, handling missing or invalid entries gracefully.
- **Stores** data in a PostgreSQL table using upsert to avoid duplicates.
- **Schedules** runs daily via Airflow's scheduler.
- **Dockerizes** the entire setup (Airflow + PostgreSQL) for easy deployment.
- **Secures** sensitive info (API keys, DB credentials) with environment variables.

Built using Airflow's SequentialExecutor for ease of use and comprehensive error handling for reliability.

## 🛠️ Technologies Used
- **Apache Airflow**: Orchestrates the ETL pipeline with scheduled DAGs.
- **Docker & Docker Compose**: Containerizes Airflow and PostgreSQL for portability.
- **PostgreSQL**: Stores stock data and Airflow metadata.
- **Python**: Implements data fetching (`requests`) and database operations (`psycopg2`).
- **Alpha Vantage API**: Provides free stock market data.

## 📂 Project Structure
```
stock-data-pipeline/
├── docker-compose.yml     # Defines Docker services (Airflow, PostgreSQL)
├── dags/
│   ├── fetch_stock.py     # Python script for fetching and storing data
│   └── stock_dag.py       # Airflow DAG definition for scheduling
├── .gitignore             # Ignores sensitive/temporary files
└── README.md              # Project documentation
```

## 🚀 Getting Started

### Prerequisites
- Docker and Docker Compose installed ([Docker Desktop](https://www.docker.com/products/docker-desktop)).
- A free [Alpha Vantage API key](https://www.alphavantage.co/support/#api-key).

### Setup Instructions
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/SABARNO-PRAMANICK/Airflow-Stock-Vantage-Pipeline.git
   cd stock-data-pipeline
   ```

2. **Create a `.env` File**:
   In the project root, create a `.env` file with your API key and user ID:
   ```bash
   echo "API_KEY=your_alpha_vantage_api_key" > .env
   echo "AIRFLOW_UID=$(id -u)" >> .env
   ```
   - Replace `your_alpha_vantage_api_key` with your key from Alpha Vantage.
   - `AIRFLOW_UID` aligns file permissions (optional on Mac/Windows, run `id -u` to get your user ID).

3. **Start the Pipeline**:
   ```bash
   docker compose up -d
   ```
   This spins up Airflow (webserver, scheduler, init) and PostgreSQL containers.

4. **Access Airflow UI**:
   - Open [http://localhost:8080](http://localhost:8080) in your browser.
   - Login: Username `airflow`, Password `airflow`.
   - Enable the `stock_pipeline` DAG and trigger it manually or wait for the daily schedule.

5. **Verify Data**:
   Check stored stock data in PostgreSQL:
   ```bash
   docker compose exec postgres psql -U airflow -d airflow -c "SELECT * FROM stock_data LIMIT 5;"
   ```

6. **Stop the Pipeline**:
   ```bash
   docker compose down
   ```
   To clear data: `docker compose down -v`.

## 🔧 Customization
- **Change Stock Symbol**: Edit `dags/stock_dag.py`, update `op_kwargs={'symbol': 'YOUR_SYMBOL'}` (e.g., 'AAPL' for Apple).
- **Adjust Schedule**: Modify `schedule_interval` in `dags/stock_dag.py` (e.g., `'@hourly'`).
- **Error Handling**: The pipeline skips missing data points and retries API failures (3 attempts, 5-minute delay).

## 🛡️ Features
- **Robust Error Handling**: Skips invalid data, retries on API failures, logs issues.
- **Scalability**: Uses Airflow's DAG for easy task expansion; can switch to CeleryExecutor for parallel processing.
- **Security**: Stores API key and DB credentials in `.env`.
- **Portability**: Fully Dockerized for consistent deployment across environments.
- **Data Integrity**: Upserts prevent duplicate entries in the database.

## 📊 Example Data
The pipeline processes JSON from Alpha Vantage, storing fields like:
- Symbol: IBM
- Date: 2025-08-14
- Open: 238.2500
- High: 239.0000
- Low: 235.6200
- Close: 237.1100
- Volume: 4556725


## 📝 Notes
- Alpha Vantage free tier has rate limits (5 calls/min, 500/day). Monitor usage for production.
- For production, consider adding monitoring (e.g., Airflow alerts) or scaling with CeleryExecutor.
- See [Airflow Docs](https://airflow.apache.org/docs/apache-airflow/stable/) for advanced configuration.

---

⭐ If you find this project useful, give it a star on GitHub!  
For questions or contributions, open an issue or reach out via [sabarnopramanick@gmail.com].
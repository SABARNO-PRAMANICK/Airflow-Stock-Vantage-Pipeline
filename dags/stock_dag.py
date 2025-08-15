from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from fetch_stock import fetch_and_store

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 8, 15),
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'stock_pipeline',
    default_args=default_args,
    description='Daily stock data pipeline',
    schedule_interval='@daily',
    catchup=False,
)

fetch_task = PythonOperator(
    task_id='fetch_and_store_stock_data',
    python_callable=fetch_and_store,
    op_kwargs={'symbol': 'IBM'},
    dag=dag,
)

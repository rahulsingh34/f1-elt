from airflow import DAG
from datetime import datetime
from airflow.operators.python_operator import PythonOperator

default_args = {
    'owner': 'rahul',
    'depends_on_past': False,
    'start_date': datetime(2024, 6, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1
}

# Tasks
def get_data():
    # Task logic
    pass

def push_to_staging():
    # Task logic
    pass

# DAG
with DAG(
    'load_from_s3',
    default_args=default_args,
    description='Load data from S3 to staging tables',
    schedule_interval=None,
    catchup=False,
) as dag:
    
    get_data = PythonOperator(
        task_id='get_data',
        python_callable=get_data,
    )

    push_to_staging = PythonOperator(
        task_id='push_to_staging',
        python_callable=push_to_staging,
    )
    
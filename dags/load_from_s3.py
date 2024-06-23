from airflow import DAG
from datetime import datetime
from airflow.operators.python import PythonOperator
from airflow.hooks.S3_hook import S3Hook
import pandas as pd

# Variables
BUCKET = 'f1-source'
AWS_CONN_ID = 'aws_default'
POSTGRES_CONN_ID = 'postgres_localhost'

# Defaults
default_args = {
    'owner': 'rahul',
    'depends_on_past': False,
    'start_date': datetime(2024, 6, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1
}

# List files in bucket
def list_files_in_s3():
    hook = S3Hook(aws_conn_id=AWS_CONN_ID)
    keys = hook.list_keys(bucket_name=BUCKET)
    return keys

# Process and push CSVs to Postgres
def push_to_postgres(**kwargs):
    # Get the list of files from previous task
    ti = kwargs['ti']
    keys = ti.xcom_pull(task_ids='list_files_in_s3')

    # AWS Connection
    hook = S3Hook(aws_conn_id=AWS_CONN_ID)

    # Iterate over the files
    for key in keys:
        # Download the file
        file = hook.download_file(bucket_name=BUCKET, key=key, preserve_file_name=True)

        # INP: Load CSV to Postgres
        df = pd.read_csv(file)
        #df.to_sql(name=key, con=POSTGRES_CONN_ID, if_exists='replace', index=False)

# DAG
with DAG(
    dag_id='load_from_s3',
    default_args=default_args,
    description='Load data from S3 to staging tables',
    schedule_interval=None,
    catchup=False,
) as dag:

    list_files_in_s3 = PythonOperator(
        task_id='list_files_in_s3',
        python_callable=list_files_in_s3,
        provide_context=True
    )

    push_to_postgres = PythonOperator(
        task_id='process_files',
        python_callable=push_to_postgres,
        provide_context=True
    )

    list_files_in_s3 >> push_to_postgres
FROM apache/airflow:2.9.2

USER airflow

RUN pip install dbt-core dbt-postgres
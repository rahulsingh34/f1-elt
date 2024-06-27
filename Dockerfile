FROM apache/airflow:2.9.2

USER root

RUN pip install dbt-core dbt-postgres

USER airflow
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from datetime import datetime

dag = DAG(
    'dag_postgres',
    description = "Dag Postgres",
    schedule_interval=None,
    start_date=datetime(2023,9,3),
    catchup=False,
    default_view='graph',
    tags=['Database']
)

def print_result(**kwargs):
    task_instance = kwargs['ti'].xcom_pull(task_ids='query_data')
    print("Resultado da consulta:")
    for row in task_instance:
        print(row)

create_table = PostgresOperator(task_id='create_table', postgres_conn_id='postgres',sql='create table if not exists teste(id int);',dag=dag)

insert_data = PostgresOperator(task_id='insert_data',postgres_conn_id='postgres',sql='insert into teste values(1);',dag=dag)

query_data = PostgresOperator(task_id='query_data',postgres_conn_id='postgres',sql='select * from teste;',dag=dag)

print_result_task = PythonOperator(task_id='result_query',python_callable=print_result,provide_context=True,dag=dag)

create_table >> insert_data >> query_data >> print_result_task
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime

dag = DAG(
    'dag_postgres_hooks',
    description = "Dag Postgres Hooks",
    schedule_interval=None,
    start_date=datetime(2023,9,3),
    catchup=False,
    default_view='graph',
    tags=['Database']
)

def create_table():
    PostgresHook(postgres_conn_id='postgres').run('create table if not exists teste2(id int);', autocommit=True)

def insert_data():
    PostgresHook(postgres_conn_id='postgres').run('insert into teste2 values(1);',autocommit=True)

def select_data(**kwargs):
    records = PostgresHook(postgres_conn_id='postgres').get_records('select * from teste2;')
    kwargs['ti'].xcom_push(key='query_result',value=records)

def print_result(**kwargs):
    task_instance = kwargs['ti'].xcom_pull(key='query_result', task_ids='select_postgres')
    print("Resultado da consulta:")
    for row in task_instance:
        print(row)


create_postgres = PythonOperator(task_id='create_postgres',python_callable= create_table,dag=dag)
insert_postgres = PythonOperator(task_id='insert_postgres',python_callable= insert_data,dag=dag)
select_postgres = PythonOperator(task_id='select_postgres',python_callable= select_data,dag=dag)
print_postgres = PythonOperator(task_id='print_postgres',python_callable= print_result,provide_context=True,dag=dag)

create_postgres >> insert_postgres >> select_postgres >> print_postgres
# Limpeza simples de dados utilizando o operator PythonOperator

from airflow import DAG, Dataset
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
import pandas as pd

dag = DAG(
    'dag_producer',
    description = "Dag producer",
    schedule_interval=None,
    start_date=datetime(2023,9,2),
    catchup=False,
    default_view='graph',
    tags=['Producer']
)

MyDataset = Dataset('/opt/airflow//data/Churn_new.csv')

def my_file():
    dataset = pd.read_csv("/opt/airflow//data/Churn.csv", sep=";")
    dataset.to_csv("/opt/airflow//data/Churn_new.csv", sep=";")


task1 = PythonOperator(task_id='task1', python_callable=my_file, dag=dag, outlets=[MyDataset])

task1
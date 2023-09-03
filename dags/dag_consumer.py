# Limpeza simples de dados utilizando o operator PythonOperator

from airflow import DAG, Dataset
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
import pandas as pd

MyDataset = Dataset('/opt/airflow//data/Churn_new.csv')

dag = DAG(
    'dag_consumer',
    description = "Dag consumer",
    schedule=[MyDataset],
    start_date=datetime(2023,9,2),
    catchup=False,
    default_view='graph',
    tags=['Consumer']
)

def my_file():
    dataset = pd.read_csv("/opt/airflow//data/Churn_new.csv", sep=";")
    dataset.to_csv("/opt/airflow//data/Churn_new_2.csv", sep=";")

task1 = PythonOperator(task_id='task1', python_callable=my_file, dag=dag, provide_context=True)

task1
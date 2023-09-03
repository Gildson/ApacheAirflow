# Limpeza simples de dados utilizando o operator PythonOperator

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
import random
import pandas as pd
import statistics as sts

dag = DAG(
    'dag_data_cleaner',
    description = "Dag data cleaner",
    schedule_interval=None,
    start_date=datetime(2023,9,2),
    catchup=False,
    default_view='graph',
    tags=['Datacleaner']
)

def data_cleaner():
    dataset = pd.read_csv('/opt/airflow//data/Churn.csv', sep=";")
    dataset.columns = ['id','Score','Estado','Genero','Idade','Patrimonio','Saldo','Produtos','TemCartCredito','Ativo','Salario','Saiu']

    mediana_salarios = sts.median(dataset['Salario'])

    dataset['Salario'].fillna(mediana_salarios,inplace=True)

    dataset['Genero'].fillna('Masculino',inplace=True)

    mediana_idade = sts.median(dataset['Idade'])

    dataset.loc[(dataset['Idade'] < 0) | (dataset['Idade'] > 120), 'Idade'] = mediana_idade

    dataset.drop_duplicates(subset='id',keep='first', inplace=True)

    dataset.to_csv('/opt/airflow/data/ChurnCleaner.csv', sep=";", index=False)

datacleaner = PythonOperator(task_id='datacleaner', python_callable=data_cleaner, dag=dag)

datacleaner
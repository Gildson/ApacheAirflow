# Escolha de caminho com branch

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator, BranchPythonOperator
from datetime import datetime
import random

dag = DAG(
    'dag_branchs',
    description = "Dag branchs",
    schedule_interval=None,
    start_date=datetime(2023,9,2),
    catchup=False,
    default_view='graph',
    tags=['processo','tags','pipeline']
)

def function_num_random():
    return random.randint(1,100)

num_random = PythonOperator(task_id='num_random', python_callable=function_num_random, dag=dag)

def check_num_random(**kwargs):
    num = kwargs['task_instance'].xcom_pull(task_ids='num_random')
    if num % 2 == 0:
        return 'par_task'
    else:
        return  'impar_task'

branch_task = BranchPythonOperator(task_id='branch_task',python_callable=check_num_random,provide_context=True, dag=dag)

par_task = BashOperator(task_id='par_task', bash_command='echo "Número par"', dag=dag)
impar_task = BashOperator(task_id='impar_task', bash_command='echo "Número impar"', dag=dag)

num_random >> branch_task
branch_task >> par_task
branch_task >> impar_task

# Gerenciamento de recusos com pool

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime

dag = DAG(
    'dag_pools',
    description = "Dag pools",
    schedule_interval=None,
    start_date=datetime(2023,9,2),
    catchup=False
)


task1 = BashOperator(task_id='task1', bash_command='sleep 1', dag=dag, pool='MyPool')
task2 = BashOperator(task_id='task2', bash_command='sleep 1', dag=dag, pool='MyPool', priority_weight=5)
task3 = BashOperator(task_id='task3', bash_command='sleep 1', dag=dag, pool='MyPool')
task4 = BashOperator(task_id='task4', bash_command='sleep 1', dag=dag, pool='MyPool', priority_weight=10)


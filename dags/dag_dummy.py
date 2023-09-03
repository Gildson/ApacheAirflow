# Dummy

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator
from datetime import datetime

dag = DAG(
    'dag_dummy',
    description = "Dag Dummy",
    schedule_interval=None,
    start_date=datetime(2023,9,2),
    catchup=False
)

task1 = BashOperator(task_id='task1', bash_command='sleep 1', dag=dag)
task2 = BashOperator(task_id='task2', bash_command='sleep 1', dag=dag)
task3 = BashOperator(task_id='task3', bash_command='sleep 1', dag=dag)

dummy = DummyOperator(task_id='dummy', dag=dag)

task4 = BashOperator(task_id='task4', bash_command='sleep 1', dag=dag)
task5 = BashOperator(task_id='task5', bash_command='sleep 1', dag=dag)

[task1,task2,task3] >> dummy >> [task4,task5]
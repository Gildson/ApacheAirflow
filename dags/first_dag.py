from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime


dag = DAG(
    'first_dag',
    description = "My first dag",
    schedule_interval=None,
    start_date=datetime(2023,9,1),
    catchup=False
)

task1 = BashOperator(
    task_id='task1',
    bash_command='sleep 5',
    dag=dag
)


task2 = BashOperator(
    task_id='task2',
    bash_command='sleep 5',
    dag=dag
)


task3 = BashOperator(
    task_id='task3',
    bash_command='sleep 5',
    dag=dag
)


task1 >> task2 >> task3
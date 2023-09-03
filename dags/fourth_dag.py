#Outra maneira para executar a ordem de execução(procedência)

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime


with DAG(
    'fourth_dag',
    description = "My fourth dag",
    schedule_interval=None,
    start_date=datetime(2023,9,1),
    catchup=False ) as dag:

    task1 = BashOperator(
        task_id='task1',
        bash_command='sleep 5'
    )


    task2 = BashOperator(
        task_id='task2',
        bash_command='sleep 5'
    )


    task3 = BashOperator(
        task_id='task3',
        bash_command='sleep 5'
    )


task1.set_upstream(task2)
task2.set_upstream(task3)
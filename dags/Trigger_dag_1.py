from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime


dag = DAG(
    'trigger_dag_1',
    description = "My frist trigger dag",
    schedule_interval=None,
    start_date=datetime(2023,9,2),
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
    dag=dag,
    trigger_rule = 'one_failed'
)


[task1,task2] >> task3
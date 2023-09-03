#Criar fluxo de execução mais complexo

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime


dag = DAG(
    'dag_trigger_operator_2',
    description = "Dag trigger operator 2",
    schedule_interval=None,
    start_date=datetime(2023,9,2),
    catchup=False
)

task1 = BashOperator(task_id='task1', bash_command='sleep 5', dag=dag)
task2 = BashOperator(task_id='task2', bash_command='sleep 5', dag=dag)

task1 >> task2

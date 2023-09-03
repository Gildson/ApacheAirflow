# Envio de emails

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.email_operator import EmailOperator
from datetime import datetime, timedelta

default_args = {
    'depends_on_past': False,
    'start_date': datetime(2023, 9, 2),
    'email':['gildson.santos@inovall.com.br'], #Email referente a avisos do sistema
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(seconds=10)
}

dag = DAG(
    'dag_send_email',
    description = "Dag send email",
    default_args = default_args,
    catchup=False,
    default_view='graph',
    tags=['processo','tags','pipeline']
)

task1 = BashOperator(task_id='task1', bash_command='sleep 1', dag=dag)
task2 = BashOperator(task_id='task2', bash_command='sleep 1', dag=dag)
task3 = BashOperator(task_id='task3', bash_command='sleep 1', dag=dag)
task4 = BashOperator(task_id='task4', bash_command='exit 1', dag=dag)

SendEmail = EmailOperator(task_id='Send_Email',
                          to='gildson.santos@inovall.com.br',
                          subject='Airflow Error',
                          html_content="""<h3>Ocorreu um erro na Dag. </h3>
                                        <p>Dag: Send_email</p>""",
                          dag=dag,
                          trigger_rule='one_failed')

task5 = BashOperator(task_id='task5', bash_command='sleep 1', dag=dag, trigger_rule='none_failed')
task6 = BashOperator(task_id='task6', bash_command='sleep 1', dag=dag, trigger_rule='none_failed')

[task1,task2] >> task3 >> task4
task4 >> [SendEmail,task5,task6]

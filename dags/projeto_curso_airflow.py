from airflow import DAG
from airflow.operators.python_operator import PythonOperator, BranchPythonOperator
from airflow.operators.email_operator import EmailOperator
from airflow.sensors.filesystem import FileSensor
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.models import Variable  #Utilização de variáveis definidas no airflow
from airflow.utils.task_group import TaskGroup
from datetime import datetime, timedelta
import json
import os

default_args = {
    'depends_on_past':False,
    'email':['gildson.santos@inovall.com.br'],
    'email_on_failure':True,
    'email_on_retry':False,
    'retries':1,
    'retry_delay':timedelta(seconds=10)
}

dag = DAG('dag_windturbine',description='dados da turbina',
          schedule_interval=None, start_date=datetime(2023,9,3), catchup=False, default_args=default_args,default_view='graph',
          doc_md="## Dag para registrar dados de turbina eólica")


#Grupos para junta as etapas do script, parecido com um classe python
group_check_temp = TaskGroup("group_check_temp", dag=dag)
group_database = TaskGroup("group_database",dag=dag)

#Monitorar o arquivo que está no caminho guardado dentro da variável criada no airflow
#O monitoramento é feito a cada 10 segundos
file_sensor_task = FileSensor(task_id='file_sensor_task',
                              filepath=Variable.get('path_file'),
                              fs_conn_id='fs_default',
                              poke_interval=10,
                              dag=dag)

#Pegar os valores das leituras
def process_file(**kwargs):
    with open(Variable.get('path_file')) as f:
        data = json.load(f)
        kwargs['ti'].xcom_push(key='idtemp',value=data['idtemp'])
        kwargs['ti'].xcom_push(key='powerfactor',value=data['powerfactor'])
        kwargs['ti'].xcom_push(key='hydraulicpressure',value=data['hydraulicpressure'])
        kwargs['ti'].xcom_push(key='temperature',value=data['temperature'])
        kwargs['ti'].xcom_push(key='timestamp',value=data['timestamp'])
        os.remove(Variable.get('path_file'))

get_data = PythonOperator(task_id='get_data', #função que gera os valores dos xcom
                          python_callable=process_file,
                          provide_context=True, #Para ler os valores do xcom
                          dag=dag)

#Tarefas
create_table = PostgresOperator(task_id='create_table',
                                postgres_conn_id='postgres',
                                sql='''create table if not exists sensors (idtemp varchar, 
                                powerfactor varchar, hydraulicpressure varchar, temperature varchar, timestamp varchar);''',
                                task_group=group_database,
                                dag=dag)

insert_data = PostgresOperator(task_id='insert_data',
                               postgres_conn_id='postgres',
                               #Expressão ginja
                               parameters=(
                                   '{{ti.xcom_pull(task_ids="get_data",key="idtemp")}}',
                                   '{{ti.xcom_pull(task_ids="get_data",key="powerfactor")}}',
                                   '{{ti.xcom_pull(task_ids="get_data",key="hydraulicpressure")}}',
                                   '{{ti.xcom_pull(task_ids="get_data",key="temperature")}}',
                                   '{{ti.xcom_pull(task_ids="get_data",key="timestamp")}}',
                               ),
                               sql='''insert into sensors (idtemp, powerfactor, hydraulicpressure, temperature, timestamp)
                               values (%s, %s, %s, %s, %s);''',
                               task_group=group_database,
                               dag=dag)

#Envio de email
#Tarefas
send_email_alert = EmailOperator(task_id='email_alert',
                                 to='gildson.santos@inovall.com.br',
                                 subject='Airflow alert',
                                 html_content='''
                                <h3>Alerta de temperatura. </h3>
                                <p>Dag: dag_windturbine</p>''',
                                task_group=group_check_temp,
                                dag=dag)

send_email_normal = EmailOperator(task_id='email_normal',
                                 to='gildson.santos@inovall.com.br',
                                 subject='Airflow advise',
                                 html_content='''
                                <h3>Temperaturas normais. </h3>
                                <p>Dag: dag_windturbine</p>''',
                                task_group=group_check_temp,
                                dag=dag)

#Decisão de qual email enviar
def avalia_temp(**kwargs):
    number = float(kwargs['ti'].xcom_pull(task_ids='get_data', #função que geras os valores para o xcom
                                    key='temperature'))
    if number >= 24:
        return 'group_check_temp.email_alert' #chama a tarefa que criamos a ação desejada (chama pelo task_id)
                                                #Como as tarefas estão dentro do um group, utilizamos a mesmo sintaxe para chamar um método de um classe,
                                                #para chamar a tarefa dentro do group responsável pela aquela tarefa.
    else:
        return 'group_check_temp.email_normal'

check_temp = BranchPythonOperator(task_id='check_temp',
                                  python_callable=avalia_temp,
                                  provide_context=True, #Par ler os valores dos xcom
                                  task_group=group_check_temp,
                                  dag=dag)


with group_check_temp:
    check_temp >> [send_email_alert, send_email_normal]

with group_database:
    create_table >> insert_data

file_sensor_task >> get_data
get_data >> group_check_temp
get_data >> group_database
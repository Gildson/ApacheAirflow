from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.http.sensors.http import HttpSensor
from datetime import datetime
import requests

dag = DAG(
    'dag_http_sensor',
    description = "Dag HTTP sensor",
    schedule_interval=None,
    start_date=datetime(2023,9,2),
    catchup=False,
    default_view='graph',
    tags=['Sensor']
)

def query_api():
    response = requests.get('https://api.publicapis.org/entries')
    print(response.text)

check_api = HttpSensor(task_id='check_api', http_conn_id='MyConnectionPublics',endpoint='entries',poke_interval=5,timeout=20,dag=dag)

process_data = PythonOperator(task_id='process_data', python_callable=query_api, dag=dag)

check_api >> process_data
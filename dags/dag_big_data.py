from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime
from big_data_operator import BigDataOperator

dag = DAG(
    'dag_big_data',
    description = "Dag for big data example",
    schedule_interval=None,
    start_date=datetime(2023,9,3),
    catchup=False,
    default_view='graph',
    tags=['Sensor']
)

big_data = BigDataOperator(task_id='big_data',
                           path_to_csv_file='/opt/airflow//data/Churn.csv',
                           path_to_save_file='/opt/airflow//data/Churn_big_data.json',
                           file_type='json',
                           dag=dag)

big_data
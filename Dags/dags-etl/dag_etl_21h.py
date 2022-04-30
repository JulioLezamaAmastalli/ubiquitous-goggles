from datetime import timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago

import os

path = os.path.dirname(os.path.abspath(__file__))
path_etl_general=os.path.join(path, 'etl_general.py')
path_etl_scores=os.path.join(path, 'etl_scores.py')
path_etl_standings=os.path.join(path, 'etl_standings.py')

params = {
    'path_etl_general': path_etl_general,
    'path_etl_scores': path_etl_scores,
    'path_etl_standings': path_etl_standings}

dag = DAG(
    'etl_dag_21h',
    description = '3 tables ETL dag',
    #At 21:00 every day
    schedule_interval='0 21 * * *',
    start_date = days_ago(1))

t1 = BashOperator(
    task_id='etl_general',
    depends_on_past=False,
    params=params,
    bash_command='python3 {{params.path_etl_general}}',
    dag=dag)


t2 = BashOperator(
    task_id='etl_scores',
    depends_on_past=False,
    params=params,
    bash_command='python3 {{params.path_etl_scores}}',
    dag=dag)

t3 = BashOperator(
    task_id='etl_standings',
    depends_on_past=False,
    params=params,
    bash_command='python3 {{params.path_etl_standings}}',
    dag=dag)


t1 >> t2
t2 >>t3

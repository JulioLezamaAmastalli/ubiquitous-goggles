from datetime import timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago

import os

path = os.path.dirname(os.path.abspath(__file__))
path_etl_api=os.path.join(path, 'etl_api.py')
path_etl_model=os.path.join(path, 'etl_model.py')

params = {
    'path_etl_api': path_etl_api,
    'path_etl_model': path_etl_model}

dag = DAG(
    'etl_dag',
    description = '2 step etl: API call + feat eng',
    #“At 13:00 on Friday.”    
    schedule_interval='0 13 * * 5',
    start_date = days_ago(1))

t1 = BashOperator(
    task_id='etl_api_call',
    depends_on_past=False,
    params=params,
    bash_command='python3 {{params.path_etl_api}}',
    dag=dag)


t2 = BashOperator(
    task_id='etl_feat_eng',
    depends_on_past=False,
    params=params,
    bash_command='python3 {{params.path_etl_model}}',
    dag=dag)


t1 >> t2

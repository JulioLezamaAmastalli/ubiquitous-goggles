from datetime import timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago

import os

path = os.path.dirname(os.path.abspath(__file__))
path_get_latest_version=os.path.join(path, 'get_latest_version')
path_predict=os.path.join(path, 'prediction.py')

params = {'path_get_latest_version': path_get_latest_version,
          'path_predict': path_predict}

dag = DAG(
    'predict',
    description = 'Create features table -> train -> eval',
    #At 09:00 on every 2nd day-of-week from Monday through Sunday.â€
    schedule_interval='50 13 * * 1/2',
    start_date = days_ago(1))

t1 = BashOperator(
    task_id='get_latest_version',
    depends_on_past=False,
    params=params,
    bash_command='{{params.path_get_latest_version}} ',
    dag=dag)

t2 = BashOperator(
    task_id='predictions',
    depends_on_past=False,
    params=params,
    bash_command='python3 {{params.path_predict}}',
    dag=dag)

t1 >> t2
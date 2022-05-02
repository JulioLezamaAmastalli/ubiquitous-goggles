from datetime import timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago

import os

path = os.path.dirname(os.path.abspath(__file__))
path_features=os.path.join(path, 'feat_eng.py')
path_train=os.path.join(path, 'train.py')

params = {
    'path_features': path_features,
    'path_train': path_train}

dag = DAG(
    'model_pipeline',
    description = 'Create features table -> train -> eval',
    #At 09:00 on every 2nd day-of-week from Monday through Sunday.”
    schedule_interval='50 13 * * 1/2',
    start_date = days_ago(1))

t1 = BashOperator(
    task_id='create features',
    depends_on_past=False,
    params=params,
    bash_command='python3 {{params.path_features}}',
    dag=dag)


t2 = BashOperator(
    task_id='train model',
    depends_on_past=False,
    params=params,
    bash_command='python3 {{params.path_train}}',
    dag=dag)


t1 >> t2


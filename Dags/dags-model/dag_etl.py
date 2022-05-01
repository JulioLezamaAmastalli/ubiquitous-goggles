from datetime import timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago

import os

path = os.path.dirname(os.path.abspath(__file__))
path_features=os.path.join(path, 'features.py')
path_train=os.path.join(path, 'train.py')
path_predict=os.path.join(path, 'predict.py')

params = {
    'path_features': path_features,
    'path_train': path_train,
    'path_predict': path_predict}

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

t3 = BashOperator(
    task_id='predictions',
    depends_on_past=False,
    params=params,
    bash_command='python3 {{params.path_predict}}',
    dag=dag)


t1 >> t2
t2 >>t3

from datetime import timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago

import os

path = os.path.dirname(os.path.abspath(__file__))
path_html_factory=os.path.join(path, 'html_factory.py')
path_html_to_bucket=os.path.join(path, 'html_to_bucket')

params = {
    'path_html_factory': path_html_factory,
    'path_html_to_bucket': path_html_to_bucket}
dag = DAG(
    'process 4 deployment',
    description = '2 step deployment: create html + send it to bucket',
    #“At 13:45 on Friday.”    
    schedule_interval='45 13 * * 5',
    start_date = days_ago(1))

t1 = BashOperator(
    task_id='html_factory',
    depends_on_past=False,
    params=params,
    bash_command='python3 {{params.path_html_factory}}',
    dag=dag)


t2 = BashOperator(
    task_id='html_to_bucket',
    depends_on_past=False,
    params=params,
    bash_command='python3 {{params.path_html_to_bucket}}',
    dag=dag)


t1 >> t2

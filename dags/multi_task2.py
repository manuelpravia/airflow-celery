from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from airflow.operators.bash import BashOperator
from airflow.contrib.operators.ssh_operator import SSHOperator
from datetime import datetime, timedelta
import json
import os
import pendulum
''''
local_tz = pendulum.timezone("America/Lima")
ruta_archivos = "/opt/airflow/dags/json"
archivos_json = os.listdir(ruta_archivos)

for archivo in archivos_json:
    archivo_leer = os.path.join(ruta_archivos, archivo)
    with open(archivo_leer, 'r') as file:
        dag_info = json.load(file)

    dag = DAG(
        dag_id=dag_info['dag_id'], 
        default_args=dag_info['default_args'],
        description=dag_info['description'],
        #schedule_interval='16 10 *  *  *',
        schedule_interval='*/30 * *  *  *',
        #schedule_interval=timedelta(days=1),
        #schedule_interval=timedelta(days=1),
        #schedule='@daily',
        #start_date=pendulum.datetime(2024,6,5, tz="America/Lima"),
        #start_date=pendulum.datetime(2024,6,3,tz='UTC'),
        tags=[dag_info['tags']],
        start_date= datetime(2024, 6, 4,tzinfo=local_tz),
        catchup=False,
        #is_paused_upon_creation=True 
    ) 
 
    tasks = {}
    for task_info in dag_info['tasks']:
        task_id = task_info['task_id']

        tasks[task_id] = SSHOperator(
            task_id=task_id,
            ssh_conn_id=task_info['ssh_conn_id'],
            command=task_info['command'],
            cmd_timeout=task_info['cmd_timeout'],
            do_xcom_push=True,
            dag=dag,
        )

    #start = EmptyOperator(task_id='start', dag=dag)
    #end = EmptyOperator(task_id='end', dag=dag)

    for task_info in dag_info['tasks']:
        task_id = task_info['task_id']
        predecesores = task_info.get('predecesores', [])
        if predecesores:
            for predecesor in predecesores:
                tasks[predecesor] >> tasks[task_id]
        #else:
        #    start >> tasks[task_id]
        #tasks[task_id] >> end

    globals()[dag.dag_id] = dag
'''
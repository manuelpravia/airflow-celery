from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import json
import os
'''
ruta_archivos = "/opt/airflow/dags/json"
archivos_json = os.listdir(ruta_archivos)

for archivo in archivos_json:
    archivo_leer = os.path.join(ruta_archivos, archivo)
    with open(archivo_leer, 'r') as file:
        dag_info = json.load(file)

    dag = DAG(
        dag_id=dag_info['dag_id'],
        default_args=dag_info['default_args'],
        description='DAG generado desde JSON',
        schedule_interval=timedelta(days=1),
        start_date=datetime(2024, 4, 30),
        tags=["load-data"],
        catchup=False,
        is_paused_upon_creation=True 
    )

    tasks = {}
    for task_info in dag_info['tasks']:
        task_id = task_info['task_id']
        python_file = task_info['python_file']
        tasks[task_id] = PythonOperator(
            task_id=task_id,
            python_callable=lambda: exec(open(task_info['python_file']).read()),
            dag=dag,
        )

    for task_info in dag_info['tasks']:
        task_id = task_info['task_id']
        predecesor = task_info['predecesor']
        if predecesor is not None:
            tasks[predecesor] >> tasks[task_id]

    start = tasks[dag_info['tasks'][0]['task_id']]
    end = tasks[dag_info['tasks'][-1]['task_id']]

    globals()[dag.dag_id] = dag
'''
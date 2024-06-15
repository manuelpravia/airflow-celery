from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
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
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from airflow.operators.bash import BashOperator
from airflow.contrib.operators.ssh_operator import SSHOperator
from datetime import datetime, timedelta
import json
import os
import pendulum
import requests
import logging

#limit_task
api_url = 'http://172.26.0.10:8087'
local_tz = pendulum.timezone("America/Lima")

def getDags():
    try:
        response = requests.get(api_url + "/dags")
        response.raise_for_status()  # Lanza una excepción si la petición no fue exitosa
        return response.json()
    except:
        logging.error("Ocurrio un error al obtener la lista de Dags...")

def getTaskByDagId(dagId):
    try:
        response_task = requests.get(api_url + "/dag/" + dagId + "/tasks")
        response_task.raise_for_status()  # Lanza una excepción si la petición no fue exitosa
        return response_task.json()
    except:
        logging.info("Ocurrio un error al obtener las lista de Task...")


objects = getDags()
for dag_info in objects:

    default_args = {
        "owner": dag_info['owner'],
        "depends_on_past": False,
        "email_on_failure": False,
        "email_on_retry": False,
        "retries": 1,
        "retry_delay": timedelta(minutes=2)
    }

    dag = DAG(
        dag_id=dag_info['name'], 
        default_args=default_args,
        description=dag_info['description'],
        #schedule_interval='16 10 *  *  *',
        #schedule_interval='*/30 * *  *  *',
        schedule_interval='*/10 9-10 *  *  *',
        #schedule_interval=timedelta(days=1),
        #schedule_interval=timedelta(minutes=5),
        #schedule='@daily',
        #start_date=pendulum.datetime(2024,6,5, tz="America/Lima"),
        #start_date=pendulum.datetime(2024,6,3,tz='UTC'),
        tags=[dag_info['tags']],
        start_date= datetime(2024, 6, 11,15,10,tzinfo=local_tz),
        catchup=False,
        #is_paused_upon_creation=True 
    ) 
 
    tasks = {}
    task_list = getTaskByDagId(str(dag_info['dag_id']))
     
    for task_info in task_list:
        task_id = task_info['name']
        comando = "python3 {}".format(task_info['script'])
        tasks[task_id] = SSHOperator(
            task_id=task_id,
            ssh_conn_id="my_ssh_conn",
            command=comando,
            cmd_timeout=120,
            do_xcom_push=True,
            dag=dag,
        )

    #start = EmptyOperator(task_id='start', dag=dag)
    #end = EmptyOperator(task_id='end', dag=dag)

    for task_info in task_list:
        task_id = task_info['task_id']
        task_name = task_info['name']
        predecesores = task_info['predecesor'].split(',')
        if predecesores:
            for predecesor in predecesores:
                elemento_encontrado = next((elemento for elemento in task_list if elemento['task_id'] == predecesor), None)
                if elemento_encontrado:
                    name = elemento_encontrado['name']
                    tasks[name] >> tasks[task_name]


    globals()[dag.dag_id] = dag

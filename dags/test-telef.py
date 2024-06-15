import time
import pendulum
from datetime import datetime, timedelta

from airflow import DAG
from airflow.exceptions import AirflowFailException
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.contrib.operators.ssh_operator import SSHOperator


dag_args = {
    "depends_on_past": False,  # si esta como true, Esta indica que solo se ejecutara si la misma tarea anterior ha tenido exito.
    "email": ["test@test.com"], # Lista de correos a los cuales se les enviaran notificaciones
    "email_on_failure": False, # Enviar correo cuando la tarea falle
    "email_on_retry": False,   # Enviar correo cuando latarea se reintente
    "retries": 1,  # Numero de veces que la tarea debe reintentarse si falla
    "retry_delay": timedelta(minutes=3), # Tiempo de espera entre reintentos cuando una tarea falla
    # 'queue': 'bash_queue', # Nombre de la cola en la que debe ejecutarse
    # 'pool': 'backfill',   # Nombre del pool a la que pertenece la tarea, los pool son usados para limitar las tareas concurrentes
    # 'priority_weight': 10,  # peso de prioridad de la tarea, las tareas con mayor peso tienen prioridad sobre las de menor peso
    # 'end_date': datetime(2016, 1, 1), # Fecha en que la tarea debe dejar de ejecutarse
    # 'wait_for_downstream': False,  # Si esta como ture, espera que todas las tareas decendientes se completen antes de marcar esta tarea como completada
    # 'sla': timedelta(hours=2), # Tiempo dentro del cual se espera que esa tarea se complete, si no se completa dentro de este tiempo se considera como fallido
    # 'execution_timeout': timedelta(seconds=300), # tiempo maximo de ejecucion para esa tarea, si excede se considera como fallido
    # 'on_failure_callback': some_function, # Funcion o lista de funciones que se ejecutaran cuando la tarea falle
    # 'on_success_callback': some_other_function, # Funcion o lista de funciones que se ejecutaran cuando la tarea se complete con exito
    # 'on_retry_callback': another_function, # Funcion o lista de funciones que se ejecutaran cuando la tarea se reintente
    # 'sla_miss_callback': yet_another_function, # Funcion o lista de funciones que se ejecutaran cuando la tarea falle en cumplir su sla
    # 'trigger_rule': 'all_success' # Define como se comporta una tarea en relacion a sus predecesoras. ejem all_success, all_failes, one_success
}

dag = DAG(
    "test_log_write_and_send",
    description="Mi primer DAG",
    default_args=dag_args,
    #schedule_interval=timedelta(days=1),
    schedule_interval=timedelta(days=1),
    #start_date=pendulum.datetime(2024,6,4, tz="America/Lima"),
    start_date=pendulum.datetime(2024,6,6),
    #start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["prueba-worker"],
)


def tareafinal_func(**kwargs):
    print("ejecutando tarae2: inicio de ejecucion")
    time.sleep(5)
    print( "Hola" )
    print("ejecucion de tarea2: fin de la ejecucion")
    return { "ok": 2 }

tarea_final = PythonOperator(
    task_id='tarea_final',
    python_callable=tareafinal_func,
    dag=dag
)

tarea1 = SSHOperator(
    task_id='ejecuta_carga_entre_servidores_desde_sevidor3',
    ssh_conn_id='my_ssh_conn_serv3',  # Nombre de tu conexión SSH configurada en Airflow
    command='python3 /root/load_data_postgres.py',  # Ruta al script de Python en el servidor remoto
    #params={'origen': 'Airflow container', 'destino': 'servidor remoto 1'},  # Parámetros que deseas enviar al script
    cmd_timeout=500,
    #queue='transform',
    do_xcom_push=True,  # Permite que la salida de la tarea se almacene en XCom para verla en la interfaz de Airflow
    dag=dag,
)


tarea1 >> tarea_final

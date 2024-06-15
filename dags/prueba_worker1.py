import time
from datetime import datetime, timedelta

from airflow import DAG
from airflow.exceptions import AirflowFailException
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.contrib.operators.ssh_operator import SSHOperator


dag_args = {
    "depends_on_past": False,
    "email": ["test@test.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
    # 'wait_for_downstream': False,
    # 'sla': timedelta(hours=2),
    # 'execution_timeout': timedelta(seconds=300),
    # 'on_failure_callback': some_function, # or list of functions
    # 'on_success_callback': some_other_function, # or list of functions
    # 'on_retry_callback': another_function, # or list of functions
    # 'sla_miss_callback': yet_another_function, # or list of functions
    # 'trigger_rule': 'all_success'
}

dag = DAG(
    "test_worker1",
    description="Mi primer DAG",
    default_args=dag_args,
    schedule_interval=timedelta(days=1),
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["prueba-worker"],
)


def tarea2_func(**kwargs):
    xcom_value = kwargs['ti'].xcom_pull(task_ids='tarea0')
    print("ejecutando tarae2: inicio de ejecucion")
    time.sleep(20)
    print( "Hola" )
    print( xcom_value )
    print("ejecucion de tarea2: fin de la ejecucion")
    return { "ok": 2 }



tarea1 = SSHOperator(
    task_id='ejecuta_carga_entre_servidores_desde_sevidor1',
    ssh_conn_id='my_ssh_conn',  # Nombre de tu conexión SSH configurada en Airflow
    command='python3 /root/ejecutar_servido2.py',  # Ruta al script de Python en el servidor remoto
    #params={'origen': 'Airflow container', 'destino': 'servidor remoto 1'},  # Parámetros que deseas enviar al script
    cmd_timeout=120,
    #queue='transform',
    do_xcom_push=True,  # Permite que la salida de la tarea se almacene en XCom para verla en la interfaz de Airflow
    dag=dag,
)

tarea2 = SSHOperator(
    task_id='Descargando_archivos_desde_azure_servidor2',
    ssh_conn_id='my_ssh_conn_serv2',  # Nombre de tu conexión SSH configurada en Airflow
    command='python3 /root/dowload_data_azure.py',  # Ruta al script de Python en el servidor remoto
    #params={'origen': 'Airflow container', 'destino': 'servidor remoto 1'},  # Parámetros que deseas enviar al script
    cmd_timeout=120,
    do_xcom_push=True,  # Permite que la salida de la tarea se almacene en XCom para verla en la interfaz de Airflow
    dag=dag,
)

tarea3 = SSHOperator(
    task_id='Cargando_data_oracle_servidor3',
    ssh_conn_id='my_ssh_conn_serv3',
    command='python3 /root/load_data_oracle.py',  
    cmd_timeout=120,
    do_xcom_push=True,
    dag=dag,
)

tarea4 = SSHOperator(
    task_id='Descargando_data_de_google_cloud_servidor2',
    ssh_conn_id='my_ssh_conn_serv2',
    command='python3 /root/dowload_data_google-cloud.py',  
    cmd_timeout=120,
    #queue='dowload',
    do_xcom_push=True,
    dag=dag,
)

tarea5 = SSHOperator(
    task_id='Caragando_data_mongoDB_servidor3',
    ssh_conn_id='my_ssh_conn_serv3',
    command='python3 /root/load_data_mongoDB.py',  
    cmd_timeout=120,
    #queue='load',
    do_xcom_push=True,
    dag=dag,
)

tarea6 = SSHOperator(
    task_id='transformando_data_csv_servidor1',
    ssh_conn_id='my_ssh_conn',
    command='python3 /root/transform_data_to_csv.py',  
    cmd_timeout=120,
    #queue='transform',
    do_xcom_push=True,
    dag=dag,
)

tarea7 = SSHOperator(
    task_id='cragando_data_a_postgres_servidor3',
    ssh_conn_id='my_ssh_conn_serv3',
    command='python3 /root/load_data_postgres.py',  
    cmd_timeout=120,
    do_xcom_push=True,
    dag=dag,
)

[tarea1, tarea2, tarea3 ]
tarea2 >> tarea4
tarea1 >> tarea6
tarea3 >> [tarea5, tarea6]
[tarea4, tarea5, tarea6] >> tarea7

#tarea0 >> tarea2 >> tarea3
import time
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
    "test_worker5",
    description="Mi primer DAG",
    default_args=dag_args,
    schedule_interval=timedelta(days=1),
    start_date=datetime(2024, 1, 1),
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
    task_id='ejecuta_carga_entre_servidores_desde_sevidor1',
    ssh_conn_id='my_ssh_conn',  # Nombre de tu conexión SSH configurada en Airflow
    command='python3 /root/ejecutar_servido2.py',  # Ruta al script de Python en el servidor remoto
    #params={'origen': 'Airflow container', 'destino': 'servidor remoto 1'},  # Parámetros que deseas enviar al script
    cmd_timeout=500,
    #queue='transform',
    do_xcom_push=True,  # Permite que la salida de la tarea se almacene en XCom para verla en la interfaz de Airflow
    pool='limit_task',
    dag=dag,
)

tarea2 = SSHOperator(
    task_id='Descargando_archivos_desde_azure_servidor2',
    ssh_conn_id='my_ssh_conn_serv2',  # Nombre de tu conexión SSH configurada en Airflow
    command='python3 /root/dowload_data_azure.py',  # Ruta al script de Python en el servidor remoto
    #params={'origen': 'Airflow container', 'destino': 'servidor remoto 1'},  # Parámetros que deseas enviar al script
    cmd_timeout=500,
    do_xcom_push=True,  # Permite que la salida de la tarea se almacene en XCom para verla en la interfaz de Airflow
    pool='limit_task',
    dag=dag,
)

tarea3 = SSHOperator(
    task_id='Cargando_data_oracle_servidor3',
    ssh_conn_id='my_ssh_conn_serv3',
    command='python3 /root/load_data_oracle.py',  
    cmd_timeout=500,
    do_xcom_push=True,
    pool='limit_task',
    dag=dag,
)

tarea4 = SSHOperator(
    task_id='Descargando_data_de_google_cloud_servidor2',
    ssh_conn_id='my_ssh_conn_serv2',
    command='python3 /root/dowload_data_google-cloud.py',  
    cmd_timeout=500,
    #queue='dowload',
    do_xcom_push=True,
    pool='limit_task',
    dag=dag,
)

tarea5 = SSHOperator(
    task_id='Caragando_data_mongoDB_servidor3',
    ssh_conn_id='my_ssh_conn_serv3',
    command='python3 /root/load_data_mongoDB.py',  
    cmd_timeout=500,
    #queue='load',
    do_xcom_push=True,
    pool='limit_task',
    dag=dag,
)

tarea6 = SSHOperator(
    task_id='transformando_data_csv_servidor1',
    ssh_conn_id='my_ssh_conn',
    command='python3 /root/transform_data_to_csv.py',  
    cmd_timeout=500,
    #queue='transform',
    do_xcom_push=True,
    pool='limit_task',
    dag=dag,
)


tarea7 = SSHOperator(
    task_id='cragando_data_a_postgres_servidor3',
    ssh_conn_id='my_ssh_conn_serv3',
    command='python3 /root/load_data_postgres.py',  
    cmd_timeout=500,
    do_xcom_push=True,
    pool='limit_task',
    dag=dag,
)


tarea8 = SSHOperator(
    task_id='extrayendo_data_a_mongo-db-servidor3',
    ssh_conn_id='my_ssh_conn_serv3',
    command='python3 /root/load_data_mongoDB.py',  
    cmd_timeout=500,
    do_xcom_push=True,
    pool='limit_task',
    dag=dag,
)


tarea9 = SSHOperator(
    task_id='ejecuta_descarga_entre_servidores_desde_sevidor1',
    ssh_conn_id='my_ssh_conn', 
    command='python3 /root/ejecutar_servido2.py',
    cmd_timeout=500,
    do_xcom_push=True, 
    pool='limit_task',
    dag=dag,
)


tarea10 = SSHOperator(
    task_id='cargando_data_de_google_cloud_servidor2',
    ssh_conn_id='my_ssh_conn_serv2',
    command='python3 /root/dowload_data_google-cloud.py',  
    cmd_timeout=500,
    #queue='dowload',
    do_xcom_push=True,
    pool='limit_task',
    dag=dag,
)

'''
tarea11 = SSHOperator(
    task_id='ejecutar_tara_11',
    ssh_conn_id='my_ssh_conn',  # Nombre de tu conexión SSH configurada en Airflow
    command='python3 /root/test/tarea11.py',  # Ruta al script de Python en el servidor remoto
    #params={'origen': 'Airflow container', 'destino': 'servidor remoto 1'},  # Parámetros que deseas enviar al script
    cmd_timeout=500,
    #queue='transform',
    do_xcom_push=True,  # Permite que la salida de la tarea se almacene en XCom para verla en la interfaz de Airflow
    dag=dag,
)


tarea12 = SSHOperator(
    task_id='ejecutar_tarea_12',
    ssh_conn_id='my_ssh_conn_serv2',
    command='python3 /root/test/tarea12.py',  
    cmd_timeout=500,
    #queue='dowload',
    do_xcom_push=True,
    dag=dag,
)


tarea13 = SSHOperator(
    task_id='ejecutar_tarea_13',
    ssh_conn_id='my_ssh_conn_serv3',
    command='python3 /root/test/tarea13.py',  
    cmd_timeout=500,
    #queue='dowload',
    do_xcom_push=True,
    dag=dag,
)


tarea14 = SSHOperator(
    task_id='ejecutar_tarea_14',
    ssh_conn_id='my_ssh_conn', 
    command='python3 /root/test/tarea14.py',
    cmd_timeout=500,
    do_xcom_push=True, 
    dag=dag,
)


tarea15 = SSHOperator(
    task_id='ejecutar_tarea_15',
    ssh_conn_id='my_ssh_conn_serv2', 
    command='python3 /root/test/tarea15.py',
    cmd_timeout=500,
    do_xcom_push=True, 
    dag=dag,
)

tarea16 = SSHOperator(
    task_id='ejecutar_tarea_16',
    ssh_conn_id='my_ssh_conn_serv3', 
    command='python3 /root/test/tarea16.py',
    cmd_timeout=500,
    do_xcom_push=True, 
    dag=dag,
)


tarea17 = SSHOperator(
    task_id='ejecutar_tarea_17',
    ssh_conn_id='my_ssh_conn', 
    command='python3 /root/test/tarea17.py',
    cmd_timeout=500,
    do_xcom_push=True, 
    dag=dag,
)

tarea18 = SSHOperator(
    task_id='ejecutar_tarea_18',
    ssh_conn_id='my_ssh_conn_serv2', 
    command='python3 /root/test/tarea18.py',
    cmd_timeout=500,
    do_xcom_push=True, 
    dag=dag,
)


tarea19 = SSHOperator(
    task_id='ejecutar_tarea_19',
    ssh_conn_id='my_ssh_conn_serv3', 
    command='python3 /root/test/tarea19.py',
    cmd_timeout=500,
    do_xcom_push=True, 
    dag=dag,
)


tarea20 = SSHOperator(
    task_id='ejecutar_tarea_20',
    ssh_conn_id='my_ssh_conn', 
    command='python3 /root/test/tarea20.py',
    cmd_timeout=500,
    do_xcom_push=True, 
    dag=dag,
)

tarea21 = SSHOperator(
    task_id='ejecutar_tarea_21',
    ssh_conn_id='my_ssh_conn_serv2', 
    command='python3 /root/test/tarea21.py',
    cmd_timeout=500,
    do_xcom_push=True, 
    dag=dag,
)


tarea22 = SSHOperator(
    task_id='ejecutar_tarea_22',
    ssh_conn_id='my_ssh_conn_serv3', 
    command='python3 /root/test/tarea22.py',
    cmd_timeout=500,
    do_xcom_push=True, 
    dag=dag,
)

tarea23 = SSHOperator(
    task_id='ejecutar_tarea_23',
    ssh_conn_id='my_ssh_conn', 
    command='python3 /root/test/tarea23.py',
    cmd_timeout=500,
    do_xcom_push=True, 
    dag=dag,
)

tarea24 = SSHOperator(
    task_id='ejecutar_tarea_24',
    ssh_conn_id='my_ssh_conn_serv2', 
    command='python3 /root/test/tarea24.py',
    cmd_timeout=500,
    do_xcom_push=True, 
    dag=dag,
)


tarea25 = SSHOperator(
    task_id='ejecutar_tarea_25',
    ssh_conn_id='my_ssh_conn_serv3', 
    command='python3 /root/test/tarea25.py',
    cmd_timeout=500,
    do_xcom_push=True, 
    dag=dag,
)
'''
[tarea1, tarea2, tarea3,tarea4, tarea5, tarea6,tarea7,tarea8,tarea9,tarea10]#,tarea11,tarea12,tarea13,tarea14,tarea15,tarea16,tarea17,tarea18,tarea19,tarea20,tarea21,tarea22,tarea23]
tarea1 >> tarea_final
tarea2 >> tarea_final
tarea3 >> tarea_final
tarea4 >> tarea_final
tarea5 >> tarea_final
tarea6 >> tarea_final
tarea7 >> tarea_final
tarea8 >> tarea_final
tarea9 >> tarea_final
tarea10 >> tarea_final
#tarea11 >> tarea_final
#tarea12 >> tarea_final
#tarea13 >> tarea_final
#area14 >> tarea_final
#tarea15 >> tarea_final
#tarea16 >> tarea_final
#tarea17 >> tarea_final
#tarea18 >> tarea_final
#tarea19 >> tarea_final
#tarea20 >> tarea_final
#tarea21 >> tarea_final
#tarea22 >> tarea_final
#tarea23 >> tarea_final
#tarea24 >> tarea_final
#tarea25 >> tarea_final
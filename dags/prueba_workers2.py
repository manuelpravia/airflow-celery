import time
from datetime import datetime, timedelta

from airflow import DAG
from airflow.exceptions import AirflowFailException
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator


dag_args = {
    "depends_on_past": False,
    "email": ["test@test.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
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
    "prueba_worker2",
    description="Mi primer DAG",
    default_args=dag_args,
    schedule_interval=timedelta(days=1),
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=["prueba-worker"],
)

def tarea0_func(**kwargs):
    conf = kwargs['dag_run'].conf
    print("ejecutando tarae0: inicio de ejecucion")
    time.sleep(20)
    print("ejecucion de tarea0: fin de la ejecucion")
    return { "ok": 1 }

def tarea2_func(**kwargs):
    xcom_value = kwargs['ti'].xcom_pull(task_ids='tarea0')
    print("ejecutando tarae2: inicio de ejecucion")
    time.sleep(20)
    print( "Hola" )
    print( xcom_value )
    print("ejecucion de tarea2: fin de la ejecucion")
    return { "ok": 2 }

def tarea3_func(**kwargs):
    xcom_value = kwargs['ti'].xcom_pull(task_ids='tarea2')
    print("ejecutando tarae3: inicio de ejecucion")
    time.sleep(20)
    print( "Hola" )
    print( xcom_value )
    print("ejecucion de tarea3: fin de la ejecucion")
    return { "ok": 3 }

def tarea4_func(**kwargs):
    xcom_value = kwargs['ti'].xcom_pull(task_ids='tarea2')
    print("ejecutando tarae3: inicio de ejecucion")
    time.sleep(20)
    print( "Hola tarea 4" )
    print( xcom_value )
    print("ejecucion de tarea4: fin de la ejecucion")
    return { "ok": 3 }

def tarea5_func(**kwargs):
    xcom_value = kwargs['ti'].xcom_pull(task_ids='tarea2')
    print("ejecutando tarae5: inicio de ejecucion")
    time.sleep(20)
    print( "Hola" )
    print( xcom_value )
    print("ejecucion de tarea5: fin de la ejecucion")
    return { "ok": 5 }

def tarea6_func(**kwargs):
    xcom_value = kwargs['ti'].xcom_pull(task_ids='tarea2')
    print("ejecutando tarea6: inicio de ejecucion")
    time.sleep(20)
    print( "Hola" )
    print( xcom_value )
    print("ejecucion de tarea6: fin de la ejecucion")
    return { "ok": 3 }


def tarea7_func(**kwargs):
    xcom_value = kwargs['ti'].xcom_pull(task_ids='tarea2')
    print("ejecutando tarae7: inicio de ejecucion")
    time.sleep(20)
    print( "Hola" )
    print( xcom_value )
    print("ejecucion de tarea3: fin de la ejecucion")
    return { "ok": 7 }


tarea2 = PythonOperator(
    task_id='tarea2',
    python_callable=tarea2_func,
    dag=dag
)

tarea3 = PythonOperator(
    task_id='tarea3',
    python_callable=tarea3_func,
    dag=dag
)

tarea4 = PythonOperator(
    task_id='tarea4',
    python_callable=tarea4_func,
    dag=dag
)

tarea5 = PythonOperator(
    task_id='tarea5',
    python_callable=tarea5_func,
    dag=dag
)

tarea6 = PythonOperator(
    task_id='tarea6',
    python_callable=tarea6_func,
    dag=dag
)

tarea7 = PythonOperator(
    task_id='tarea7',
    python_callable=tarea7_func,
    dag=dag
)


tarea1 = PythonOperator(
    task_id='tarea1',
    python_callable=tarea7_func,
    dag=dag
)

[tarea1, tarea2, tarea3 ]
tarea2 >> tarea4
tarea1 >> tarea6
tarea3 >> [tarea5, tarea6]
[tarea4, tarea5, tarea6] >> tarea7

#tarea0 >> tarea2 >> tarea3
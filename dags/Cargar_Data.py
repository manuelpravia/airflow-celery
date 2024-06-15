from datetime import datetime, timedelta

from airflow import DAG
from airflow.exceptions import AirflowFailException
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
import pendulum

local_tz = pendulum.timezone("America/Lima")

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
    "cargar_data",
    description="Carga la data de un archivo plano",
    default_args=dag_args,
    #schedule_interval=timedelta(days=1),
    schedule_interval='*/3 10 *  *  *',
    start_date= datetime(2024, 6, 12,10,30,tzinfo=local_tz),
    #start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["proceso_1"],
    params={"servidor": "H3serv","bd":"teradata1"}
)

def extraer_data_oracle_func(**kwargs):
    return {"OK":"Extraccion de data correcta"}

def send_data_func(**kwargs):
    xcom_value = kwargs['ti'].xcom_pull(task_ids='extraction')
    print("Se ejecuto el envio de la data")
    print(xcom_value)
    if "OK" in xcom_value:
        data_loaded = {"OK": "Datos cargados correctamente"}
        return data_loaded
    else:
        raise AirflowFailException("Error al cargar datos")





extracction = PythonOperator(
    task_id='extraction',
    python_callable=extraer_data_oracle_func,
    dag=dag
)

send = PythonOperator(
    task_id='send',
    python_callable=send_data_func,
    dag=dag
)


extracction >> send 

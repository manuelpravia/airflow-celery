
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from datetime import datetime

def generate_dynamic_dag(dag_id, schedule_interval, default_args):
    dag = DAG(dag_id=dag_id, schedule_interval=schedule_interval, default_args=default_args)

    with dag:
        start = EmptyOperator(task_id='start')
        end = EmptyOperator(task_id='end')

        start >> end

    return dag

# Ejemplo de configuración
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 4, 29),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
}

# Crear el DAG dinámico
dynamic_dag_id = 'dynamic_dag'
dynamic_schedule_interval = '0 0 * * *'
dynamic_dag = generate_dynamic_dag(dynamic_dag_id, dynamic_schedule_interval, default_args)

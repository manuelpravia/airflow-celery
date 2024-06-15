from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow.sensors.filesystem import FileSensor
from datetime import datetime, timedelta
import os

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024,4,29),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'dag_generado',
    default_args=default_args,
    description='Dag de prueba',
    schedule_interval='@daily',
    tags=['ejemplo_sensor'],
)

# Sensor waits for file to be created
file_sensor_task = FileSensor(
    task_id='sensor_archivo',
    poke_interval=10,  # Check every 10 seconds
    retries=5,
    filepath='/opt/airflow/dags/file.txt',  # Path to the file to wait for
    dag=dag,
)

# Dummy task to write to file
def write_to_file():
    with open('/opt/airflow/dags/file_out.txt', 'w') as f:
        f.write('Escribiendo desde el DAGS de airflow generado...')

write_task = PythonOperator(
    task_id='Escribe_archivo',
    python_callable=write_to_file,
    dag=dag,
)

# Define the task dependencies
file_sensor_task >> write_task



## DAGS que funciona correctamente
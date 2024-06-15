from datetime import datetime
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator

def generate_tasks():
    tasks = []
    # Aquí puedes implementar la lógica para generar tasks dinámicamente
    for i in range(1, 4):
        task = PythonOperator(
            task_id=f"task_{i}",
            python_callable=print_hello,
            dag=dag,
        )
        tasks.append(task)
    return tasks

def print_hello():
    print("Hello, world!")

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2022, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
}

dag = DAG(
    'dynamic_dag',
    default_args=default_args,
    description='A dynamic DAG',
    schedule_interval='@daily',
)

start_task = EmptyOperator(task_id='start_task', retries=3, dag=dag)
end_task = EmptyOperator(task_id='end_task', retries=3, dag=dag)

tasks = generate_tasks()

start_task >> tasks >> end_task

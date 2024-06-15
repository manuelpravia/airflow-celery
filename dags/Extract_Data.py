from datetime import datetime
import pandas as pd
from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook

# Configurar la conexión a la base de datos PostgreSQL
postgres_conn_id = 'postgresql+psycopg2://airflow:airflow@postgres/airflow'

# Definir la función para extraer datos de PostgreSQL y guardarlos en un archivo CSV temporal
def extract_data_to_csv():
    pg_hook = PostgresHook(postgres_conn_id=postgres_conn_id)
    conn = pg_hook.get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM nombre_tabla")
    rows = cursor.fetchall()
    df = pd.DataFrame(rows, columns=[desc[0] for desc in cursor.description])
    df.to_csv('/tmp/datos_temp.csv', index=False)

# Definir la función para cargar el archivo CSV en un DataFrame de pandas
def load_csv_to_dataframe():
    df = pd.read_csv('/tmp/datos_temp.csv')
    return df

# Definir la función para escribir el DataFrame en un archivo de texto
def write_dataframe_to_text(df):
    df.to_csv('/tmp/datos.txt', sep='\t', index=False)

# Definir el DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 4, 26),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
}

dag = DAG(
    'extract_postgres_data_to_text',
    default_args=default_args,
    description='Extract data from PostgreSQL, load into DataFrame, and write to text file',
    schedule_interval=None,
)

# Definir las tareas del DAG
extract_data_task = PythonOperator(
    task_id='extract_data',
    python_callable=extract_data_to_csv,
    dag=dag,
)

load_to_dataframe_task = PythonOperator(
    task_id='load_to_dataframe',
    python_callable=load_csv_to_dataframe,
    dag=dag,
)

write_to_text_task = PythonOperator(
    task_id='write_to_text',
    python_callable=write_dataframe_to_text,
    op_args=[],
    provide_context=True,
    dag=dag,
)


# Establecer la secuencia de las tareas
extract_data_task >> load_to_dataframe_task >> write_to_text_task

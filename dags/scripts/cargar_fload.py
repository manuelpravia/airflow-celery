import time

archivo_texto = "/opt/airflow/dags/scripts/archivo.txt"
time.sleep(5)
with open(archivo_texto, 'a') as archivo:
    # Escribe una cadena en una nueva línea en el archivo
    archivo.write('\nCargando data a Fload... ')
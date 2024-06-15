# Proyecto de airflow 2.9.0

Apache airflowes una plataforma de código abierto para crear, programar y monitorear flujosde trabajo de manera programática. Fue desarrolado por Airbnb y es ampliamnte utilizado en la industria para la automatzacion de tareas repetitivas y complejas en flujos de trabajo de datos.

## Servicios

1. **Webserver:** Prporcioa una interas de usuario para monitorer y gestionar los flujos de trabajo.
2. **Scheduler:** Monitoriza todas las tareas yDAGs y desencaena ls instancias de tareas una ves que sus dependecias esten compleadas.
3. **Worker:** Procesos en donde se ejecutan las tareas de dags. Estos toman las tareas de una cola de redis, las ejecutan y devuelven los resulado.
4. **Redis:** Maneja las colas de tareas y distribuye a los workers Asegurando la comuncaion eficiente entre el scheduler y los workers.
5. **PostgresSQL:** Almacena los metadatos de aiflow, nformcion de los dgas,las ejecuciones de lastareas logs y otras configraciones necesarias para airflow
6. **Flower** Interfas grafica para visualizar y gestionar las tareas,los workers y otros aspectos de celery en tiemo real

## Ejecución del Proyecto

Para ejecutar el proyecto localmente, asegúrate de tener instalado Docker y Docker Compose. Luego, clona el repositorio y ejecuta el siguiente comando en la raíz del proyecto:

1. **Crear los directorios:** Asegurarse de tener los directorios dags, logs, config, plugins
2. **Eejcutar el siguiente comando** ejecutar el primer comando, si requiere levantar mas de un worker ejecutar el segundo comando e indicar el numero de instancias de workers
```bash
docker-compose up -d

#Comado para Escalar servicios de workers
docker-compose up -d -scale airflow-worker=2
```
2. **Ingresar a la interfas** En el navegador ingresar a http://127.0.0.1:8080/ mostrara la interfas del webserver ingresar con user: airflow, pass: airflow
3. **Para levantar flower** Para levantar Flower ejecutamos el siguiente comando
```bash
docker-compose up -d flower
```


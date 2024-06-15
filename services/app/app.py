from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask_cors import CORS
import logging
import sys
import os

app = Flask(__name__)
CORS(app) 

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Crear un manejador para la consola (stdout)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)

# Crear un manejador para el archivo
file_handler = logging.FileHandler('logfile.log')
file_handler.setLevel(logging.INFO)

# Crear un formato común para ambos manejadores
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# Agregar los manejadores al logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)

# Configuración de la conexión a MongoDB
client = MongoClient("mongodb://172.26.0.9:27017/")
db = client["scheduler"]

dag = db["GD_AFDag_HTTP"]
task = db["GD_AFTask_HTTP"]
'''
@app.route('/dag', methods=['GET'])
def get_dags():
    dags_collection = db["dag"]
    dags = dags_collection.find()
    logger.info("Consultando por los dags...")
    return dumps(dags)
'''

@app.route('/dags', methods=['GET'])
def get_dags():
    dag_collection = db['GD_AFDag_HTTP']
    dags = dag_collection.find()
    result = []
    for dag in dags:
        result.append({
            '_id': str(dag['_id']),
            'dag_id': dag['dag_id'],
            'name': dag['name'],
            'owner': dag['owner'],
            'description': dag['description'],
            'schedule_interval': dag['schedule_interval'],
            'start_date': dag['start_date'],
            'tags': dag['tags'],
            'state': dag['state'],
            'create_ts': dag['create_ts'],
            'update_ts': dag['update_ts']
        })
    return jsonify(result)

@app.route('/dag/<dag_id>/tasks', methods=['GET'])
def get_tasks(dag_id):
    task_collection = db['GD_AFTask_HTTP']
    tasks = task_collection.find({'dag_id': dag_id})
    result = []
    for task in tasks:
        result.append({
            '_id': str(task['_id']),
            'task_id': task['task_id'],
            'dag_id': task['dag_id'],
            'name': task['name'],
            'description': task['description'],
            'task_type': task['task_type'],
            'predecesor': task['predecesor'],
            'state': task['state'],
            'layout': task['layout'],
            'fecha': task['fecha'],
            'script': task['script'],
            'create_ts': task['create_ts'],
            'update_ts': task['update_ts']
        })
    return jsonify(result)



if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=8087)


#!/bin/bash

#*************************************************************
#Descripcion: Shell para crear usuarios de manera masiva
#Fecha: 15/06/2024
#*************************************************************


messageFormatting(){
    FECHA_LOG=$(date '+%Y-%m-%d %H:%M:%S')
    echo "($FECHA_LOG) $*" 
}

start(){
    HORA_INICIO=$(date '+%Y-%m-%d %H:%M:%S')
    START_TIME=$(date '+%s')
    messageFormatting "---------------------------------------------------------------------------------"
    messageFormatting "            INICIANDO LA CREACION DE USUARIOS "
    messageFormatting "Sell: " $0
    messageFormatting "Fecha y hora: " $HORA_INICIO
    messageFormatting "----------------------------------------------------------------------------------"
}

end(){
    HORA_FIN=$(date '+%Y-%m-%d %H:%M:%S')
    END_TIME=$(date '+%s')
    ELAPSED_TIME=$((END_TIME - START_TIME))
    ELAPSED_HOURS=$((ELAPSED_TIME / 3600))
    ELAPSED_MINUTES=$((ELAPSED_TIME % 3600 / 60))
    ELAPSED_SECONDS=$((ELAPSED_TIME % 60))
    messageFormatting "---------------------------------------------------------------------------------"
    messageFormatting "           CREACION DE USUARIOS FINALIZADA"
    messageFormatting "Fecha y hora: " $HORA_FIN
    messageFormatting "Tiempo transcurrido: ${ELAPSED_HOURS}h ${ELAPSED_MINUTES}m ${ELAPSED_SECONDS}s"
    messageFormatting "----------------------------------------------------------------------------------"
}
 

createUsers(){
# Ruta al archivo CSV
USERS_FILE="/opt/airflow/config/data/users.csv"

if [ ! -f "$USERS_FILE" ]; then
    mensajeFormat "El archivo $USERS_FILE no existe. El proceso se ha detenido."
    exit 1
fi

messageFormatting "Creando usuarios ..."
# Leer el archivo CSV línea por línea, omitiendo la primera línea
tail -n +2 "$USERS_FILE" | while IFS=, read -r USERNAME FIRSTNAME LASTNAME ROLE EMAIL PASSWORD
do
  # Comprobar si el usuario ya existe
  EXISTS=$(airflow users list | grep -w "$USERNAME")

  if [ -n "$EXISTS" ]; then
    messageFormatting "El usuario $USERNAME ya existe. No se creará nuevamente."
  else
    # Crear el usuario
    airflow users create \
      --username "$USERNAME" \
      --firstname "$FIRSTNAME" \
      --lastname "$LASTNAME" \
      --role "$ROLE" \
      --email "$EMAIL" \
      --password "$PASSWORD"
    messageFormatting "Usuario $USERNAME creado exitosamente."
  fi
done 

}

main(){
    start
    createUsers
    end
}

main
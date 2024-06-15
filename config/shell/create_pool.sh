#!/bin/bash

#*************************************************************
#Descripcion: Shell para crear pools de manera masiva
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
    messageFormatting "            INICIANDO LA CREACION DE POOLS "
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
    messageFormatting "           CREACION DE POOLS FINALIZADA"
    messageFormatting "Fecha y hora: " $HORA_FIN
    messageFormatting "Tiempo transcurrido: ${ELAPSED_HOURS}h ${ELAPSED_MINUTES}m ${ELAPSED_SECONDS}s"
    messageFormatting "----------------------------------------------------------------------------------"
}

createPools(){
# Ruta al archivo CSV
POOL_FILE="/opt/airflow/config/data/pools.csv"

if [ ! -f "$POOL_FILE" ]; then
    messageFormatting "El archivo $POOL_FILE no existe. El roceso no puede continuar..."
    exit 1
fi

messageFormatting "Creando los Pools...."
# Leer el archivo CSV línea por línea, omitiendo la primera línea
tail -n +2 "$POOL_FILE" | while IFS=, read -r POOL_NAME SLOTS DESCRIPTION
do
  # Comprobar si el pool ya existe
  EXISTS=$(airflow pools list | grep -w "$POOL_NAME")

  if [ -n "$EXISTS" ]; then
    messageFormatting "El pool $POOL_NAME ya existe. Se actualizara..."
    airflow pools set "$POOL_NAME" "$SLOTS" "$DESCRIPTION"
  else
    # Crear o actualizar el pool
    airflow pools set "$POOL_NAME" "$SLOTS" "$DESCRIPTION"
    messageFormatting "Pool $POOL_NAME creado exitosamente."
  fi
done
}

main() {
    start
    createPools
    end
}

main
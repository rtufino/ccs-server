#!/bin/bash

# Script para obtener el respaldo de los registros del dia
# Autor: Rodrigo Tufino <rtufino@lisoft.net>
# Fecha: 11-01-2020

fecha=`date +%F`
hora=`date +%T`
FILE_LOC=/tmp/respaldo.sql
FILE_REM=`date "+%Y%m%d_%H%M%S"`.sql
FILE_LOG=respaldar.log

mysqldump -u root -ph8SEWNe3FQC5dR db_ccs registro --where="fecha>='$fecha 00:00:00'" > $FILE_LOC

if test -f "$FILE_LOC"; then
	scp -i /home/pi/.ssh/ccs-cloud-01 $FILE_LOC rtufino_lisoft_net@104.198.248.157:/home/rtufino_lisoft_net/respaldos/$FILE_REM
	echo [`date "+%F %T"`] - COPIADO AL SERVIDOR >> $FILE_LOG
else
	echo [`date "+%F %T"`] - NO SE CREO EL RESPALDO >> $FILE_LOG
fi

rm -f $FILE_LOC

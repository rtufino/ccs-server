#!/bin/bash

# Script para obtener el respaldo de los registros del dia
# Autor: Rodrigo Tufino <rtufino@lisoft.net>
# Version 1.0.1	11-01-2020
# Version 1.0.2	16-01-2020

fecha=`date +%F`
hora=`date +%T`
FILE_LOC=/tmp/respaldo.sql
FILE_REM=`date "+%Y%m%d"`.sql
FILE_LOG=respaldar.log

mysqldump -u root -ph8SEWNe3FQC5dR db_ccs registro --where="fecha>='$fecha 00:00:00' and fecha<='$fecha 23:59:59'" > $FILE_LOC

if test -f "$FILE_LOC"; then
        scp -i /home/pi/.ssh/ccs-cloud-01 $FILE_LOC rtufino_lisoft_net@104.198.248.157:/home/rtufino_lisoft_net/respaldos/$FILE_REM
        echo [`date "+%F %T"`] - RESPALDO COPIADO AL SERVIDOR $FILE_REM >> $FILE_LOG
        rm -f $FILE_LOC
else
        echo [`date "+%F %T"`] - NO SE CREO EL RESPALDO >> $FILE_LOG
fi

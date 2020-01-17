#!/bin/bash

# Script para establecer un tunel ssh con ccs-cloud-01
# Autor: Rodrigo Tufino <rtufino@lisoft.net>
# Version: 1.1 [11-01-2020]


log=tunel.log
usuario=pi
puerto=2049
np=`ps aux | grep $usuario | grep R$puerto | wc -l`
if [ $np -eq 1 ]
then
        ssh -f -N -T -R$puerto:127.0.0.1:22 -i /home/$usuario/.ssh/ccs-cloud-01 rtufino_lisoft_net@104.198.248.157
        echo [`date "+%F %T"`] - RECONECCION >> $log
else
        echo [`date "+%F %T"`] - EN EJECUCION >> $log
fi


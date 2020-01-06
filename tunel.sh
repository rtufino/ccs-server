#!/bin/bash

# Script para establecer un tunel con ccs-cloud-01
# Autor: Rodrigo Tufiño <rtufino@lisoft.net>
# Fecha: 06-01-2019

ssh -f -N -T -R2049:127.0.0.1:22 -i /home/pi/.ssh/ccs-cloud-01 rtufino_lisoft_net@104.198.248.157

#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  Copyright (C) Lisoft & AV Electronics - All Rights Reserved
#  Unauthorized copying of this file, via any medium is strictly prohibited
#  Proprietary and confidential
#  Written by Rodrigo Tufiño <rtufino@lisoft.net>, December 2019

"""
    ccs-server.app
    ~~~~~~~~~~~~~~

    Aplicación de servidor para registrar y visualizar llamadas de cajas
"""

from datetime import datetime
from os import environ

from flask import Flask, render_template, request, abort
from dotenv import load_dotenv, find_dotenv
from flask_socketio import SocketIO, emit, disconnect

from modelos import db, Hub, Evento, Caja, Registro

__author__ = 'Rodrigo Tufiño'
__copyright__ = 'Copyright 2019, Cashier Calling System'
__credits__ = ['Rodrigo Tufiño']
__license__ = 'Privative'
__version__ = '1.0.0'
__maintainer__ = 'LISOFT'
__email__ = 'rtufino@lisoft.net'
__status__ = 'Dev'

# Cargar archivo de configuracion
load_dotenv(find_dotenv())

# Flask
app = Flask(__name__)

# Configuraciones
app.config['DEBUG'] = True if environ.get('DEBUG') == 'True' else False
app.config['PORT'] = 80

# Base de Datos
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Socketio
app.config['SECRET_KEY'] = environ.get('SECRET_KEY')
DOMAIN = environ.get('DOMAIN')
async_mode = None
socketio = SocketIO(app, async_mode=async_mode)

# Variables
CODE_KEY = environ.get('CODE_KEY')
NAMESPACE = '/calling'


def validar_peticion(peticion):
    """
    Valida las cabeceras (headers) de una peticion RESTful
    :param peticion: Objeto request de Flask
    :return: True si es correcto. Abortará en caso de error
    """
    if not peticion.is_json:
        abort(400, "Invalid request format: application/json")
    try:
        if peticion.headers['X-Code-Key'] != CODE_KEY:
            abort(400, "Invalid code key number")
        if len(peticion.headers['X-Serial']) <= 0:
            abort(400, "No serial number sended")
    except KeyError:
        abort(406, "Invalid request")
    return True


@app.route('/')
def index():
    grupos = Caja.get_grupos()
    cajas = Caja.query.filter_by(estado=1).all()
    grid = 12 // len(grupos)
    return render_template('index.html',
                           anio=datetime.now().year,
                           version=__version__,
                           grupos=grupos,
                           grid=grid,
                           cajas=cajas)


@app.route('/viewer', methods=['GET'])
def viewer():
    grupo = request.args['grupo']
    return render_template('viewer.html',
                           async_mode=socketio.async_mode,
                           grupo=grupo)


@app.route('/api/v1.0/registrar', methods=['POST'])
def registrar():
    # Validar headers de la peticion
    validar_peticion(request)
    # Obtener el numero de caja
    numero_caja = request.json['caja']
    # Obtener la caja
    caja = Caja.get_by_numero(numero_caja)
    if caja is None:
        abort(400, "Cashier number invalid")
    # Emitir mensaje a WebSocket
    llamar_caja(caja)
    # Crear el registro
    registro = Registro(
        caja=caja.id,
        fecha=datetime.now(),
        estado=1
    )
    # Agregar a la base de datos
    db.session.add(registro)
    # Comprometer datos
    db.session.commit()
    # Retornar respuesta
    return {"message": "ok"}, 200


@app.route('/api/v1.0/iniciar', methods=['POST'])
def iniciar():
    # Validar headers de la peticion
    validar_peticion(request)
    # Obtener ip
    ip = request.json["IP"]
    # Obtener serial del hub
    serial = request.headers['X-Serial']
    # Obtener el hub
    hub = Hub.get_by_serial(serial)
    # Crear el evento
    evento = Evento(
        hub=hub.id,
        fecha=datetime.now(),
        descripcion=f"INICIADO;IP={ip}",
        estado=1
    )
    # Agregar a la base de datos
    db.session.add(evento)
    # Comprometer datos
    db.session.commit()
    # Retornar respuesta
    return {"message": "ok"}, 200


@socketio.on('connect', namespace=NAMESPACE)
def conectar():
    emit('servidor_conectado', {'data': 'Hi from server!'})


@socketio.on('navegador_conectado', namespace=NAMESPACE)
def test_message(message):
    ip = request.remote_addr
    print("Cliente conectado [" + ip + "] emite para el grupo", message['grupo'])
    emit('servidor_conectado', {'data': 'Hola. Emites para el grupo ' + str(message['grupo'])})


def llamar_caja(caja):
    socketio.emit('llamar', {
        'numero': caja.numero,
        'grupo': caja.grupo,
        'direccion': caja.direccion,
        'audio': caja.audio
    }, namespace=NAMESPACE)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')

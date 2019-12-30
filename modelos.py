#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  Copyright (C) Lisoft & AV Electronics - All Rights Reserved
#  Unauthorized copying of this file, via any medium is strictly prohibited
#  Proprietary and confidential
#  Written by Rodrigo Tufiño <rtufino@lisoft.net>, December 2019

"""
    Módulo con los modelos y administración de la base de datos
"""

from os import environ

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
app = Flask(__name__)

# Configuraciones
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Variables
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


class Banco(db.Model):
    __tablename__ = 'banco'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(64), nullable=False, unique=True)
    estado = db.Column(db.Integer, nullable=False, default=1)

    def __repr__(self):
        return f'<Banco {self.nombre}>'

    @staticmethod
    def get_by_id(id):
        return Banco.query.get(id)


class Sucursal(db.Model):
    __tablename__ = 'sucursal'
    id = db.Column(db.Integer, primary_key=True)
    banco = db.Column(db.Integer, db.ForeignKey('banco.id'), nullable=False)
    nombre = db.Column(db.String(64), nullable=False)
    direccion = db.Column(db.Text, nullable=True)
    telefono = db.Column(db.Text, nullable=True)
    estado = db.Column(db.Integer, nullable=False, default=1)


class TipoCaja(db.Model):
    __tablename__ = 'tipo_caja'

    id = db.Column(db.Integer, primary_key=True)
    banco = db.Column(db.Integer, db.ForeignKey('banco.id'), nullable=False)
    nombre = db.Column(db.String(64), nullable=False)
    estado = db.Column(db.Integer, nullable=False, default=1)


class Caja(db.Model):
    __tablename__ = 'caja'

    id = db.Column(db.Integer, primary_key=True)
    sucursal = db.Column(db.Integer, db.ForeignKey('sucursal.id'), nullable=False)
    tipo_caja = db.Column(db.Integer, db.ForeignKey('tipo_caja.id'), nullable=False)
    numero = db.Column(db.Integer, nullable=False)
    grupo = db.Column(db.Integer, nullable=False)
    direccion = db.Column(db.String(3), nullable=False)
    audio = db.Column(db.String(16), nullable=False)
    estado = db.Column(db.Integer, nullable=False, default=1)

    @staticmethod
    def get_by_numero(numero):
        return Caja.query.filter_by(numero=numero).first()

    @staticmethod
    def get_grupos():
        rows = Caja.query.filter_by(estado=1).group_by('grupo').all()
        grupos = []
        for r in rows:
            grupos.append(r.grupo)
        return grupos


class Hub(db.Model):
    __tablename__ = 'hub'

    id = db.Column(db.Integer, db.ForeignKey('sucursal.id'), primary_key=True)
    serial = db.Column(db.String(10), nullable=False, unique=True)
    fecha_instalacion = db.Column(db.DateTime, nullable=True)
    parametros = db.Column(db.Text, nullable=True)
    estado = db.Column(db.Integer, nullable=False, default=1)

    @staticmethod
    def get_by_serial(serial):
        return Hub.query.filter_by(serial=serial).first()


class Registro(db.Model):
    __tablename__ = 'registro'

    id = db.Column(db.Integer, primary_key=True)
    caja = db.Column(db.Integer, db.ForeignKey('caja.id'), nullable=False)
    fecha = db.Column(db.DateTime, nullable=False)
    estado = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Registro caja={self.caja}, fecha={self.fecha}, estado={self.estado}>'


class Evento(db.Model):
    __tablename__ = 'evento'

    id = db.Column(db.Integer, primary_key=True)
    hub = db.Column(db.Integer, db.ForeignKey('hub.id'), nullable=False)
    fecha = db.Column(db.DateTime, nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    estado = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Registro caja={self.caja}, fecha={self.fecha}, estado={self.estado}>'


if __name__ == "__main__":
    # Para administrar la base de datos
    # ref: https://programadorwebvalencia.com/tutorial-flask-para-crear-chat-con-socketio-y-vuejs/
    #
    # python3 models.py db init
    # python3 models.py db migrate
    # python3 models.py db upgrade
    manager.run()

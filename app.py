from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuración de SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:h8SEWNe3FQC5dR@192.168.100.75/db_ccs'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

api = Api(app)
db = SQLAlchemy(app)

from servicios import ListaRegistros, ListaEventos

api.add_resource(ListaRegistros, '/api/v1.0/registros')
api.add_resource(ListaEventos, '/api/v1.0/eventos/<int:tipo_evento>')


@app.route('/')
def index() -> str:
    return 'Cashier Calling System - Server v0.2'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

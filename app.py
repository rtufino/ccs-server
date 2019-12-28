from flask import Flask, render_template, session
from flask_socketio import SocketIO, emit
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from threading import Lock

app = Flask(__name__)

# Configuración de SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:h8SEWNe3FQC5dR@192.168.100.75/db_ccs'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

api = Api(app)
db = SQLAlchemy(app)

# Configuracion de servicio
# from servicios import ListaRegistros, ListaEventos
#
# api.add_resource(ListaRegistros, '/api/v1.0/registros')
# api.add_resource(ListaEventos, '/api/v1.0/eventos/<int:tipo_evento>')

# -------------
# Configuracion de SocletIO
# -------------
# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = None
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
# socketio = SocketIO(app)
thread = None
thread_lock = Lock()


def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        socketio.sleep(10)
        count += 1
        socketio.emit('my_response',
                      {'data': 'Server generated event', 'count': count},
                      namespace='/test')


@app.route('/')
def index() -> str:
    # return 'Cashier Calling System - Server v0.2'
    return render_template('index.html', async_mode=socketio.async_mode)
    # return render_template('index.html')


@socketio.on('connect', namespace='/test')
def test_connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)
    emit('my_response', {'data': 'Connected', 'count': 0})


if __name__ == '__main__':
    # app.run(debug=True, host='0.0.0.0')
    socketio.run(app, debug=True, host='0.0.0.0')

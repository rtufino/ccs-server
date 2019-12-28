from flask_restful import Resource, request, abort
from datetime import datetime
from controlador import Concentrador

CODE_NUMBER = '48b9f2fdb33fd40db329a60aad6c9148775a2b6a723ef45215d85e438f35392e'

REGISTROS = [
    {
        'caja': 1,
        'fecha': '2019-12-22 12:34:30'
    }
]


def validar_peticion(peticion):
    if not peticion.is_json:
        abort(400, message="Invalid request format: application/json")
    headers = peticion.headers
    try:
        if headers['X-Code'] != CODE_NUMBER:
            abort(400, message="Invalid code number")
        if len(headers['X-Serial']) <= 0:
            abort(400, message="No serial number sended")
    except KeyError:
        abort(406, message="Invalid request")
    return True


class ListaRegistros(Resource):
    def get(self):
        return {"registros": REGISTROS}, 200

    def post(self):
        validar_peticion(request)
        concentrador = Concentrador()
        caja = request.json['caja']
        resultado = concentrador.registrar_caja(numero_caja=caja)
        if resultado:
            return {"message": "OK"}, 200
        else:
            return {"message": concentrador.mensaje}, 500
        return {'message': 'OK'}, 200


class ListaEventos(Resource):

    def post(self, tipo_evento):
        validar_peticion(request)
        concentrador = Concentrador()
        ip = request.json["IP"]
        serial = request.headers['X-Serial']
        resultado = concentrador.registrar_evento(ip, serial, tipo_evento)
        if resultado:
            return {"message": "OK"}, 200
        else:
            return {"message": concentrador.mensaje}, 500

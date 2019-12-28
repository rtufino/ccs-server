from enum import Enum
from modelos import Hub, Evento, Caja, Registro
from datetime import datetime


# def registrar(tipoip):
#     print("registrando evento:", self.tipo_evento, "para el dispositivo", ip)
#     b = Banco()
#     b.nombre = ip
#     b.estado = 1
#     if not b.save():
#         self.mensaje = "Error al registrar el evento "
#         return False
#     return True

# class Caja:
#     mensaje = ""
#
#     def registrar(self, caja):
#         fecha = datetime.now()
#         estado = 1
#         registro = Registro(caja, fecha, estado)
#         if not registro.save():
#             self.mensaje =


class Concentrador:
    mensaje = ""

    def __init__(self):
        self.mensaje = ""

    def registrar_evento(self, ip, serial, tipo_evento):
        hub = Hub.get_by_serial(serial)
        evento = Evento()
        evento.hub = hub.id
        evento.fecha = datetime.now()
        evento.estado = 1
        texto = ''
        if tipo_evento == 1:
            texto = 'INICIADO'
        evento.descripcion = f"{texto}; IP={ip}"
        if not evento.save():
            self.mensaje = "Error on saving event"
            return False
        return True

    def registrar_caja(self, numero_caja, serial=None):
        # -------------------------------
        # Se necesitara el hub para consultar por Sucursal
        # cuando el sistema sea para multiples sucursales
        # hub = Hub.get_by_serial(serial)
        # -------------------------------
        caja = Caja.get_by_numero(numero_caja)
        registro = Registro()
        registro.caja = caja.id
        registro.fecha = datetime.now()
        registro.estado = 1
        if not registro.save():
            self.mensaje = "Error on saving register for cashier"
            return False
        return True

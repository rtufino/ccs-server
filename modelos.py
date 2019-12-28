from app import db
from sqlalchemy.exc import SQLAlchemyError


class Banco(db.Model):
    __tablename__ = 'banco'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(64), nullable=False, unique=True)
    estado = db.Column(db.Integer, nullable=False, default=1)
    # sucursales = db.relationship('Sucursal', backref='banco', lazy=True)
    # tipos_cajas = db.relationship('TipoCaja', backref='banco', lazy=True)

    def __repr__(self):
        return f'<Banco {self.nombre}>'

    def save(self):
        try:
            if not self.id:
                db.session.add(self)
            db.session.commit()
        except SQLAlchemyError as e:
            print(str(e.__dict__['orig']))
            return False
        return True

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
    # cajas = db.relationship('Caja', backref='sucursal', lazy=True)
    # hub = db.relationship('Hub', backref='sucursal', lazy=True, uselist=False)

    def save(self):
        try:
            if not self.id:
                db.session.add(self)
            db.session.commit()
        except SQLAlchemyError as e:
            print(str(e.__dict__['orig']))
            return False
        return True


class TipoCaja(db.Model):
    __tablename__ = 'tipo_caja'

    id = db.Column(db.Integer, primary_key=True)
    banco = db.Column(db.Integer, db.ForeignKey('banco.id'), nullable=False)
    nombre = db.Column(db.String(64), nullable=False)
    estado = db.Column(db.Integer, nullable=False, default=1)
    #cajas = db.relationship('Caja', backref='tipo_caja', lazy=True)

    def save(self):
        try:
            if not self.id:
                db.session.add(self)
            db.session.commit()
        except SQLAlchemyError as e:
            print(str(e.__dict__['orig']))
            return False
        return True


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
    # registros = db.relationship('Registro', backref='caja', lazy=True)

    def save(self):
        try:
            if not self.id:
                db.session.add(self)
            db.session.commit()
        except SQLAlchemyError as e:
            print(str(e.__dict__['orig']))
            return False
        return True

    @staticmethod
    def get_by_numero(numero):
        return Caja.query.filter_by(numero=numero).first()


class Hub(db.Model):
    __tablename__ = 'hub'

    id = db.Column(db.Integer, db.ForeignKey('sucursal.id'), primary_key=True)
    serial = db.Column(db.String(10), nullable=False, unique=True)
    fecha_instalacion = db.Column(db.DateTime, nullable=True)
    parametros = db.Column(db.Text, nullable=True)
    estado = db.Column(db.Integer, nullable=False, default=1)

    def save(self):
        try:
            if not self.id:
                db.session.add(self)
            db.session.commit()
        except SQLAlchemyError as e:
            print(str(e.__dict__['orig']))
            return False
        return True

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

    def save(self):
        try:
            if not self.id:
                db.session.add(self)
            db.session.commit()
        except SQLAlchemyError as e:
            print(str(e.__dict__['orig']))
            return False
        return True


class Evento(db.Model):
    __tablename__ = 'evento'

    id = db.Column(db.Integer, primary_key=True)
    hub = db.Column(db.Integer, db.ForeignKey('hub.id'), nullable=False)
    fecha = db.Column(db.DateTime, nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    estado = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Registro caja={self.caja}, fecha={self.fecha}, estado={self.estado}>'

    def save(self):
        try:
            if not self.id:
                db.session.add(self)
            db.session.commit()
        except SQLAlchemyError as e:
            print(str(e.__dict__['orig']))
            return False
        return True

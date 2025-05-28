from . import db

class OrdenBlatt(db.Model):
    __tablename__ = 'ordenes_blatt'

    id = db.Column(db.Integer, primary_key=True)
    numero_orden = db.Column(db.String(50), nullable=False)
    cliente = db.Column(db.String(100), nullable=False)
    fecha = db.Column(db.String(20), nullable=False)
    tiraje = db.Column(db.String(50), nullable=False)
    producto = db.Column(db.String(100), nullable=False)

    tamano_final = db.Column(db.String(100))
    paginas_interiores = db.Column(db.Integer)
    papel_interiores = db.Column(db.String(100))
    tintas_interiores = db.Column(db.String(100))
    papel_portada = db.Column(db.String(100))
    tintas_portada = db.Column(db.String(100))

    acabados = db.Column(db.String(255))
    precio_unitario = db.Column(db.Float)
    subtotal = db.Column(db.Float)
    total_iva = db.Column(db.Float)
    tiempo_entrega = db.Column(db.String(100))
    condiciones_pago = db.Column(db.String(255))

    razon_social = db.Column(db.String(255))
    rfc = db.Column(db.String(50))
    domicilio_fiscal = db.Column(db.String(255))

    nombre_cliente_rl = db.Column(db.String(100))


from werkzeug.security import generate_password_hash, check_password_hash

class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.Text, nullable=False)  # Ya actualizado
    rol = db.Column(db.String(20), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class OrdenImpresion(db.Model):
    __tablename__ = 'ordenes_impresion'

    id = db.Column(db.Integer, primary_key=True)
    numero_orden = db.Column(db.String(50), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    cliente = db.Column(db.String(255), nullable=False)

    # Detalles del producto
    nombre_producto = db.Column(db.String(255))
    tiraje = db.Column(db.Integer)
    tamano_final = db.Column(db.String(150))
    paginas_interiores = db.Column(db.String(10))
    papel_interiores = db.Column(db.String(100))
    tintas_interiores = db.Column(db.String(50))
    papel_portada = db.Column(db.String(100))
    tintas_portada = db.Column(db.String(50))
    acabados = db.Column(db.Text)
    observaciones = db.Column(db.Text)

    # Precios y condiciones
    precio_unitario = db.Column(db.Numeric(10, 2))
    subtotal = db.Column(db.Numeric(10, 2))
    total_iva = db.Column(db.Numeric(10, 2))
    condiciones_pago = db.Column(db.String(255))

    # Entrega
    tiempo_entrega = db.Column(db.String(100))
    lugar_entrega = db.Column(db.String(255))

    # Facturación
    razon_social = db.Column(db.String(255))
    rfc = db.Column(db.String(20))
    domicilio_fiscal = db.Column(db.Text)

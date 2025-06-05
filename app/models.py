from . import db
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

# Tabla CLIENTES
class Cliente(db.Model):
    __tablename__ = 'clientes'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.Text, nullable=False)
    razon_social = db.Column(db.Text)
    rfc = db.Column(db.Text, unique=True)
    domicilio_fiscal = db.Column(db.Text)
    representante_legal = db.Column(db.Text)
    email = db.Column(db.Text)
    telefono = db.Column(db.Text)

    # Precios personalizados
    precio_tiro = db.Column(db.Numeric(10, 2))
    precio_placas = db.Column(db.Numeric(10, 2))
    precio_engargolado = db.Column(db.Numeric(10, 2))
    precio_hotmelt = db.Column(db.Numeric(10, 2))
    precio_grapa = db.Column(db.Numeric(10, 2))
    precio_plastificado_m = db.Column(db.Numeric(10, 2))
    precio_plastificado_b = db.Column(db.Numeric(10, 2))
    precio_barniz_uv = db.Column(db.Numeric(10, 2))
    precio_folio = db.Column(db.Numeric(10, 2))
    precio_doblez = db.Column(db.Numeric(10, 2))
    precio_alzado = db.Column(db.Numeric(10, 2))
    precio_suaje = db.Column(db.Numeric(10, 2))
    precio_tabla_suaje = db.Column(db.Numeric(10, 2))
    precio_placa_foil = db.Column(db.Numeric(10, 2))
    precio_tiro_foil = db.Column(db.Numeric(10, 2))
    precio_empaque = db.Column(db.Numeric(10, 2))
    precio_corte = db.Column(db.Numeric(10, 2))

    cotizaciones = db.relationship("Cotizacion", back_populates="cliente", cascade="all, delete")
    ordenes = db.relationship("OrdenDeCompra", back_populates="cliente", cascade="all, delete")


# Tabla COTIZACIONES
class Cotizacion(db.Model):
    __tablename__ = 'cotizaciones'

    id = db.Column(db.Integer, primary_key=True)
    fecha_cotizacion = db.Column(db.Date)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'))
    cliente = db.relationship("Cliente", back_populates="cotizaciones")

    tiraje = db.Column(db.Integer)
    producto = db.Column(db.String)

    # INTERIOR
    tipo_papel_interior = db.Column(db.String)
    paginas_interior = db.Column(db.Integer)
    tamano_final_interior = db.Column(db.String)
    tamano_pliego_interior = db.Column(db.String)
    frente_vuelta_interior = db.Column(db.Boolean)
    paginas_x_pliego_interior = db.Column(db.Integer)
    precio_papel_interior = db.Column(db.Float)
    numero_tintas_interior = db.Column(db.Integer)
    plastificado_m_interior = db.Column(db.Boolean)
    plastificado_b_interior = db.Column(db.Boolean)
    barniz_uv_interior = db.Column(db.Boolean)
    suaje_interior = db.Column(db.Boolean)
    tabla_suaje_interior = db.Column(db.Boolean)
    folio_interior = db.Column(db.Boolean)

    # PORTADA
    tipo_papel_portada = db.Column(db.String)
    paginas_portada = db.Column(db.Integer)
    tamano_final_portada = db.Column(db.String)
    tamano_pliego_portada = db.Column(db.String)
    frente_vuelta_portada = db.Column(db.Boolean)
    paginas_x_pliego_portada = db.Column(db.Integer)
    precio_papel_portada = db.Column(db.Float)
    numero_tintas_portada = db.Column(db.Integer)
    plastificado_m_portada = db.Column(db.Boolean)
    plastificado_b_portada = db.Column(db.Boolean)
    barniz_uv_portada = db.Column(db.Boolean)
    suaje_portada = db.Column(db.Boolean)
    tabla_suaje_portada = db.Column(db.Boolean)
    folio_portada = db.Column(db.Boolean)

    # ACABADOS FINALES
    engargolado = db.Column(db.Boolean)
    hotmelt = db.Column(db.Boolean)
    grapa = db.Column(db.Boolean)
    doblez = db.Column(db.Boolean)
    alzado = db.Column(db.Boolean)
    empaque = db.Column(db.Boolean)
    corte = db.Column(db.Boolean)
    otros = db.Column(db.Boolean)

    # PRECIOS UNITARIOS
    precio_tiro = db.Column(db.Float)
    precio_placas = db.Column(db.Float)
    precio_engargolado = db.Column(db.Float)
    precio_hotmelt = db.Column(db.Float)
    precio_grapa = db.Column(db.Float)
    precio_plastificado_m = db.Column(db.Float)
    precio_plastificado_b = db.Column(db.Float)
    precio_barniz_uv = db.Column(db.Float)
    precio_folio = db.Column(db.Float)
    precio_doblez = db.Column(db.Float)
    precio_alzado = db.Column(db.Float)
    precio_suaje = db.Column(db.Float)
    precio_tabla_suaje = db.Column(db.Float)
    precio_placa_foil = db.Column(db.Float)
    precio_tiro_foil = db.Column(db.Float)
    precio_empaque = db.Column(db.Float)
    precio_corte = db.Column(db.Float)
    precio_otros = db.Column(db.Float)

    # SUBTOTAL GENERAL
    subtotal = db.Column(db.Float)

    # Relación con ordenes
    ordenes = db.relationship("OrdenDeCompra", back_populates="cotizacion", cascade="all, delete-orphan")


# Tabla ORDENES DE COMPRA
class OrdenDeCompra(db.Model):
    __tablename__ = 'ordenes_de_compra'

    id = db.Column(db.Integer, primary_key=True)
    num_oc = db.Column(db.String(50), unique=True, nullable=False)
    fecha_oc = db.Column(db.Date, nullable=False)

    cotizacion_id = db.Column(db.Integer, db.ForeignKey('cotizaciones.id', ondelete='CASCADE'), nullable=False)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id', ondelete='CASCADE'), nullable=False)

    razon_social = db.Column(db.Text)
    rfc = db.Column(db.Text)
    domicilio_fiscal = db.Column(db.Text)
    representante_legal = db.Column(db.Text)
    email = db.Column(db.Text)
    telefono = db.Column(db.Text)

    factura = db.Column(db.Boolean)
    tiempo_entrega = db.Column(db.Text)
    condiciones_pago = db.Column(db.Text)

    subtotal = db.Column(db.Numeric(10, 2))
    iva = db.Column(db.Numeric(10, 2))
    total = db.Column(db.Numeric(10, 2))

    fecha_produccion = db.Column(db.Date)
    fecha_impresion = db.Column(db.Date)
    prioridad = db.Column(db.Text)
    entregado = db.Column(db.Boolean, default=False)

    cotizacion = db.relationship("Cotizacion", back_populates="ordenes")
    cliente = db.relationship("Cliente", back_populates="ordenes")


# Tabla USUARIOS
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    rol = db.Column(db.String(20), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

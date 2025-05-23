from flask import Blueprint, render_template, request, redirect, url_for
from .models import OrdenImpresion
from . import db
from datetime import datetime

main = Blueprint('main', __name__, url_prefix='')  # <--- AÑADE ESTO

@main.route('/')
def index():
    return redirect(url_for('main.nueva_orden'))

@main.route('/nueva', methods=['GET', 'POST'])
def nueva_orden():
    if request.method == 'POST':
        orden = OrdenImpresion(
            numero_orden=request.form['numero_orden'],
            fecha=datetime.strptime(request.form['fecha'], '%Y-%m-%d'),
            cliente=request.form['cliente'],
            nombre_producto=request.form['nombre_producto'],
            tiraje=request.form['tiraje'],
            tamano_final=request.form['tamano_final'],
            paginas_interiores=request.form['paginas_interiores'],
            papel_interiores=request.form['papel_interiores'],
            tintas_interiores=request.form['tintas_interiores'],
            papel_portada=request.form['papel_portada'],
            tintas_portada=request.form['tintas_portada'],
            acabados=request.form['acabados'],
            observaciones=request.form['observaciones'],
            precio_unitario=request.form['precio_unitario'],
            subtotal=request.form['subtotal'],
            total_iva=request.form['total_iva'],
            condiciones_pago=request.form['condiciones_pago'],
            tiempo_entrega=request.form['tiempo_entrega'],
            lugar_entrega=request.form['lugar_entrega'],
            razon_social=request.form['razon_social'],
            rfc=request.form['rfc'],
            domicilio_fiscal=request.form['domicilio_fiscal']
        )
        db.session.add(orden)
        db.session.commit()
        return 'Orden registrada con éxito ✅'

    return render_template('nueva_orden.html')

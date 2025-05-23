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
        try:
            orden = OrdenImpresion(
                numero_orden=request.form.get('numero_orden', '').strip(),
                fecha=datetime.strptime(request.form['fecha'], '%Y-%m-%d'),
                cliente=request.form.get('cliente', '').strip(),
                nombre_producto=request.form.get('nombre_producto', '').strip(),
                tiraje=int(request.form.get('tiraje', '0')),
                tamano_final=request.form.get('tamano_final', '').strip(),
                paginas_interiores=request.form.get('paginas_interiores', '').strip(),
                papel_interiores=request.form.get('papel_interiores', '').strip(),
                tintas_interiores=request.form.get('tintas_interiores', '').strip(),
                papel_portada=request.form.get('papel_portada', '').strip(),
                tintas_portada=request.form.get('tintas_portada', '').strip(),
                acabados=request.form.get('acabados', '').strip(),
                observaciones=request.form.get('observaciones', '').strip(),
                precio_unitario=float(request.form.get('precio_unitario', '0')),
                subtotal=float(request.form.get('subtotal', '0')),
                total_iva=float(request.form.get('total_iva', '0')),
                condiciones_pago=request.form.get('condiciones_pago', '').strip(),
                tiempo_entrega=request.form.get('tiempo_entrega', '').strip(),
                lugar_entrega=request.form.get('lugar_entrega', '').strip(),
                razon_social=request.form.get('razon_social', '').strip(),
                rfc=request.form.get('rfc', '').strip(),
                domicilio_fiscal=request.form.get('domicilio_fiscal', '').strip()
            )
            db.session.add(orden)
            db.session.commit()
            return 'Orden registrada con éxito ✅'
        except Exception as e:
            return f"<h1>Error al guardar</h1><p>{str(e)}</p>", 500

    return render_template('nueva_orden.html')

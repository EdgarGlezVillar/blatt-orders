from flask import Blueprint, render_template, request, redirect, url_for
from . import db
from .models import OrdenBlatt

main = Blueprint('main', __name__)

@main.route('/')
def index():
    # Solo muestra las tablas disponibles
    inspector = db.inspect(db.engine)
    tablas = inspector.get_table_names()
    return render_template('nueva_orden.html', tablas=tablas)

@main.route('/nueva-orden', methods=['GET', 'POST'])
def nueva_orden():
    if request.method == 'POST':
        orden = OrdenBlatt(
            numero_orden = request.form['numero_orden'],
            cliente = request.form['cliente'],
            fecha = request.form['fecha'],
            tiraje = request.form['tiraje'],
            producto = request.form['producto'],
            tamano_final = request.form['tamano_final'],
            paginas_interiores = request.form.get('paginas_interiores') or 0,
            papel_interiores = request.form['papel_interiores'],
            tintas_interiores = request.form['tintas_interiores'],
            papel_portada = request.form['papel_portada'],
            tintas_portada = request.form['tintas_portada'],
            acabados = request.form['acabados'],
            precio_unitario = float(request.form.get('precio_unitario') or 0),
            subtotal = float(request.form.get('subtotal') or 0),
            total_iva = float(request.form.get('total_iva') or 0),
            tiempo_entrega = request.form['tiempo_entrega'],
            condiciones_pago = request.form['condiciones_pago'],
            razon_social = request.form['razon_social'],
            rfc = request.form['rfc'],
            domicilio_fiscal = request.form['domicilio_fiscal'],
            nombre_cliente_rl = request.form['nombre_cliente_rl'],
        )

        @main.route('/ordenes')
        def ver_ordenes():
            ordenes = OrdenBlatt.query.all()
            return render_template('ver_ordenes.html', ordenes=ordenes)


        db.session.add(orden)
        db.session.commit()

        return redirect(url_for('main.index'))

    return render_template('nueva_orden.html')

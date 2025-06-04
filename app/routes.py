from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from . import db
from .models import Usuario, Cliente, Cotizacion, OrdenDeCompra
import datetime

main = Blueprint('main', __name__)

# ----------------------------
# LOGIN
# ----------------------------
@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = Usuario.query.filter_by(username=request.form['username']).first()
        if user and user.check_password(request.form['password']):
            session['usuario'] = user.username
            session['rol'] = user.rol
            return redirect(url_for('main.menu'))
        flash('Usuario o contraseña incorrectos')
    return render_template('login.html')

@main.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.login'))

# ----------------------------
# MENÚ PRINCIPAL
# ----------------------------
@main.route('/menu')
def menu():
    if 'usuario' not in session:
        return redirect(url_for('main.login'))
    return render_template('menu.html', usuario=session['usuario'], rol=session['rol'])

# ----------------------------
# REGISTRO DE CLIENTES
# ----------------------------
@main.route('/registrar-cliente', methods=['GET', 'POST'])
def registrar_cliente():
    if 'usuario' not in session or session.get('rol') != 'ventas':
        flash('Acceso no autorizado.')
        return redirect(url_for('main.menu'))

    if request.method == 'POST':
        cliente = Cliente(
            nombre=request.form['nombre'],
            razon_social=request.form['razon_social'],
            rfc=request.form['rfc'],
            domicilio_fiscal=request.form['domicilio_fiscal'],
            representante_legal=request.form['representante_legal'],
            email=request.form['email'],
            telefono=request.form['telefono'],
            precio_tiro=request.form.get('precio_tiro') or 0,
            precio_placas=request.form.get('precio_placas') or 0,
            precio_engargolado=request.form.get('precio_engargolado') or 0,
            precio_hotmelt=request.form.get('precio_hotmelt') or 0,
            precio_grapa=request.form.get('precio_grapa') or 0,
            precio_plastificado_m=request.form.get('precio_plastificado_m') or 0,
            precio_plastificado_b=request.form.get('precio_plastificado_b') or 0,
            precio_barniz_uv=request.form.get('precio_barniz_uv') or 0,
            precio_folio=request.form.get('precio_folio') or 0,
            precio_doblez=request.form.get('precio_doblez') or 0,
            precio_alzado=request.form.get('precio_alzado') or 0,
            precio_suaje=request.form.get('precio_suaje') or 0,
            precio_tabla_suaje=request.form.get('precio_tabla_suaje') or 0,
            precio_placa_foil=request.form.get('precio_placa_foil') or 0,
            precio_tiro_foil=request.form.get('precio_tiro_foil') or 0,
            precio_empaque=request.form.get('precio_empaque') or 0,
            precio_corte=request.form.get('precio_corte') or 0
        )
        db.session.add(cliente)
        db.session.commit()
        flash('Cliente registrado correctamente.')
        return redirect(url_for('main.menu'))

    return render_template('registrar_cliente.html')


# ----------------------------
# REGISTRO DE COTIZACIÓN
# ----------------------------
@main.route('/registrar-cotizacion', methods=['GET', 'POST'])
def registrar_cotizacion():
    if 'usuario' not in session or session.get('rol') != 'ventas':
        flash('Acceso no autorizado.')
        return redirect(url_for('main.menu'))

    clientes = Cliente.query.all()

    if request.method == 'POST':
        cliente_id = request.form.get('cliente_id')
        cliente = Cliente.query.get(cliente_id)

        if not cliente:
            flash('Cliente no encontrado.')
            return redirect(url_for('main.registrar_cotizacion'))

        # Cálculos y extracción de datos
        tiraje = int(request.form['tiraje'])
        paginas_interior = int(request.form['paginas_interior'])
        paginas_x_pliego = int(request.form['paginas_x_pliego_interior'])
        frente_vuelta = 'frente_vuelta_interior' in request.form
        numero_tintas = int(request.form['numero_tintas_interior'])

        precio_tiro = float(request.form.get('precio_tiro') or 0)
        precio_placas = float(request.form.get('precio_placas') or 0)
        precio_plastificado_m = float(request.form.get('precio_plastificado_m') or 0)
        precio_plastificado_b = float(request.form.get('precio_plastificado_b') or 0)
        precio_barniz_uv = float(request.form.get('precio_barniz_uv') or 0)
        precio_suaje = float(request.form.get('precio_suaje') or 0)
        precio_tabla_suaje = float(request.form.get('precio_tabla_suaje') or 0)

        # Interior
        pliegos = paginas_interior / paginas_x_pliego
        fv = 2 if frente_vuelta else 1
        placas = numero_tintas * pliegos * fv
        tiros = numero_tintas * pliegos * fv * precio_tiro
        acabados = (
            int('plastificado_m_interior' in request.form) * precio_plastificado_m +
            int('plastificado_b_interior' in request.form) * precio_plastificado_b +
            int('barniz_uv_interior' in request.form) * precio_barniz_uv +
            int('suaje_interior' in request.form) * precio_suaje
        )
        acabados_total = ((pliegos * tiraje * fv) / 1000) * acabados
        acabados_total += int('tabla_suaje_interior' in request.form) * precio_tabla_suaje
        subtotal_interior = placas * precio_placas + tiros + acabados_total

        # Portada
        paginas_portada = int(request.form['paginas_portada'])
        paginas_x_pliego_portada = int(request.form['paginas_x_pliego_portada'])
        frente_vuelta_portada = 'frente_vuelta_portada' in request.form
        numero_tintas_portada = int(request.form['numero_tintas_portada'])

        pliegos_portada = paginas_portada / paginas_x_pliego_portada
        fv_portada = 2 if frente_vuelta_portada else 1
        placas_portada = numero_tintas_portada * pliegos_portada * fv_portada
        tiros_portada = numero_tintas_portada * pliegos_portada * fv_portada * precio_tiro
        acabados_portada = (
            int('plastificado_m_portada' in request.form) * precio_plastificado_m +
            int('plastificado_b_portada' in request.form) * precio_plastificado_b +
            int('barniz_uv_portada' in request.form) * precio_barniz_uv +
            int('suaje_portada' in request.form) * precio_suaje
        )
        total_acabados_portada = ((pliegos_portada * tiraje * fv_portada) / 1000) * acabados_portada
        total_acabados_portada += int('tabla_suaje_portada' in request.form) * precio_tabla_suaje
        subtotal_portada = placas_portada * precio_placas + tiros_portada + total_acabados_portada

        # Acabados finales
        precio_grapa = float(request.form.get('precio_grapa') or 0)
        precio_hotmelt = float(request.form.get('precio_hotmelt') or 0)
        precio_engargolado = float(request.form.get('precio_engargolado') or 0)
        precio_doblez = float(request.form.get('precio_doblez') or 0)
        precio_alzado = float(request.form.get('precio_alzado') or 0)
        precio_empaque = float(request.form.get('precio_empaque') or 0)
        precio_corte = float(request.form.get('precio_corte') or 0)
        precio_otros = float(request.form.get('precio_otros') or 0)

        acabados_finales = (
            int('engargolado' in request.form) * precio_engargolado +
            int('hotmelt' in request.form) * precio_hotmelt +
            int('grapa' in request.form) * precio_grapa +
            int('doblez' in request.form) * precio_doblez +
            int('alzado' in request.form) * precio_alzado +
            int('empaque' in request.form) * precio_empaque +
            int('corte' in request.form) * precio_corte +
            int('otros' in request.form) * precio_otros
        )
        subtotal_acabados_finales = tiraje * acabados_finales

        # Subtotal final
        subtotal_general = subtotal_interior + subtotal_portada + subtotal_acabados_finales

        cotizacion = Cotizacion(
            fecha_cotizacion=datetime.date.today(),
            cliente_id=cliente.id,
            tiraje=tiraje,
            producto=request.form.get('producto'),
            precio_tiro=precio_tiro,
            precio_placas=precio_placas,
            precio_plastificado_m=precio_plastificado_m,
            precio_plastificado_b=precio_plastificado_b,
            precio_barniz_uv=precio_barniz_uv,
            precio_suaje=precio_suaje,
            precio_tabla_suaje=precio_tabla_suaje,
            precio_grapa=precio_grapa,
            precio_hotmelt=precio_hotmelt,
            precio_engargolado=precio_engargolado,
            precio_doblez=precio_doblez,
            precio_alzado=precio_alzado,
            precio_empaque=precio_empaque,
            precio_corte=precio_corte,
            precio_otros=precio_otros,
            subtotal=subtotal_general
        )
        db.session.add(cotizacion)
        db.session.commit()
        flash(f'Cotización registrada con subtotal: ${subtotal_general:,.2f}')
        return redirect(url_for('main.menu'))

    return render_template('registrar_cotizacion.html', clientes=clientes)


# ----------------------------
# REGISTRO DE ORDEN DE COMPRA
# ----------------------------
@main.route('/registrar-orden', methods=['GET', 'POST'])
def registrar_orden():
    if 'usuario' not in session or session.get('rol') != 'ventas':
        flash('Acceso no autorizado.')
        return redirect(url_for('main.menu'))

    cotizaciones = Cotizacion.query.all()
    cotizacion_seleccionada = None

    if request.method == 'POST':
        if 'seleccionar' in request.form:
            cotizacion_id = request.form['cotizacion_id']
            cotizacion_seleccionada = Cotizacion.query.get(cotizacion_id)
            return render_template('registrar_orden.html', cotizaciones=cotizaciones, cotizacion=cotizacion_seleccionada)

        orden = OrdenDeCompra(
            num_oc=request.form['num_oc'],
            fecha_oc=datetime.datetime.strptime(request.form['fecha_oc'], '%Y-%m-%d').date(),
            cotizacion_id=int(request.form['cotizacion_id']),
            cliente_id=int(request.form['cliente_id']),
            razon_social=request.form['razon_social'],
            rfc=request.form['rfc'],
            domicilio_fiscal=request.form['domicilio_fiscal'],
            representante_legal=request.form['representante_legal'],
            email=request.form['email'],
            telefono=request.form['telefono'],
            factura='factura' in request.form,
            tiempo_entrega=request.form['tiempo_entrega'],
            subtotal=float(request.form['subtotal']),
            iva=float(request.form['iva']),
            total=float(request.form['total']),
            condiciones_pago=request.form['condiciones_pago'],
            fecha_produccion=datetime.datetime.strptime(request.form['fecha_produccion'], '%Y-%m-%d').date(),
            fecha_impresion=datetime.datetime.strptime(request.form['fecha_impresion'], '%Y-%m-%d').date(),
            prioridad=request.form['prioridad'],
            entregado='entregado' in request.form
        )
        db.session.add(orden)
        db.session.commit()
        flash('Orden de compra registrada correctamente.')
        return redirect(url_for('main.menu'))

    return render_template('registrar_orden.html', cotizaciones=cotizaciones)


# ----------------------------
# REDIRECCIÓN RAÍZ
# ----------------------------
@main.route('/')
def index():
    return redirect(url_for('main.login'))

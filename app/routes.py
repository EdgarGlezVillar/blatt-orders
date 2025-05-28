from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from . import db
from .models import OrdenBlatt, Usuario

main = Blueprint('main', __name__)

# RUTA: login
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

# RUTA: logout
@main.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.login'))

# RUTA: menú principal
@main.route('/menu')
def menu():
    if 'usuario' not in session:
        return redirect(url_for('main.login'))
    return render_template('menu.html', usuario=session['usuario'], rol=session['rol'])

# RUTA: usuarios
@main.route('/usuarios')
def ver_usuarios():
    if 'usuario' not in session:
        return redirect(url_for('main.login'))
    usuarios = Usuario.query.all()
    return render_template('usuarios.html', usuarios=usuarios)

# RUTA: gestión base
@main.route('/gestion-base')
def gestion_base():
    if 'usuario' not in session:
        return redirect(url_for('main.login'))
    return '<h1>Gestión de base en construcción</h1>'

# RUTA: raíz redirige a login
@main.route('/')
def index():
    return redirect(url_for('main.login'))

# RUTA: registrar nueva orden (solo admin)
@main.route('/nueva-orden', methods=['GET', 'POST'])
def nueva_orden():
    if 'usuario' not in session or session.get('rol') != 'admin':
        flash('Acceso no autorizado.')
        return redirect(url_for('main.menu'))

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
            nombre_cliente_rl = request.form['nombre_cliente_rl']
        )
        db.session.add(orden)
        db.session.commit()
        return redirect(url_for('main.ver_ordenes'))

    return render_template('nueva_orden.html')

# RUTA: ver órdenes
@main.route('/ordenes')
def ver_ordenes():
    if 'usuario' not in session:
        return redirect(url_for('main.login'))
    ordenes = OrdenBlatt.query.all()
    return render_template('ver_ordenes.html', ordenes=ordenes)

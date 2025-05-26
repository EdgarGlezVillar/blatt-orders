from flask import Blueprint, render_template
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    # Obtener las tablas de la base de datos
    inspector = db.inspect(db.engine)
    tablas = inspector.get_table_names()
    return render_template('nueva_orden.html', tablas=tablas)

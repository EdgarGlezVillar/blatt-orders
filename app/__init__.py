from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv('SECRET_KEY', 'clave_dev_segura_123')

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # 👉 Importar rutas
    from .routes import main
    app.register_blueprint(main)

    from . import models  # 👈 Esto fuerza que los modelos se registren en SQLAlchemy

    # 👉 Crear tablas y usuarios base
    with app.app_context():
        db.create_all()

        from .models import Usuario

        # Usuario administrador
        if not Usuario.query.filter_by(username='admin').first():
            admin = Usuario(username='admin', rol='admin')
            admin.set_password('admin123')
            db.session.add(admin)

        # Usuario ventas
        if not Usuario.query.filter_by(username='ventas').first():
            ventas = Usuario(username='ventas', rol='ventas')
            ventas.set_password('ventas123')
            db.session.add(ventas)

        # Usuario producción
        if not Usuario.query.filter_by(username='prod').first():
            prod = Usuario(username='prod', rol='produccion')
            prod.set_password('prod123')
            db.session.add(prod)

        db.session.commit()

    return app

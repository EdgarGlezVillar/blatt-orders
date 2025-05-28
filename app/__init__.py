from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # 👉 Importar rutas
    from .routes import main
    app.register_blueprint(main)

    from . import models  # 👈 Esto fuerza que los modelos se registren en SQLAlchemy

    # 👉 Crear tablas si no existen
    with app.app_context():
        db.create_all()
                # Crear usuarios base si no existen
        from .models import Usuario

        if not Usuario.query.filter_by(username='admin').first():
            admin = Usuario(username='admin', rol='admin')
            admin.set_password('admin123')
            db.session.add(admin)

        if not Usuario.query.filter_by(username='general').first():
            general = Usuario(username='general', rol='general')
            general.set_password('general123')
            db.session.add(general)

        db.session.commit()


    return app

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Usa tus propias credenciales de DATABASE_URL (de tu dashboard de PostgreSQL)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')  # Lo cargas desde variables de entorno
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Importar rutas
    from .routes import main
    app.register_blueprint(main)

    return app

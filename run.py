from app import create_app, db
from app.models import OrdenImpresion  # Asegúrate de importar el modelo

app = create_app()

with app.app_context():
    db.create_all()
    print("✅ Tablas creadas (o ya existentes) en la base de datos PostgreSQL")


if __name__ == '__main__':
    app.run(debug=True)

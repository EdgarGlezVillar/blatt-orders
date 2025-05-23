import os
from app import create_app, db

app = create_app()

# Solo ejecuta db.create_all() si estamos en Render (evitamos que lo haga localmente en cada arranque)
if os.environ.get('RENDER'):
    with app.app_context():
        db.create_all()
        print("✔️ Tablas creadas automáticamente en Render")

if __name__ == '__main__':
    app.run(debug=True)

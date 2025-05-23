import os
from app import create_app, db

app = create_app()

# Solo ejecutar esto si estás en entorno local de desarrollo
if os.environ.get("FLASK_ENV") == "development":
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    app.run(debug=True)

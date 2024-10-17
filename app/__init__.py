# /var/www/mi_proyecto/app/__init__.py

from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    with app.app_context():
        # Aquí se pueden registrar rutas y inicializar extensiones
        from .views import main
        app.register_blueprint(main)

    return app


import os
from flask_admin import Admin
from models import db, User, People, Planet, Favorite
from flask_admin.contrib.sqla import ModelView

def setup_admin(app):
    # Configurar la clave secreta para la aplicación Flask, necesaria para la administración de sesiones y seguridad
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')

    # Configurar el tema de Flask-Admin utilizando 'cerulean', que es un tema Bootstrap
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

    # Crear una instancia de Flask-Admin para la aplicación, con nombre '4Geeks Admin'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')

    # Agregar los modelos a la vista de administrador, lo que permite gestionarlos desde la interfaz de Flask-Admin
    admin.add_view(ModelView(User, db.session))    # Añadir el modelo User
    admin.add_view(ModelView(People, db.session))  # Añadir el modelo People
    admin.add_view(ModelView(Planet, db.session))  # Añadir el modelo Planet
    admin.add_view(ModelView(Favorite, db.session)) # Añadir el modelo Favorite

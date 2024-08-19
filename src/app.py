"""
Este módulo se encarga de iniciar el servidor API, cargar la base de datos y añadir los endpoints.
"""
import os
from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planet, Favorite

# Cargar las variables de entorno desde un archivo .env
load_dotenv()

# Crear una instancia de la aplicación Flask
app = Flask(__name__)
app.url_map.strict_slashes = False  # Deshabilitar la necesidad de usar / al final de las rutas

# Configurar la base de datos usando una URL desde las variables de entorno
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Deshabilitar la modificación de seguimiento (menos uso de memoria)

# Inicializar la base de datos con la aplicación
db.init_app(app)
MIGRATE = Migrate(app, db)  # Manejar las migraciones de la base de datos
CORS(app)  # Habilitar Cross-Origin Resource Sharing
setup_admin(app)  # Configurar la interfaz de administración

# Crear todas las tablas en la base de datos
with app.app_context():
    db.create_all()

# Manejar/serializar errores como objetos JSON
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# Generar el mapa del sitio con todos los endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# Endpoint para obtener todas las personas
@app.route('/people', methods=['GET'])
def get_people():
    people = People.query.all()  # Consultar todas las personas en la base de datos
    return jsonify([person.serialize() for person in people])  # Serializar y devolver como JSON

# Endpoint para obtener una persona por ID
@app.route('/people/<int:people_id>', methods=['GET'])
def get_person(people_id):
    person = People.query.get_or_404(people_id)  # Consultar una persona por ID o devolver un error 404
    return jsonify(person.serialize())

# Endpoint para obtener todos los planetas
@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planet.query.all()  # Consultar todos los planetas en la base de datos
    return jsonify([planet.serialize() for planet in planets])

# Endpoint para obtener un planeta por ID
@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planet.query.get_or_404(planet_id)  # Consultar un planeta por ID o devolver un error 404
    return jsonify(planet.serialize())

# Endpoint para obtener todos los usuarios
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()  # Consultar todos los usuarios en la base de datos
    return jsonify([user.serialize() for user in users])

# Endpoint para obtener los favoritos del primer usuario
@app.route('/users/favorites', methods=['GET'])
def get_user_favorites():
    user = User.query.first()  # Obtener el primer usuario
    favorites = Favorite.query.filter_by(user_id=user.id).all()  # Consultar los favoritos del usuario
    return jsonify([favorite.serialize() for favorite in favorites])

# Endpoint para añadir un planeta a los favoritos del primer usuario
@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    user = User.query.first()  # Obtener el primer usuario
    new_favorite = Favorite(user_id=user.id, planet_id=planet_id)  # Crear un nuevo favorito
    db.session.add(new_favorite)  # Añadir a la sesión de la base de datos
    db.session.commit()  # Guardar los cambios en la base de datos
    return jsonify({'message': 'Favorite planet added successfully'}), 201  # Devolver un mensaje de éxito

# Endpoint para añadir una persona a los favoritos del primer usuario
@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_person(people_id):
    user = User.query.first()  # Obtener el primer usuario
    new_favorite = Favorite(user_id=user.id, people_id=people_id)  # Crear un nuevo favorito
    db.session.add(new_favorite)  # Añadir a la sesión de la base de datos
    db.session.commit()  # Guardar los cambios en la base de datos
    return jsonify({'message': 'Favorite person added successfully'}), 201  # Devolver un mensaje de éxito

# Endpoint para eliminar un planeta de los favoritos del primer usuario
@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    user = User.query.first()  # Obtener el primer usuario
    favorite = Favorite.query.filter_by(user_id=user.id, planet_id=planet_id).first()  # Buscar el favorito
    if favorite:
        db.session.delete(favorite)  # Eliminar de la sesión de la base de datos
        db.session.commit()  # Guardar los cambios en la base de datos
        return jsonify({'message': 'Favorite planet removed successfully'})  # Devolver un mensaje de éxito
    return jsonify({'message': 'Favorite not found'}), 404  # Devolver un mensaje de error si no se encuentra

# Endpoint para eliminar una persona de los favoritos del primer usuario
@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_person(people_id):
    user = User.query.first()  # Obtener el primer usuario
    favorite = Favorite.query.filter_by(user_id=user.id, people_id=people_id).first()  # Buscar el favorito
    if favorite:
        db.session.delete(favorite)  # Eliminar de la sesión de la base de datos
        db.session.commit()  # Guardar los cambios en la base de datos
        return jsonify({'message': 'Favorite person removed successfully'})  # Devolver un mensaje de éxito
    return jsonify({'message': 'Favorite not found'}), 404  # Devolver un mensaje de error si no se encuentra

# Este código solo se ejecuta si el script es ejecutado directamente (no importado)
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))  # Obtener el puerto desde las variables de entorno o usar 3000 por defecto
    app.run(host='0.0.0.0', port=PORT, debug=False)  # Iniciar el servidor en el puerto especificado

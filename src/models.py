from flask_sqlalchemy import SQLAlchemy

# Inicializamos la extensión de SQLAlchemy
db = SQLAlchemy()

# Definición del modelo User que representa a un usuario en la base de datos
class User(db.Model):
    # Definimos las columnas de la tabla 'user'
    id = db.Column(db.Integer, primary_key=True)  # Identificador único para cada usuario
    email = db.Column(db.String(120), unique=True, nullable=False)  # Correo electrónico del usuario, debe ser único y no puede estar vacío
    password = db.Column(db.String(80), unique=False, nullable=False)  # Contraseña del usuario, no es único pero no puede estar vacío
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)  # Indica si el usuario está activo o no

    # Relación uno a muchos con el modelo 'Favorite'
    favorites = db.relationship('Favorite', backref='user', lazy=True)

    # Método para representar el objeto como una cadena (útil para depuración)
    def __repr__(self):
        return f'<User {self.email}>'

    # Método para serializar los datos del usuario a un diccionario (útil para convertir a JSON)
    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "is_active": self.is_active
        }

# Definición del modelo People que representa una persona en la base de datos
class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Identificador único para cada persona
    name = db.Column(db.String(120), nullable=False)  # Nombre de la persona, no puede estar vacío

    # Método para representar el objeto como una cadena
    def __repr__(self):
        return f'<People {self.name}>'

    # Método para serializar los datos de la persona a un diccionario
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }

# Definición del modelo Planet que representa un planeta en la base de datos
class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Identificador único para cada planeta
    name = db.Column(db.String(120), nullable=False)  # Nombre del planeta, no puede estar vacío

    # Método para representar el objeto como una cadena
    def __repr__(self):
        return f'<Planet {self.name}>'

    # Método para serializar los datos del planeta a un diccionario
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }

# Definición del modelo Favorite que representa los favoritos de un usuario
class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Identificador único para cada favorito
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Relación con el usuario, no puede estar vacío
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'))  # Relación opcional con una persona
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'))  # Relación opcional con un planeta

    # Método para representar el objeto como una cadena
    def __repr__(self):
        return f'<Favorite {self.id}>'

    # Método para serializar los datos del favorito a un diccionario
    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "people_id": self.people_id,
            "planet_id": self.planet_id
        }

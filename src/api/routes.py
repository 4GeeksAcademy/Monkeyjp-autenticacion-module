# ¿Qué son las variables de entorno?
# Son valores que se cargan en la memoria de la app al arrancar.
# No están “hardcodeados” en el código → eso evita exponer información sensible en GitHub.


# Hash de contraseñas 🔑
# ❓ ¿Qué es un hash?
# Un hash es una transformación matemática de un texto (como una contraseña) a una cadena irreconocible.
# No se puede revertir fácilmente (no se puede obtener la contraseña original a partir del hash).

# ¿Por qué usamos hash para las contraseñas?
# Nunca guardamos contraseñas en texto plano en la base de datos (sería inseguro).
# Si alguien hackea la base de datos, vería solo hashes.
# Cuando un usuario se loguea, tomamos la contraseña que ingresó, la hasheamos y la comparamos con el hash guardado.

# JWT (JSON Web Token) 🪙
# ❓ ¿Qué es un JWT?
# Es un token (una cadena de texto única) que representa la sesión de un usuario autenticado.
# Está compuesto por 3 partes codificadas en base64:
# Header → información del algoritmo.
# Payload → información del usuario (ej: su id o email).
# Signature → validación para comprobar que no fue alterado.

# ¿Cómo funciona?
# Usuario hace login con email y password.
# Si las credenciales son correctas, el servidor genera un JWT y se lo devuelve al cliente.
# El cliente guarda el JWT (normalmente en localStorage).
# Cada vez que hace una petición privada, envía el JWT en el header Authorization.
# El backend valida el token → si es válido, permite el acceso; si no, devuelve 401 Unauthorized.

# ¿Por qué implementamos esto en nuestras apps?
# Seguridad: los usuarios solo acceden a lo que les corresponde.
# Escalabilidad: el backend no necesita guardar sesiones en memoria (JWT es “stateless”).
# Buenas prácticas: cualquier app real (red social, e-commerce, etc.) necesita autenticación.

# INSTALACIONES NECESARIAS
# pipenv install flask-bcrypt
# Documentacion: https://flask-bcrypt.readthedocs.io/en/1.0.1/
# pipenv install flask-jwt-extended
# Documentacion: https://flask-jwt-extended.readthedocs.io/en/stable/index.html


"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required


from sqlalchemy.exc import IntegrityError

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200


@api.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"msg": "Email and password are required"}), 400

    existing_user = db.session.execute(db.select(User).where(
        User.email == email)).scalar_one_or_none()
    if existing_user:
        return jsonify({"msg": "User with this email already exists"}), 409

    new_user = User(email=email)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "User created successfully"}), 201


@api.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"msg": "Email and password are required"}), 400

    user = db.session.execute(db.select(User).where(
        User.email == email)).scalar_one_or_none()

    if user is None:
        return jsonify({"msg": "Invalid email or password"}), 401

    if user.check_password(password):
        access_token = create_access_token(identity=str(user.id))
        return jsonify({"msg": "Login successful", "token": access_token}), 200
    else:
        return jsonify({"msg": "Invalid email or password"}), 401


@api.route('/profile', methods=["GET"])
@jwt_required()
# ¿Qué hace?
# Indica que esa ruta solo puede usarse si el usuario tiene un JWT válido.
# Si no se envía el token, o si está mal/expirado → Flask devuelve automáticamente 401 Unauthorized.
def get_profile():
    user_id = get_jwt_identity()
    user = db.session.get(User, int(user_id))

    if not user:
        return jsonify({"msg": "User not found"}), 404

    return jsonify(user.serialize()), 200

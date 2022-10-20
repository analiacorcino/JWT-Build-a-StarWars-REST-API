"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Users, Bookmarks, Characters, Planets
import json
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager

#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)




###################################################### inicio get



@app.route('/users', methods=['GET'])
def get_all_users():

    users = Users.query.all() # esto obtiene todos los registros de la tabla User
    results = list(map(lambda item: item.serialize(), users)) #esto serializa los datos del arrays users

    return jsonify(results), 200


@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):

    user = Users.query.filter_by(id=user_id).first()

    return jsonify(user.serialize()), 200




###################################################### inicio get



#Obtenemos todos los favoritos de un usuario
@app.route('/user/<int:user_id>/bookmarks', methods=['GET'])
def get_all_user_bookmarks(user_id):

    bookmarks = Bookmarks.query.filter_by(user_id=user_id).all() # esto obtiene todos los registros de la tabla User
    results = list(map(lambda item: item.serialize(), bookmarks)) #esto serializa los datos del arrays users

    return jsonify(results), 200

#Obtenemos un favorito dependiendo de la ID
@app.route('/user/<int:user_id>/bookmark/<int:bookmark_id>', methods=['GET'])
def get_one_user_bookmark(user_id, bookmark_id):

    bookmark = Bookmarks.query.filter_by(id=bookmark_id).first()

    return jsonify(bookmark.serialize()), 200



###################################################### inicio get




@app.route('/characters', methods=['GET'])
def get_all_characters():

    characters = Characters.query.all() # esto obtiene todos los registros de la tabla User
    results = list(map(lambda item: item.serialize(), characters)) #esto serializa los datos del arrays users

    return jsonify(results), 200


@app.route('/character/<int:character_id>', methods=['GET'])
def get_character(character_id):

    character = Characters.query.filter_by(id=character_id).first()

    return jsonify(character.serialize()), 200



###################################################### inicio get




@app.route('/planets', methods=['GET'])
def get_all_planets():

    planets = Planets.query.all() # esto obtiene todos los registros de la tabla User
    results = list(map(lambda item: item.serialize(), planets)) #esto serializa los datos del arrays users

    return jsonify(results), 200


@app.route('/planet/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):

    planet = Planets.query.filter_by(id=planet_id).first()

    return jsonify(planet.serialize()), 200




###################################################### fin get




###################################################### inicio POST USERS


#endpoint para crear usuario
@app.route('/users/new', methods=['POST'])
def create_user():
    body = json.loads(request.data)
    # data = request.get_json()
    # print(data)

    query_user = Users.query.filter_by(email=body["email"]).first()
    print(query_user)
    
    # if body["email"] == query_user.email:
    if query_user is None:
        #guardar datos recibidos a la tabla User
        new_user = Users(
        password=body["password"],
        email=body["email"],
        username=body["username"],
        first_name=body["first_name"],
        last_name=body["last_name"])

        db.session.add(new_user)
        db.session.commit()
        response_body = {
               "msg": "Usuario creado con exito!"
            }

        return jsonify(response_body), 200

    response_body = {
            "msg": "Este usuario ya existe maaaann"
        }
    return jsonify(response_body), 400





##################################################### inicio POST PLANETS


#endpoint para crear planets
@app.route('/planets/new', methods=['POST'])
def create_planet():
    body = json.loads(request.data)


    query_planet = Planets.query.filter_by(name=body["name"]).first()
    print(query_planet)
    

    if query_planet is None:
        #guardar datos recibidos a la tabla planet
        new_planet = Planets(
            name=body["name"],
            climate=body["climate"],
            diameter=body["diameter"],
            orbital_period=body["orbital_period"],
            rotation_period=body["rotation_period"],
            population=body["population"])
       
        db.session.add(new_planet)
        db.session.commit()
        response_body = {
               "msg": "Planeta creado con exito!"
            }

        return jsonify(response_body), 200

    response_body = {
            "msg": "Este planeta ya existe maaaann"
        }
    return jsonify(response_body), 400



##################################################### inicio POST Characters


#endpoint para crear Characters
@app.route('/characters/new', methods=['POST'])
def create_character():
    body = json.loads(request.data)


    query_character = Characters.query.filter_by(name=body["name"]).first()
    print(query_character)
    

    if query_character is None:
        #guardar datos recibidos a la tabla character
        new_character = Characters(
            name=body["name"],
            birth_year=body["birth_year"],
            gender=body["gender"],
            height=body["height"],
            skin_color=body["skin_color"],
            eye_color=body["eye_color"])
       
        db.session.add(new_character)
        db.session.commit()
        response_body = {
               "msg": "Personaje creado con exito!"
            }

        return jsonify(response_body), 200

    response_body = {
            "msg": "Este personaje ya existe maaaann"
        }
    return jsonify(response_body), 400







##################################################### inicio POST Bookmarks


#endpoint para crear Bookmarks
@app.route('/bookmarks/new', methods=['POST'])
def create_bookmark():
    body = json.loads(request.data)


    query_user = Bookmarks.query.filter_by(user_id=body["user_id"]).first()
    print(query_user)
    if query_user is None:
        response_body = {
            "msg": "El usuario no existe"
        }
        return jsonify(response_body), 400


    #guardar datos recibidos a la tabla bookmark
    new_bookmark = Bookmarks(
        user_id=body["user_id"],
        planet_id=body["planet_id"],
        character_id=body["character_id"])
    
    db.session.add(new_bookmark)
    db.session.commit()
    response_body = {
            "msg": "Favorito creado con exito!"
        }

    return jsonify(response_body), 200

    

################### DELETEEEE




###################################################### inicio DELETE




@app.route('/user/delete/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):

    user = Users.query.filter_by(id=user_id).first()

    if user is None:
        raise APIException('Usuario no encontrado', status_code=404)

    db.session.delete(user)
    db.session.commit()
    response_body = {
           "msg": "Usuario eliminado con exito!"
        }
    return jsonify(response_body), 200
   




###################################################### inicio DELETE Personaje




@app.route('/character/delete/<int:character_id>', methods=['DELETE'])
def delete_character(character_id):

    character = Characters.query.filter_by(id=character_id).first()

    if character is None:
        raise APIException('Personaje no encontrado', status_code=404)

    db.session.delete(character)
    db.session.commit()
    response_body = {
           "msg": "Personaje eliminado con exito!"
        }
    return jsonify(response_body), 200
   




###################################################### inicio DELETE Planeta




@app.route('/planet/delete/<int:planet_id>', methods=['DELETE'])
def delete_planet(planet_id):

    planet = Planets.query.filter_by(id=planet_id).first()

    if planet is None:
        raise APIException('Planeta no encontrado', status_code=404)

    db.session.delete(planet)
    db.session.commit()
    response_body = {
           "msg": "Planeta eliminado con exito!"
        }
    return jsonify(response_body), 200
   




###################################################### inicio DELETE Bookmark




@app.route('/bookmark/delete/<int:bookmark_id>', methods=['DELETE'])
def delete_bookmark(bookmark_id):

    bookmark = Bookmarks.query.filter_by(id=bookmark_id).first()

    if bookmark is None:
        raise APIException('Favorito no encontrado', status_code=404)

    db.session.delete(bookmark)
    db.session.commit()
    response_body = {
           "msg": "Favorito eliminado con exito!"
        }
    return jsonify(response_body), 200





# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
jwt = JWTManager(app)


# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.
@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    query_user = Users.query.filter_by(username=username).first()
   
    if query_user is None:
        raise APIException('Usuario no encontrado', status_code=401)

    if username != query_user.username or password != query_user.password:
        return jsonify({"msg": "El nombre de usuario o la contraseña es incorrecta."}), 401

    access_token = create_access_token(identity=username)
    response_body = {
        "access_token": access_token,
        "user": query_user.serialize()
    }
    return jsonify(response_body) , 200


# Protect a route with jwt_required, which will kick out requests
# without a valid JWT present.
@app.route("/profile", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()

    query_user = Users.query.filter_by(username=current_user).first()
   
    if query_user is None:
        raise APIException('No tienes permitido estar aqui', status_code=401)

    response_body = {
        "user": query_user.serialize() 
    }
    return jsonify(response_body), 200



###################################################### ESTO VA AL FINAL

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

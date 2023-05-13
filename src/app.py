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
from models import db, User, People, Planet, Vehicles, Favorites

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
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



# MIS RUTAS
@app.route('/user', methods = ['GET'])            # app es nuestro flask, entre '' nombre d la ruta q voy ha llamar 
def get_users():                                # declarar func cn nombre descriptivo
    all_users=User.query.all()                  # crear var q cntiene info cn la q va a trabajar mi ruta ///
    all_users=list(map(lambda user:user.serialize(), all_users))  # mapeas all info that user return 

    return jsonify(all_users),200

@app.route('/user/<int:id>', methods = ['GET'])    
def get_user_by_id(id):
    user=User.query.get(id)

    return jsonify(user.serialize()),200

@app.route('/user', methods = ['POST'])
def create_user():
    data=request.get_json()
    new_user= User(data['email'], data['user_name'], data['first_name'], data['last_name'], data['password'])
    db.session.add(new_user)
    db.session.commit()

    return jsonify(new_user.serialize()),200

@app.route('/user/<int:id>',methods=['DELETE'])
def delete_user(id):
    user=User.query.get(id).first()
    db.session.remove(user)
    db.session.commit()
    return jsonify(user.serialize()),201

@app.route('/people',methods=['GET'])
def  get_people():
     all_people=People.query.all()
     all_people=list(map(lambda people:people.serialize(), all_people))

     return jsonify(all_people),200

@app.route('/people/<int:id>', methods=['DELETE'])
def delete_people(id):
    character=People.query.get(id).first()
    db.session.remove(character)
    db.session.commit()
    return jsonify(character.serialize()), 201

@app.route('/people', methods=['POST'])
def create_people():
    data=request.get_json()
    new_people= People(data['name'], data['birth_date'], data ['description'], data ['eye_color'], data ['hair_color'])
    db.session.add(new_people)
    db.session.commit()

    return jsonify(people.serialize()),200


@app.route('/people/<int:id>',methods=['GET']) 
def get_people_by_id(id):
    people=People.query.get(id)

    return jsonify(people.serialize()),200    

@app.route('/planet', methods= ['GET'])
def get_planet():
    all_planet=Planet.query.all() 
    all_planet=list(map(lambda planet:planet.serialize(), all_planet))  

    return jsonify(all_planet),200

@app.route('/planet/<int:id>',methods=['DELETE'])
def delete_planet(id):
    planet=planet.query.get(id).first()
    db.session.remove(planet)
    db.session.commit()

    return jsonify(planet.serialize()),201


@app.route('/planet',methods=['POST'])
def create_planet():
    data=request.get_json()
    new_planet= Planet(data['description'], data['name'], data['population'], data['terrain'], data['climate'])
    db.session.add(new_planet)
    db.session.commit()

    return jsonify(new_planet.serialize()),200    


@app.route('/planet/<int:id>',methods=['GET'])
def get_planet_by_id(id):
    planet:Planet.query.get(id)

    return jsonify(planet.serialize()),200    

@app.route('/vehicle', methods= ['GET'])
def get_vehicle():
    all_vehicle=Vehicle.query.all()
    all_vehicle=list(map(lambda vehicle:vehicle.serialize(), all_vehicle))

    return jsonify(all_vehicle),200


@app.route('/vehicle/<int:id>',methods=['DELETE'])
def delete_vehicle(id):
    vehicle=vehicle.query.get(id).first()
    db.session.remove(vehicle)
    db.session.commit()

    return jsonify(vehicle.serialize()),201


@app.route('/vehicle',methods=['POST'])
def create_vehicle():
    data=request.get_json()
    new_vehicle= User(data['model'], data['name'], data['description'], data['pilot'] )
    db.session.add(new_vehicle)
    db.session.commit()

    return jsonify(new_vehicle.serialize()),200    

@app.route('/vehicle/<int:id>',methods=['GET'])
def get_vehicle_by_id(id):
    vehicle:Vehicle.query.get(id)

    return jsonify(vehicle.serialize()),200   


@app.route('/favorite', methods= ['GET'])
def get_favorite():
    all_favorite=Favorite.query.all()
    all_favorite=list(map(lambda favorite:favorite.serialize(),all_favorite))

    return jsonify(all_favorite),200

@app.route('/favorite/people', methods=['POST'])
def new_favorite_people():
    data=request.get_json()
    new_favorite= People(data['name'],data ['birth_date'], data['description'] ,data['eye_color'] ,data ['hair_color'])
    db.session.add(new_favorite)
    db.session.commit()

    return jsonify(new_favorite.serialize()),200

@app.route('/favorite/planet', methods=['POST'])
def new_favorite_planet():
    data=request.get_json()
    new_favorite= Planet(data['name'],data ['population'], data['description'] ,data['terrain'] ,data ['climate'])
    db.session.add(new_favorite)
    db.session.commit()

    return jsonify(new_favorite.serialize()),200

@app.route('/favorite/vehicle', methods=['POST'])
def new_favorite_vehicle():
    data=request.get_json()
    new_favorite= Vehicle(data['name'],data ['model'], data['description'] ,data['pilot'])
    db.session.add(new_favorite)
    db.session.commit()

    return jsonify(new_favorite.serialize()),200


@app.route('/favorite/<int:id>',methods=['DELETE'])
def delete_favorite(id):
    favorite=favorite.query.get(id).first()
    db.sessionremove(id)
    db.session.commit()

    return jsonify(favorite.serialize()),201




@api.route("/signup", methods=["POST"])
def signup_user():

    try:

        body = request.json

        # Rellenar la tabla de la DB, con el registro de Usuario
        user_response = create_user(body)
        if user_response["code"] != 200:
            return jsonify(user_response)

        return jsonify(user_response), 200

    except Exception as error:
        print(error)
        return jsonify(user_response), user_response["code"]


@api.route("/users", methods=["GET"])
def users():

    try:

         # Obtener info de las tablas de la DB
        users_response = get_users()

        if users_response["code"] != 200:
            return jsonify(users_response)

        return jsonify(users_response["users"])

    except Exception as error:
        print(error)
        return jsonify(users_response), users_response["code"]

@api.route("/carers", methods=["GET"])
@jwt_required()
def carers():

    try:

         # Obtener info de las tablas de la DB
        users_response = get_carers()

        if users_response["code"] != 200:
            return jsonify(users_response)

        return jsonify(users_response["users_carers"])

    except Exception as error:
        print(error)
        return jsonify(users_response), users_response["code"]


@api.route("/users/<int:id>", methods=["GET","PUT","DELETE"])
def users_id(id):

    try:

        # Obtener, actualizar y borrar info de las tablas de la DB
        if request.method == "PUT":
            body = request.json
            user_response = update_user(body, id)

        if request.method == "GET":
            user_response = get_user(id)

        if request.method == "DELETE":
            user_response = delete_user(id)

        if user_response["code"] != 200:
            return jsonify(user_response)

        return jsonify(user_response)

    except Exception as error:
        print(error)
        return jsonify(user_response), user_response["code"]


###################################################################
# RUTAS PARA EL REGISTRO DE PERROS Y LAS PETICIONES DE DOG(S)/CRUD DESDE EL FRONT
@api.route("/signup-dog", methods=["POST"])
@jwt_required()
def signup_dog():

    try:

        body = request.json

        # Rellenar la tabla de la DB, con el registro de Perro
        dog_response = create_dog(body)
        if dog_response["code"] != 200:
            return jsonify(dog_response)

        return jsonify(dog_response), 200

    except Exception as error:
        print(error)
        return jsonify(dog_response), dog_response["code"]


@api.route("/dogs", methods=["GET"])
def dogs():

    try:

        # Obtener info de las tablas de la DB
        dogs_response = get_dogs()

        if dogs_response["code"] != 200:
            return jsonify(dogs_response)

        return jsonify(dogs_response["dogs"])

    except Exception as error:
        print(error)
        return jsonify(dogs_response), dogs_response["code"]


@api.route("/dogs/<int:id>", methods=["GET","PUT","DELETE"])
def dogs_id(id):

    try:

        # Obtener, actualizar y borrar info de las tablas de la DB
        if request.method == "PUT":
            body = request.json
            dog_response = update_dog(body, id)

        if request.method == "GET":
            dog_response = get_dog(id)

        if request.method == "DELETE":
            dog_response = delete_dog(id)

        if dog_response["code"] != 200:
            return jsonify(dog_response)

        return jsonify(dog_response)

    except Exception as error:
        print(error)
        return jsonify(dog_response), dog_response["code"]




from api.models import db, User
from flask_jwt_extended import create_access_token, get_jwt_identity
from api.checks.checks_user import check_user


# import requests
# import json 


def create_user(body):

    try:

        # checks_response = check_user(body)
        # if checks_response["code"] != 200:
        #     return checks_response["msg"]

        claves_user = body.keys()

        if not "email" in claves_user or not "password" in claves_user or not "name" in claves_user or not "lastName" in claves_user or not "address" in claves_user or not "province" in claves_user or not "postalCode" in claves_user or not "phone" in claves_user or not "country" in claves_user or not "birthdate" in claves_user:           # or not "latitude" in claves_user or not "longitude" in claves_user        
            return {"code": 400, "msg": "¡Información recibida en el Back insuficiente, falta información!"}


        # Crear un nuevo usuario en la base de datos
        new_user = User(
            email = body["email"],
            password = body["password"], 
            name = body["name"], 
            lastName = body["lastName"], 
            address = body["address"], 
            province = body["province"], 
            postalCode = int(body["postalCode"]), 
            phone = int(body["phone"]),
            country = body["country"], 
            birthdate = body["birthdate"],
            userPhoto = "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png",
            is_active = True)

            # latitude = int(body["latitude"]),
            # longitude = body["longitude"], 

        db.session.add(new_user)
        db.session.commit()
        
        # id_user = new_user.id

        return {"code": 200, "msg": "¡Usuario creado correctamente!" }         # "id": id_user # ID para rutas

    except Exception as error:
        print(error)
        return {"code": 500, "msg": "¡Error en el servidor, algo fue mal!"}


def get_users():

    try:
        
        # Obtener usuarios de la base de datos
        query = db.select(User).order_by(User.id)
        users = db.session.execute(query).scalars()

        user_list = [user.serialize() for user in users]

        return {"code": 200, "msg": "Usuarios existentes obtenidos", "users": user_list}

    except Exception as error:
        print(error)
        return {"code": 500, "msg": "¡Error en el servidor, algo fue mal!"}


    # users = db.session.execute(db.select(User.email).order_by(User.id)).scalars()
    # users = db.session.execute(db.select([User.name, User.email]).order_by(User.id)).scalars()

    # all_users = User.query.all()
    # # planet_serialized = [planet.serialize() for planet in all_planets] array comprehension
    # user_serialized = list(map(lambda user: user.serialize(), all_users))
    # response = {
    #     "result": {
    #         "planets": planet_serialized,
    #         "user": user_serialized
    #     }
    # }
    # return response, 200


def get_carers():

    try:

        sub_token = get_jwt_identity()
        user_id = sub_token["id"]
        
        # Obtener usuarios de la base de datos
        query = db.select(User).order_by(User.id)
        users = db.session.execute(query).scalars()

        users_carers_list = [user.serialize() for user in users if len(user.tariffs) != 0 ]

        users_carers_list_without_me = [user for user in users_carers_list if user["id"] != user_id ]

        return {"code": 200, "msg": "Usuarios existentes obtenidos", "users_carers": users_carers_list_without_me}

    except Exception as error:
        print(error)
        return {"code": 500, "msg": "¡Error en el servidor, algo fue mal!"}

# users_carers_list = list(filter(lambda user.serialize(): len(user.tariffs) != 0, users_carers_list))      # OTRA FORMA DE HACER UN FILTER


def get_user(id):

    try:
    
        # Obtener usuario de la base de datos
        user = db.get_or_404(User, id)
        # user = db.session.execute(db.select(User).filter_by(id)).scalars().one()
        
        return {"code": 200, "msg": "Usuario requerido obtenido", "user": user.serialize()}

    except Exception as error:
        print(error)
        return {"code": 500, "msg": "¡Error en el servidor, algo fue mal!"}


def update_me_user():

    try:

        sub_token = get_jwt_identity()
        user_id = sub_token["id"]
    
        # Obtener usuario de la base de datos
        user = db.get_or_404(User, user_id)

        access_token = create_access_token(identity=user.serialize())
        
        return {"code": 200, "msg": "¡Usuario actualizado correctamente!", "user": user.serialize(), "token": access_token}

    except Exception as error:
        print(error)
        return {"code": 500, "msg": "¡Error en el servidor, algo fue mal!"}


def update_user(body, id):

    try:
    
        # Obtener usuario de la base de datos
        user = db.get_or_404(User, id)

        claves_user = body.keys()

        if "password" in claves_user:
            user.password = body["password"]

        if "userPhoto" in claves_user:
            user.userPhoto = body["userPhoto"]
 
        # user.email = body["email"]        # ESTA DISABLED PARA CAMBIAR EN EL FRONT
        user.name = body["name"]
        user.lastName = body["lastName"]
        user.address = body["address"]
        user.province = body["province"]
        user.postalCode = int(body["postalCode"])
        user.phone = int(body["phone"])
        user.country = body["country"]
        user.birthdate = body["birthdate"]
        user.aboutMe = body.get("aboutMe", None)
        user.is_active = True

        # latitude = int(body["latitude"])
        # longitude = body["longitude"]

        db.session.commit()

        return {"code": 200, "msg": "¡Datos del usuario actualizados correctamente!", "user": user.serialize()}

    except Exception as error:
        print(error)
        return {"code": 500, "msg": "¡Error en el servidor, algo fue mal!"}


def delete_user(id):

    try:
    
        # Obtener usuarios de la base de datos
        user = db.get_or_404(User, id)

        db.session.delete(user)
        db.session.commit()

        # query = db.select(User).order_by(User.id)                 # SI DESPUES NECESITA UNA LISTA COMPLETA ACTUALIZADA
        # users = db.session.execute(query).scalars()


        return {"code": 200, "msg": "¡Usuario eliminado correctamente!"}

    except Exception as error:
        print(error)
        return {"code": 500, "msg": "¡Error en el servidor, algo fue mal!"}


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)


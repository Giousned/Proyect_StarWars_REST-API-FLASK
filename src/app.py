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
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from models import db, User, People, Planet, Vehicle, Favorites

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config["JWT_SECRET_KEY"] = "[}{*Super_Secreto_Holi-jeJE.*/*]"           # ¡Cambia las palabras "super-secret" por otra cosa!
jwt = JWTManager(app)

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



######################################################
# MIS RUTAS



# PERSONAJES
@app.route("/people", methods=["GET"])
def get_peoples():

    try:
        
        # Obtener personajes de la base de datos
        query = db.select(People).order_by(People.id)
        peoples = db.session.execute(query).scalars()

        peoples_list = [people.serialize() for people in peoples]

        # OTRA FORMA DE HACER Y OBTENER LOS PERSONAJES
        #  peoples=People.query.all()
        #  peoples=list(map(lambda people:people.serialize(), peoples))
        #  return jsonify(peoples),200

        return {"code": 200, "msg": "Personajes existentes obtenidos", "peoples": peoples_list}

    except Exception as error:
        print(error)
        return {"code": 500, "msg": "¡Error en el servidor, algo fue mal!"}


@app.route("/people/<int:id>", methods=["GET"])
def get_people(id):

    try:
    
        # Obtener personaje de la base de datos
        people = db.get_or_404(People, id)
        # people = db.session.execute(db.select(People).filter_by(id)).scalars().one()

        # OTRA FORMA DE HACER Y OBTENER EL PERSONAJE  
        # people=People.query.get(id)
        # return jsonify(people.serialize()),200  
        
        return {"code": 200, "msg": "Personaje requerido por id obtenido", "people": people.serialize()}

    except Exception as error:
        print(error)
        return {"code": 500, "msg": "¡Error en el servidor, algo fue mal!"}


# PLANETAS
@app.route("/planet", methods=["GET"])
def get_planets():

    try:
        
        # Obtener planetas de la base de datos
        query = db.select(Planet).order_by(Planet.id)
        planets = db.session.execute(query).scalars()

        planets_list = [planet.serialize() for planet in planets]

        return {"code": 200, "msg": "Planetas existentes obtenidos", "planets": planets_list}

    except Exception as error:
        print(error)
        return {"code": 500, "msg": "¡Error en el servidor, algo fue mal!"}


@app.route("/planet/<int:id>", methods=["GET"])
def get_planet(id):

    try:
    
        # Obtener planeta de la base de datos
        planet = db.get_or_404(Planet, id)
        # planet = db.session.execute(db.select(Planet).filter_by(id)).scalars().one()
        
        return {"code": 200, "msg": "Planeta requerido por id obtenido", "planet": planet.serialize()}

    except Exception as error:
        print(error)
        return {"code": 500, "msg": "¡Error en el servidor, algo fue mal!"}


# USUARIOS
@app.route("/users", methods=["GET"])
def get_users():

    try:
        
        # Obtener usuarios de la base de datos
        query = db.select(User).order_by(User.id)
        users = db.session.execute(query).scalars()

        users_list = [user.serialize() for user in users]

        return {"code": 200, "msg": "Usuarios existentes obtenidos", "users": users_list}

    except Exception as error:
        print(error)
        return {"code": 500, "msg": "¡Error en el servidor, algo fue mal!"}


# FAVORITOS DE UN USUARIO
@app.route("/users/favorites", methods=["GET"])
@jwt_required()
def get_users_favs():

    try:

        sub_token = get_jwt_identity()
        user_id = sub_token["id"]
        
        query = db.select(Favorites).filter_by(user_id).order_by(Favorites.id)
        favorites = db.session.execute(query).scalars()

        favorites_list = [favorites.serialize_favs_user() for favorites in favorites]

        return {"code": 200, "msg": "Favoritos existentes del usuario actual obtenidos", "favorites": favorites_list}

    except Exception as error:
        print(error)
        return {"code": 500, "msg": "¡Error en el servidor, algo fue mal!"}


# CREAR PLANETA FAVORITO A UN USUARIO
@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def create_planet_fav(planet_id):

    try:
    
        body = request.json
        # OTRA FORMA
        # data=request.get_json()

        new_planet_fav= Planet(
            body['name'],
            body['description'],
            body['population'],
            body['terrain'],
            body['climate'],
            planets_id = planet_id)

        db.session.add(new_planet_fav)
        db.session.commit()

        return {"code": 200, "msg": "¡Usuario creado correctamente!", "planet_fav": new_planet_fav.serialize() }
                # OTRA FORMA: jsonify(new_planet_fav.serialize()),200

    except Exception as error:
        print(error)
        return {"code": 500, "msg": "¡Error en el servidor, algo fue mal!"}



# CREAR PERSONAJE FAVORITO A UN USUARIO
@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def create_people_fav(people_id):

    try:
    
        body = request.json

        # SI QUEREMOS COMPROBAR QUE LLEGA TODA LA INFORMACION REQUERIDA EN EL BODY
        # claves_people = body.keys()

        # if not "name" in claves_people or not "birth_date" in claves_people or not "description" in claves_people or not "eye_color" in claves_people or not "hair_color" in claves_people:        
        #     return {"code": 400, "msg": "¡Información recibida en el Back insuficiente, falta información!"}

        new_people_fav= People(
            data['name'],
            data['birth_date'],
            data ['description'],
            data ['eye_color'],
            data ['hair_color'],
            peoples_id = people_id)

        db.session.add(new_people_fav)
        db.session.commit()

        return {"code": 200, "msg": "¡Usuario creado correctamente!", "people_fav": new_people_fav.serialize() }

    except Exception as error:
        print(error)
        return {"code": 500, "msg": "¡Error en el servidor, algo fue mal!"}



# ELIMINAR PLANETA FAVORITO POR ID
@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_planet_fav(planet_id):

    try:
    
        # Obtener usuarios de la base de datos
        planet_fav = db.get_or_404(Favorites, planet_id)

        db.session.delete(planet_fav)
        db.session.commit()

        # OTRA FORMA
        # planet_fav=Favorites.query.get(planet_id).first()
        # db.session.remove(planet_fav)


        # SI DESPUES NECESITAMOS UNA LISTA COMPLETA ACTUALIZADA
        # query = db.select(Favorites).order_by(Favorites.id)                 
        # favorites = db.session.execute(query).scalars()


        return {"code": 200, "msg": "¡Planeta favorito eliminado correctamente!"}

    except Exception as error:
        print(error)
        return {"code": 500, "msg": "¡Error en el servidor, algo fue mal!"}


# ELIMINAR PERSONAJE FAVORITO POR ID
@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_people_fav(people_id):

    try:
    
        # Obtener usuarios de la base de datos
        people_fav = db.get_or_404(Favorites, people_id)

        db.session.delete(people_fav)
        db.session.commit()

        return {"code": 200, "msg": "¡Personaje favorito eliminado correctamente!"}

    except Exception as error:
        print(error)
        return {"code": 500, "msg": "¡Error en el servidor, algo fue mal!"}


#########################################################################################


#########################
# EXTRA, NO OBLIGATORIO #
#########################

# CREAR PLANETA
@app.route('/planet', methods=['POST'])
def create_planet():

    try:
    
        body = request.json

        new_planet= Planet(
            body['name'],
            body['description'],
            body['population'],
            body['terrain'],
            body['climate'])

        db.session.add(new_planet)
        db.session.commit()

        return {"code": 200, "msg": "¡Planeta creado correctamente!", "planet": new_planet.serialize() }

    except Exception as error:
        print(error)
        return {"code": 500, "msg": "¡Error en el servidor, algo fue mal!"}


# CREAR PERSONAJE
@app.route('/people', methods=['POST'])
def create_people():

    try:
    
        body = request.json

        new_people= People(
            data['name'],
            data['birth_date'],
            data ['description'],
            data ['eye_color'],
            data ['hair_color'])

        db.session.add(new_people)
        db.session.commit()

        return {"code": 200, "msg": "¡Personaje creado correctamente!", "people": new_people.serialize() }

    except Exception as error:
        print(error)
        return {"code": 500, "msg": "¡Error en el servidor, algo fue mal!"}



# ACTUALIZAR PLANETA
@app.route('/planet/<int:id>', methods=['PUT'])
def update_planet(id):

    try:

        planet = db.get_or_404(Planet, id)
        

        body = request.json

        claves_planet = body.keys()


        planet.name = body['name']
        planet.description = body['description']
        planet.population = body['population']
        planet.terrain = body['terrain']
        planet.climate = body['climate']
 

        db.session.commit()

        return {"code": 200, "msg": "¡Datos del planeta actualizados correctamente!", "planet": planet.serialize()}

    except Exception as error:
        print(error)
        return {"code": 500, "msg": "¡Error en el servidor, algo fue mal!"}


# ELIMINAR PLANETA
@app.route('/planet/<int:id>', methods=['DELETE'])
def delete_planet(id):

    try:

        planet = db.get_or_404(Planet, id)
    

        db.session.delete(planet)
        db.session.commit()

        return {"code": 200, "msg": "¡Planeta eliminado correctamente!"}

    except Exception as error:
        print(error)
        return {"code": 500, "msg": "¡Error en el servidor, algo fue mal!"}




# EJEMPLO DE UNA MISMA FUNCION/RUTA QUE ADMITE VARIOS METODOS JUNTOS
# ACTUALIZAR O ELIMINAR PERSONAJE
@app.route('/people/<int:id>', methods=["PUT","DELETE"])
def put_or_delete_people(id):

    try:

        # Actualizar o borrar personajes de las tablas de la DB
        if request.method == "PUT":
            people = db.get_or_404(People, id)
        
            body = request.json
            claves_people = body.keys()

            people.name = body['name']
            people.description = body['description']
            people.population = body['population']
            people.terrain = body['terrain']
            people.climate = body['climate']
    

            db.session.commit()

            return {"code": 200, "msg": "¡Datos del personaje actualizados correctamente!", "people": people.serialize()}



        if request.method == "DELETE":
            people = db.get_or_404(People, id)
    
            db.session.delete(people)
            db.session.commit()

            return {"code": 200, "msg": "¡Personaje eliminado correctamente!"}

    except Exception as error:
        print(error)
        return jsonify(user_response), user_response["code"]





#########################
# MAS EXTRAS, EJEMPLOS  #
#########################



# EJEMPLOS DE FORMAS DE HACER FILTERS
# users_carers_list = [user.serialize() for user in users if len(user.tariffs) != 0 ]
# users_carers_list_without_me = [user for user in users_carers_list if user["id"] != user_id ]
# users_carers_list = list(filter(lambda user.serialize(): len(user.tariffs) != 0, users_carers_list))




# EJEMPLO PARA HACER LO MISMO CON LOS VEHICULOS Y LOS FAVORITOS DE LOS MISMOS
@app.route('/vehicle',methods=['POST'])
def create_vehicle():
    data = request.get_json()

    new_vehicle = User(data['model'], data['name'], data['description'], data['pilot'])

    db.session.add(new_vehicle)
    db.session.commit()

    return jsonify(new_vehicle.serialize()), 200    


@app.route('/favorite/vehicle', methods=['POST'])
def new_favorite_vehicle():
    data = request.get_json()

    new_favorite= Vehicle(data['name'], data['model'], data['description'], data['pilot'])

    db.session.add(new_favorite)
    db.session.commit()

    return jsonify(new_favorite.serialize()), 200





# EJEMPLO PARA HACER UN REGISTRO DE USUARIO LLAMANDO A UNA FUNCION QUE ESTÉ EN UN ARCHIVO CONTROLER APARTE
@app.route("/signup", methods=["POST"])
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



# ESTA SERIA LA FUNCION QUE ESTARÍA EN EL ARCHIVO CONTROLER APARTE Y QUE HABRÍA QUE IMPORTAR
def create_user(body):

    try:

        claves_user = body.keys()

        if not "email" in claves_user or not "password" in claves_user or not "name" in claves_user or not "userName" in claves_user or not "lastName" in claves_user:        
            return {"code": 400, "msg": "¡Información recibida en el Back insuficiente, falta información!"}


        # Crear un nuevo usuario en la base de datos
        new_user = User(
            email = body["email"],
            password = body["password"], 
            name = body["name"],
            user_name = body["userName"],
            last_name = body["lastName"],
            is_active = True)

        db.session.add(new_user)
        db.session.commit()
        
        # id_user = new_user.id

        return {"code": 200, "msg": "¡Usuario creado correctamente!" }         # "id": id_user # ID para rutas

    except Exception as error:
        print(error)
        return {"code": 500, "msg": "¡Error en el servidor, algo fue mal!"}







# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)


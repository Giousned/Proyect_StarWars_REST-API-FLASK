"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""

##############################
# OTRA FORMA DE HACER LA REST-API, HACIENDO PETICIONES FETCH/REQUESTS A UNA API Y COGIENDO LOS DATOS QUE TE DEVUELVE
##################################


import os
# INSTALAR MODULO REQUESTS PARA PODER HACER PETICIONES A API, COMO FETCH EN JS
# python3 -m pip install requests
# LO NECESITO DESPUES DE INSTALAR EL MODULO REQUESTS PARA IMPORTARLO
import sys
sys.path.append("/home/gitpod/.pyenv/versions/3.10.7/lib/python3.10/site-packages")
import requests

from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User
from models import People, Planet, Vehicles, Favorites

app_DB = Flask(__name__)
app_DB.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app_DB.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app_DB.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app_DB.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app_DB, db)
db.init_app_DB(app_DB)
CORS(app_DB)
setup_admin(app_DB)

# Handle/serialize errors like a JSON object
@app_DB.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app_DB.route('/')
def sitemap():
    return generate_sitemap(app)

@app_DB.route('/people', methods=['GET'])
def get_peoples():

    url = 'https://www.swapi.tech/api/people'
    headers = {"Content-Type": "application/json"}
    response = requests.get(url)

    response_body = response.json()

    return jsonify(response_body["results"]), 200

@app_DB.route('/people/<int:people_id>', methods=['GET'])
def get_one_people(people_id):

    url = 'https://www.swapi.tech/api/people/'+str(people_id)       #  NO SE HACERLO CON /people/{people_id}
    headers = {"Content-Type": "application/json"}
    response = requests.get(url)

    response_body = response.json()

    return jsonify(response_body["result"]), 200

@app_DB.route('/planets', methods=['GET'])
def get_planets():

    url = 'https://www.swapi.tech/api/planets'
    headers = {"Content-Type": "application/json"}
    response = requests.get(url)

    response_body = response.json()

    return jsonify(response_body["results"]), 200

@app_DB.route('/planets/<int:planet_id>', methods=['GET'])
def get_one_planet(planet_id):

    url = 'https://www.swapi.tech/api/planets/'+str(planet_id)
    headers = {"Content-Type": "application/json"}
    response = requests.get(url)

    response_body = response.json()

    return jsonify(response_body["result"]), 200

@app_DB.route('/vehicles', methods=['GET'])
def get_vehicles():

    url = 'https://www.swapi.tech/api/vehicles'
    headers = {"Content-Type": "application/json"}
    response = requests.get(url)

    response_body = response.json()

    return jsonify(response_body["results"]), 200

@app_DB.route('/vehicles/<int:vehicle_id>', methods=['GET'])
def get_one_vehicle(vehicle_id):

    url = 'https://www.swapi.tech/api/vehicles/'+str(vehicle_id)
    headers = {"Content-Type": "application/json"}
    response = requests.get(url)

    response_body = response.json()

    return jsonify(response_body["result"]), 200

@app_DB.route('/starships', methods=['GET'])
def get_starships():

    url = 'https://www.swapi.tech/api/starships'
    headers = {"Content-Type": "application/json"}
    response = requests.get(url)

    response_body = response.json()

    return jsonify(response_body["results"]), 200

@app_DB.route('/starships/<int:starship_id>', methods=['GET'])
def get_one_starship(starship_id):

    url = 'https://www.swapi.tech/api/starships/'+str(starship_id)
    headers = {"Content-Type": "application/json"}
    response = requests.get(url)

    response_body = response.json()

    return jsonify(response_body["result"]), 200

@app_DB.route('/species', methods=['GET'])
def get_species():

    url = 'https://www.swapi.tech/api/species'
    headers = {"Content-Type": "application/json"}
    response = requests.get(url)

    response_body = response.json()

    return jsonify(response_body["results"]), 200

@app_DB.route('/species/<int:specie_id>', methods=['GET'])
def get_one_specie(specie_id):

    url = 'https://www.swapi.tech/api/species/'+str(specie_id)
    headers = {"Content-Type": "application/json"}
    response = requests.get(url)

    response_body = response.json()

    return jsonify(response_body["result"]), 200


##########
# ADICIONALMENTE: USER:
@app_DB.route('/users', methods=['GET'])
def get_users():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app_DB.route('/users/favorites', methods=['GET'])
def get_user_favorites():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app_DB.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def post_planet_favorite():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app_DB.route('/favorite/people/<int:people_id>', methods=['POST'])
def post_people_favorite():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app_DB.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_planet_favorite():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app_DB.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_people_favorite():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200


# this only runs if `$ python src/app_DB.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app_DB.run(host='0.0.0.0', port=PORT, debug=False)




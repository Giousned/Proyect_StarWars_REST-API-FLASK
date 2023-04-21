"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
##############################
# OTRA FORMA DE HACER LA REST-API, CON UNA DB DONDE YO INTRODUZCO LOS DATOS
##################################

import os
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
    return generate_sitemap(app_DB)

@app_DB.route('/user',methods= ['GET'])#app es nuestro flask,entre '' nombre d la ruta q voy ha llamar 
def get_users():            #declarar func cn nombre descriptivo
    all_users=User.query.all()  #crear var q cntiene info cn la q va a trabajar mi ruta ///
    all_users=list(map(lambda user:user.serialize(),all_users))  #mapeas all info that user return 

    return jsonify(all_users),200

@app_DB.route('/user/<int:id>',methods=['GET'])    
def get_user_by_id(id):
    user=User.query.get(id)

    return jsonify(user.serialize()),200

@app_DB.route('/user',methods=['POST'])
def create_user():
    data=request.get_json()
    new_user= User(data['email'],data['user_name'] ,data['first_name'] ,data['last_name'] ,data['password'] )
    db.session.add(new_user)
    db.session.commit()

    return jsonify(new_user.serialize()),200

@app_DB.route('/people',methods=['GET'])
def  get_people():
     all_people=People.query.all()
     all_people=list(map(lambda people:people.serialize(), all_people))

     return jsonify(all_people),200

@app_DB.route('/people', methods=['POST'])
def create_people():
    data=request.get_json()
    new_people= People(data['name'],data['birth_date'],data ['description'],data ['eye_color'],data ['hair_color'])
    db.session.add(new_people)
    db.session.commit()

    return jsonify(people.serialize()),200


@app_DB.route('/people/<int:id>',methods=['GET']) 
def get_people_by_id(id):
    people=People.query.get(id)

    return jsonify(people.serialize()),200    

@app_DB.route('/planet', methods= ['GET'])
def get_planet():
    all_planet=Planet.query.all() 
    all_planet=list(map(lambda planet:planet.serialize(), all_planet))  

    return jsonify(all_planet),200

@app_DB.route('/planet',methods=['POST'])
def create_planet():
    data=request.get_json()
    new_planet= Planet(data['description'],data['name'] ,data['population'] ,data['terrain'] ,data['climate'] )
    db.session.add(new_planet)
    db.session.commit()

    return jsonify(new_planet.serialize()),200    


@app_DB.route('/planet/<int:id>',methods=['GET'])
def get_planet_by_id(id):
    planet:Planet.query.get(id)

    return jsonify(planet.serialize()),200    

@app_DB.route('/vehicle', methods= ['GET'])
def get_vehicle():
    all_vehicle=Vehicle.query.all()
    all_vehicle=list(map(lambda vehicle:vehicle.serialize(), all_vehicle))

    return jsonify(all_vehicle),200


@app_DB.route('/vehicle',methods=['POST'])
def create_vehicle():
    data=request.get_json()
    new_vehicle= User(data['model'],data['name'] ,data['description'] ,data['pilot'] )
    db.session.add(new_vehicle)
    db.session.commit()

    return jsonify(new_vehicle.serialize()),200    

@app_DB.route('/vehicle/<int:id>',methods=['GET'])
def get_vehicle_by_id(id):
    vehicle:Vehicle.query.get(id)

    return jsonify(vehicle.serialize()),200   


@app_DB.route('/favorite', methods= ['GET'])
def get_favorite():
    all_favorite=Favorite.query.all()
    all_favorite=list(map(lambda favorite:favorite.serialize(),all_favorite))

    return jsonify(all_favorite),200



# this only runs if `$ python src/app_DB.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app_DB.run(host='0.0.0.0', port=PORT, debug=False)


from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    user_name = db.Column(db.String(40),nullable=False)
    last_name = db.Column(db.String(50),nullable=False)
    register_data = db.Column(db.DateTime, default = datetime.datetime.utcnow) # CONSULTAR 

    favorites = db.relationship("Favorites", back_populates = 'user')    # relacion entre clases  1 a N = multiples favoritos,

    def __repr__(self):
        return '<User %r>' % self.user_name  # con esta forma en la bd pinta el self que queramos en esta caso el nombre de usuario en vez de poner  <User 1 por ejemplo>


    def __init__(self, email, user_name, last_name, password):  #inicio las columnas que quiero, son los datos que introduciré 
        self.email = email
        self.user_name = user_name
        self.last_name = last_name
        self.password = password   
        self.is_active = True  
        # self.favorites = favorites.serialize() CONSULTAR
        

    def serialize(self):  #transformo a diccionario  los datos para ver una respuesta JSON /enviar a JSON
        return {
            "id": self.id,
            "email": self.email,
            "user_name":self.user_name,
            "last_name":self.last_name,
            "favorites": list(map(lambda favorite: favorite.serialize(), self.favorites))
            # do not serialize the password, its a security breach
        }
    
    def serialize_user(self):  #transformo a diccionario  los datos para ver una respuesta JSON /enviar a JSON
        return {
            "id": self.id,
            "user_name":self.user_name,
            # do not serialize the password, its a security breach
        }


class People(db.Model):
    __tablename__ = 'People'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    birth_date = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.String(120), unique=True, nullable=False)
    eye_color = db.Column(db.String(120), unique=True, nullable=False)
    hair_color = db.Column(db.String(120), unique=True, nullable=False)

    planet_id = db.Column(db.Integer, db.ForeignKey("Planet.id")) #relacion de tabla.id

    planet = db.relationship("Planet", back_populates = 'people') #relacion entre clases 
    favorites = db.relationship("Favorites", back_populates = 'favorites')
    vehicle = db.relationship("Vehicle", back_populates = 'people')


    def __repr__(self):
        return '<People %r>' % self.name

    def __init__(self, name, birth_date, description, eye_color, hair_color):
        self.name = name
        self.birth_date = birth_date
        self.description = description
        self.eye_color = eye_color
        self.hair_color = hair_color

    def serialize(self):
        return{
            "id": self.id,
            "name":self.name,
            "birth_date":self.birth_date,
            "description":self.description,
            "eye_color":self.eye_color,
            "hair_color":self.hair_color,
            "planet": self.planet.serialize_planet(),
        }

    def serialize_people(self):
         return{
            "id": self.id,
            "name":self.name,
            "description":self.description,
        }


class Planet(db.Model):
    __tablename__ = 'Planet'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.String(120), unique=True, nullable=False)
    population = db.Column(db.Integer)
    terrain = db.Column(db.String(120), unique=True, nullable=False)
    climate = db.Column(db.String(120), unique=True, nullable=False)

    favorites = db.relationship("Favorites", back_populates = 'favorites')
    people = db.relationship("People", back_populates = 'planet')

    def __repr__(self):
        return '<Planet %r>' % self.name
    
    def __init__(self,name,description,population,terrain,climate):
        self.name = name
        self.description = description
        self.population = population
        self.terrain = terrain
        self.climate = climate

    def serialize(self):
        return {
          "id": self.id,
          "name":self.name,
          "description":self.description,
          "population":self.population,
          "terrain": self.terrain,
          "climate":self.climate, 
        }
    
    def serialize_planet(self):
        return {
          "id": self.id,
          "name":self.name,
          "descirption":self.description,
          "population":self.population,
        }


class Vehicle(db.Model):
    __tablename__ = 'Vehicle'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.String(120), unique=True, nullable=False)
    model = db.Column(db.String(120), unique=True, nullable=True)

    pilots =  db.Column(db.Integer, db.ForeignKey("People.id")) 

    people = db.relationship("People", back_populates = 'vehicle')
    favorites = db.relationship("Favorites", back_populates = 'vehicles')

    def __repr__(self):
        return '<Vehicles %r>' % self.name

    def __init__(self, name, description, model, pilots):
        self.name = name
        self.description = description
        self.model = model
        self.pilots = pilots
     
    def serialize(self):
        return {
          "id": self.id,
          "name":self.name,
          "description":self.description,
          "model": self.model,
          "people":self.people.serialize_people() #hace referencia a quien conduce el coche, muestra los datos del conductor en este caso es la persona
        }

    def serialize_vehicle(self):
         return {
          "id": self.id,
          "name":self.name,   
        }


class Favorites(db.Model):
    __tablename__ = 'Favorites'
    id = db.Column(db.Integer,primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("User.id"))
    planets_id = db.Column(db.Integer,db.ForeignKey("Planet.id"))          #nombre de la table + id
    people_id = db.Column(db.Integer, db.ForeignKey("People.id"))
    vehicles_id = db.Column(db.Integer, db.ForeignKey("Vehicle.id"))

    user = db.relationship("User", back_populates = "favorites") ##union de clases y tabla    #relacion class y unir tablas- inner join                           #relacion entre las class 
    planet = db.relationship("Planet", back_populates = "favorites")
    people = db.relationship("People", back_populates = "favorites") #insertar en la tabla favoritos las clases 
    vehicle = db.relationship("Vehicle", back_populates = "favorites")
    

    def __init__(self, user_id, planets_id, people_id, vehicles_id):
        self.user_id = user_id
        self.planets_id = planets_id
        self.people_id = people_id
        self.vehicles_id = vehicles_id

    def serialize(self):
      return {
         "id":self.id,
         "user_id":self.user_id,
         "people_id":self.people_id,
         "planet_id":self.planets_id,
         "vehicles_id":self.vehicles_id
        }
    
    # def serialize_favs_user(self):
    #   return {
    #      "id":self.id,
    #      "people_id":self.people_id,
    #      "planet_id":self.planets_id,
    #      "vehicles_id":self.vehicles_id
    #     }
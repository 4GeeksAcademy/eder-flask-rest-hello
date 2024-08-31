from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

""" import datetime 

now = datetime.datetime.now(datetime.timezone.utc) """

db = SQLAlchemy()

class User(db.Model):    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120),unique=True,nullable=False)
    fullname = db.Column(db.String(120),nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80),  nullable=False)
    is_active = db.Column(db.Boolean(),  nullable=False)
    created = db.Column(db.DateTime(timezone=True),server_default=func.now(),nullable=True)
    favorite = db.relationship('Favorite',backref="user",lazy=True)

    def __repr__(self):
        return '<User %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "username":self.username,
            "email": self.email,
            "created_at": self.created,            
            # do not serialize the password, its a security breach
        }
    
class Planet(db.Model):
    planetID=db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(120),unique=True,nullable=False)
    diameter = db.Column(db.String(120),nullable=False)
    rotation_period = db.Column(db.String(120),nullable=False)
    orbital_period = db.Column(db.String(120),nullable=False)
    gravity = db.Column(db.String(120),nullable=False)
    population = db.Column(db.String(120),nullable=False)
    climate = db.Column(db.String(120),nullable=False)
    terrain = db.Column(db.String(120),nullable=False)
    surface_water = db.Column(db.String(120),nullable=False)
    created = db.Column(db.DateTime(timezone=True),server_default=func.now(),nullable=False)
    favorite = db.relationship('Favorite',backref='planet',lazy=True)

        
    def __repr__(self):
        return '<Planet %r>' % self.planetID

    def serialize(self):
        return {
            "id": self.planetID,
            "name":self.username,
            "diameter":self.diameter,
            "rotation_period":self.rotation_period,
            "orbital_period":self.orbital_period,
            "gravity":self.gravity,
            "population":self.population,
            "climate":self.climate,
            "terrain":self.terrain,
            "surface_water":self.surface_water,                
            
        }

class Vehicle(db.Model):
    vehicleID = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(120),nullable=False)
    model = db.Column(db.String(120),nullable=False)
    vehicles_class = db.Column(db.String(120),nullable=False)
    manufacturer = db.Column(db.String(120),nullable=False)
    lenght = db.Column(db.String(120),nullable=False)
    cost = db.Column(db.String(120),nullable=False)
    max_speed = db.Column(db.String(120),nullable=False)
    cargo_capacity = db.Column(db.String(120),nullable=False)
    consumable = db.Column(db.String(120),nullable=False)    
    created=db.Column(db.DateTime(timezone=True),server_default=func.now(),nullable=False)
    favorite = db.relationship('Favorite',backref='vehicle',lazy=True)

    
    def __repr__(self):
        return '<Vehicle %r>' % self.vehicleId

    def serialize(self):
        return {
            "id": self.vehicleId,
            "name":self.name,
            "model":self.model,
            "class":self.vehicles_class,
            "manufacturer":self.manufacturer,
            "lenght":self.lenght,
            "cost_credits": self.cost,
            "max_speed": self.max_speed,
            "cargo_capacity":self.cargo_capacity,
            "consumables":self.consumable,                       
            # do not serialize the password, its a security breach
        }
  
class People(db.Model):
    peopleID = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(120),unique=True,nullable=False)
    birth_year = db.Column(db.String(120),nullable=False)
    eye_color = db.Column(db.String(120),nullable=False)
    gender = db.Column(db.String(120),nullable=False)
    hair_color = db.Column(db.String(120),nullable=False)
    height = db.Column(db.String(120),nullable=False)
    mass = db.Column(db.String(120),nullable=False)
    skin_color = db.Column(db.String(120),nullable=False)
    homeworld = db.Column(db.String(120),nullable=False)    
    created = db.Column(db.DateTime(timezone=True),server_default=func.now(),nullable=False)
    favorite = db.relationship('Favorite',backref='people',lazy=True)

    def __repr__(self):
        return '<People %r>' % self.peopleID

    def serialize(self):
        return {
            "id": self.peopleID,
            "name":self.name,
            "birth_year":self.birth_year,
            "eye_color":self.eye_color,
            "gender":self.gender,
            "hair_color":self.hair_color,
            "height":self.height,
            "mass":self.mass,
            "skin_color":self.skin_color,
            "homeworld":self.homeworld,                             
            # do not serialize the password, its a security breach
        }

class Favorite(db.Model):
    favoriteID = db.Column(db.Integer,primary_key=True)
    people_id = db.Column(db.Integer,db.ForeignKey('people.peopleID'))
    vehicle_id = db.Column(db.Integer,db.ForeignKey('vehicle.vehicleID'))
    planet_id = db.Column(db.Integer,db.ForeignKey('planet.planetID'))
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Favorite %r>' % self.favoriteID

    def serialize(self):
        return {
            "id": self.favoriteID,
            "people_id":self.people_id,
            "vehicle_id":self.vehicle_id,
            "planet_id":self.planet_id                                      
            # do not serialize the password, its a security breach
        }





    

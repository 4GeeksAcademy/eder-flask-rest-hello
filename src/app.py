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
from models import db, User,People,Vehicle,Favorite,Planet
from flask_sqlalchemy import SQLAlchemy
#from models import Person

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


""" ENDPOINTS """

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


""" USER ENDPOINT """

@app.route('/users', methods=['GET'])
def get_all_users():
    query_users = db.session.query(User).all()
    try:
        if query_users == None:
            return jsonify({"msg":"There are no users registered yet"}),404
        else:
            result = list((map(lambda item:item.serialize(),query_users)))
            return jsonify(result),200
    except Exception as err:
        return jsonify({"error":"There was an unexpected error","msg":str(err)}),500        

@app.route('/users/<int:id_user>',methods=['GET'])
def get_specific_user(id_user):
    query_user = db.session.query(User).get_or_404(id_user,f'Sorry there is no user with id "{id}" registered')
    result = query_user.serialize()
    return jsonify(result),200
 




""" FAVORITE ENDPOINT """

@app.route('/users/favorites/<int:id_user>',methods=['GET'])
def get_user_favorites(id_user):
    query_favorites = db.session.query(Favorite).filter_by(user_id=id_user).all()
    try:
        if query_favorites is None:
            return jsonify({"msg":"This user has no favorties"}),404
        else:
            result = list(map(lambda item: item.serialize(),query_favorites))
            return jsonify(result),200

    except Exception as err:
        return jsonify({"error":"There was an unexpected error","msg":str(err)}),500

@app.route('/favorites/<int:id_user>/planets/<int:id_planet>',methods=['POST'])
def post_user_favorite_planet(id_user,id_planet):
    db.session.query(User).get_or_404(id_user,f'There is no user with id "{id_user}"')
    db.session.query(Planet).get_or_404(id_planet,f'There is no Planet with id "{id_planet}"')
    try:
        query_favorite = db.session.query(Favorite).filter_by(user_id = id_user, planet_id = id_planet).first()
        if query_favorite is not None:
            return jsonify({"msg":"This Planet has been already added to favorites"}),404
        else:
            favorite = Favorite(vehicle_id=None, people_id=None, planet_id = id_planet, user_id =id_user)
        db.session.add(favorite)
        db.session.commit()
        return jsonify({"msg":"Done"}),201            
    except SQLAlchemy as err:
        return jsonify({"error":"There was an unexpected error","msg":str(err)})
    

@app.route('/favorites/<int:id_user>/people/<int:id_people>',methods=['POST'])
def post_user_favorite_people(id_user,id_people):
    db.session.query(User).get_or_404(id_user,f'There is no user with id "{id_user}"')
    db.session.query(People).get_or_404(id_people,f'There is no Planet with id "{id_people}"')
    try:
        query_favorite = db.session.query(People).filter_by(user_id=id_user,people_id = id_people).first()
        if query_favorite is not None:
            return jsonify({"msg":"This Character has been already added to favorites"}),404
        else:
            favorite = Favorite(vehicle_id=None,planet_id=None,people_id = id_people, user_id =id_user)
            db.session.add(favorite)
            db.session.commit()
            return jsonify({"msg":"Done"}),201
    except SQLAlchemy as err:
         return jsonify({"error":"There was an unexpected error","msg":str(err)})

           
@app.route('/favorites/<int:id_user>/vehicles/<int:id_vehicle>',methods=['POST'])
def post_user_favorite_vehicle(id_user,id_vehicle):
    db.session.query(User).get_or_404(id_user,f'There is no user with id "{id_user}"')
    db.session.query(Vehicle).get_or_404(id_vehicle,f'There is no Planet with id "{id_vehicle}"')
    try:
        query_favorite = db.session.query(Vehicle).filter_by(user_id = id_user, vehicle_id = id_vehicle)
        if query_favorite is not None:
            return jsonify({"msg":"This Vehicle has been already added to favorites"}),404
        else:
            favorite = Favorite(people_id=None,planet_id=None,vehicle_id = id_vehicle, user_id =id_user)
            db.session.add(favorite)
            db.session.commit()
            return jsonify({"msg":"Done"}),201
    except SQLAlchemy as err:
        return jsonify({"error":"There was an unexpected error","msg":str(err)})
          

@app.route('/favorites/<int:id_user>/planets/<int:id_planet>',methods=['DELETE'])
def delete_user_favorite_planet(id_user,id_planet):
    db.session.query(User).get_or_404(id_user,f'There is no user with id "{id_user}"')
    db.session.query(Planet).get_or_404(id_planet,f'There is no Planet with id "{id_planet}"')
    to_delete =  db.session.query(Favorite).filter_by(user_id = id_user, planet_id = id_planet).first()      
    try:
        if to_delete is None:
            return jsonify({"msg":"There was no element to delete"}),404
        else:
            db.session.delete(to_delete)
            db.session.commit()
            return jsonify({"msg":"Element was deleted"}),204
    except Exception as err: 
        return jsonify({"error":"There was an unexpected error","msg":str(err)}),500
    
@app.route('/favorites/<int:id_user>/people/<int:id_people>',methods=['DELETE'])
def delete_user_favorite_people(id_user,id_people):
    db.session.query(User).get_or_404(id_user,f'There is no user with id "{id_user}"')
    db.session.query(People).get_or_404(id_people,f'There is no Planet with id "{id_people}"')
    to_delete =  db.session.query(Favorite).filter_by(user_id = id_user, people_id = id_people).first()      
    try:
        if to_delete is None:
            return jsonify({"msg":"There was no element to delete"}),404
        else:
            db.session.delete(to_delete)
            db.session.commit()
            return jsonify({"msg":"Element was deleted"}),204
    except Exception as err: 
        return jsonify({"error":"There was an unexpected error","msg":str(err)}),500

@app.route('/favorites/<int:id_user>/vehicles/<int:id_vehicle>',methods=['DELETE'])
def delete_user_favorite_vehicle(id_user,id_vehicle):
    db.session.query(User).get_or_404(id_user,f'There is no user with id "{id_user}"')
    db.session.query(Vehicle).get_or_404(id_vehicle,f'There is no Planet with id "{id_vehicle}"')
    to_delete =  db.session.query(Favorite).filter_by(user_id = id_user, vehicle_id = id_vehicle).first()      
    try:
        if to_delete is None:
            return jsonify({"msg":"There was no element to delete"}),404
        else:
            db.session.delete(to_delete)
            db.session.commit()
            return jsonify({"msg":"Element was deleted"}),204
    except Exception as err: 
        return jsonify({"error":"There was an unexpected error","msg":str(err)}),500

""" PEOPLE ENDPOINTS """

@app.route('/people', methods=['GET'])
def get_all_people():
    query_result = People.query.all()
    try:
     if query_result == None:
         return jsonify({"msg":"There are no characters in the list"}),404
     else: 
        result = list(map(lambda item: item.serialize(),query_result))     
        return jsonify(result), 200  
        
    except Exception as err:
        return ({"error":"There was an unexpected error","msg":str(err)})
    
@app.route('/people/<int:id>',methods=['GET'])
def get_specific_people(id):
    query_people = People.query.get_or_404(id,f'There was no Character with id "{id}"')    
    result = query_people.serialize()   
    return jsonify(result),200
    
@app.route('/people',methods=['POST'])
def post_new_people():
    data = request.get_json()       
    required = {"name","birth_year","eye_color","gender","hair_color","height","mass","skin_color","homeworld"}

    for item in required:
        if item not in data or not data[item]:
            return jsonify({"msg":"All fields are required! Check if one or more are empty!"}),400

    try:
        name = request.json.get("name")  
        query_people = db.session.query(People).filter_by(name = name).first()
        if query_people is not None:
            return jsonify({"msg":"Character with the same name already exists"}),400
        else:
            new_character = People( name = data["name"], birth_year = data["birth_year"],eye_color = data["eye_color"], gender = data["gender"], hair_color = data["hair_color"], height = data["height"], mass = data["mass"], skin_color = data["skin_color"],homeworld = data["homeworld"])
            db.session.add(new_character)
            db.session.commit()
            return jsonify({"msg":"New Character was added successfully"}),201

    except SQLAlchemy as err:
        return jsonify({"error":"There was an unexpected error","msg":str(err)})




""" PLANETS ENDPOITS """


@app.route('/planets',methods=['GET'])
def get_all_planets():
    """ query_planets2 =  Planet.query.all() """
    """ SON EQUIVALENTES """
    query_planets = db.session.query(Planet).all()  

    try:
        if query_planets == None:
            return jsonify({"msg":"There are no planets registered yet"}),404
        else: 
            result = list(map(lambda item: item.serialize(),query_planets))
            return jsonify(result),200
    except Exception as err:
        return jsonify({"error":"There was an unexpected error","error":str(err)}),500
    
   
@app.route('/planets/<int:id>',methods=['GET'])
def get_specific_planet(id):
    query_planet = db.session.query(Planet).get_or_404(id,f'Sorry there is no planet with id "{id}" registered')
    result = query_planet.serialize()
    return jsonify(result),200

@app.route('/planets',methods=['POST'])
def post_new_planet():
    data = request.get_json()       
    required = {"name","diameter","rotation_period","orbital_period","gravity","population","climate","terrain","surface_water"}

    for item in required:
        if item not in data or not data[item]:
            return jsonify({"msg":"All fields are required! Check if one or more are empty!"}),400

    try:
        name = request.json.get("name")  
        query_planet = db.session.query(Planet).filter_by(name = name).first()
        if query_planet is not None:
            return jsonify({"msg":"Character with the same name already exists"}),400
        else:
            new_planet = Planet( name = data["name"], diameter = data["diameter"],rotation_period = data["rotation_period"], orbital_period = data["orbital_period"], gravity = data["gravity"], population = data["population"], climate = data["climate"], terrain = data["terrain"],surface_water = data["surface_water"])
            db.session.add(new_planet)
            db.session.commit()
            return jsonify({"msg":"New Planet was added successfully"}),201

    except SQLAlchemy as err:
        return jsonify({"error":"There was an unexpected error","msg":str(err)})



""" VEHICLE ENDPOINTS """

@app.route('/vehicles',methods=['GET'])
def get_all_vehicles():
    query_vehicles = db.session.query(Vehicle).all()
    try:
        if query_vehicles == None:
            return jsonify({"msg":"There are no vehicles registered yet"}),404
        else: 
            result = list(map(lambda item: item.serialize(),query_vehicles))
            return jsonify(result),200
    except Exception as err:
        return jsonify({"error":"There was an unexpected error","msg":str(err)}),500

@app.route('/vehicles/<int:vehicle_id>',methods=['GET'])
def get_specific_vehicle(vehicle_id):
    query_vehicle = db.session.query(Vehicle).get_or_error_404(vehicle_id,f'There was no Vehicle with id "{vehicle_id}"')
    result = query_vehicle.serialize()
    return jsonify(result),200


@app.route('/vehicles',methods=['POST'])
def post_new_vehicle():
    data = request.get_json()       
    required = {"name","model","vehicle_class","manufacturer","lenght","cost_credits","max_speed","cargo_capacity","consumable"}

    for item in required:
        if item not in data or not data[item]:
            return jsonify({"msg":"All fields are required! Check if one or more are empty!"}),400

    try:
        name = request.json.get("name")  
        query_vehicle = db.session.query(Vehicle).filter_by(name = name).first()
        if query_vehicle is not None:
            return jsonify({"msg":"Vehicle with the same name already exists"}),400
        else:
            new_vehicle = Vehicle( name = data["name"], model = data["model"], vehicle_class= data["vehicle_class"], manufacturer = data["manufacturer"], lenght = data["lenght"], cost_credits = data["cost_credits"], max_speed = data["max_speed"], cargo_capacity = data["cargo_capacity"],consumable = data["consumable"])
            db.session.add(new_vehicle)
            db.session.commit()
            return jsonify({"msg":"New Vehicle was added successfully"}),201

    except SQLAlchemy as err:
        return jsonify({"error":"There was an unexpected error","msg":str(err)})






# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

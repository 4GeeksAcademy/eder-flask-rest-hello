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
            return({"msg":"There are no users registered yet"}),404
        else:
            result = list((map(lambda item:item.serialize(),query_users)))
            return jsonify(result),200
    except Exception as err:
        return({"error":"There was an unexpected error","msg":str(err)}),500        

@app.route('/users/<int:user_id>',methods=['GET'])
def get_specific_user(user_id):
    query_user = db.session.query(User).get_or_404(user_id,f'Sorry there is no user with id "{id}" registered')
    result = query_user.serialize()
    return jsonify(result),200
 

""" FAVORITE ENDPOINT """
@app.route('/users/favorites/<int:id_user>',methods=['GET'])
def get_user_favorites(id_user):
    query_favorites = db.session.query(Favorite).filter_by(user_id=id_user).all()
    try:
        if query_favorites is None:
            return({"msg":"This user has no favorties"}),404
        else:
            result = list(map(lambda item: item.serialize(),query_favorites))
            return jsonify(result),200

    except Exception as err:
        return({"error":"There was an unexpected error","msg":str(err)}),500

@app.route('/favorites/<int:id_user>/planets/<int:id_planet>',methods=['POST'])
def post_user_favorite_planet(id_user,id_planet):
    db.session.query(User).get_or_404(id_user,f'There is no user with id "{id_user}"')
    db.session.query(Planet).get_or_404(id_planet,f'There is no Planet with id "{id_planet}"')
    favorite = Favorite(vehicle_id=None,people_id=None,planet_id = id_planet, user_id =id_user)
    db.session.add(favorite)
    db.session.commit()
    return ({"msg":"Done"}),201;

@app.route('/favorites/<int:id_user>/people/<int:id_people>',methods=['POST'])
def post_user_favorite_people(id_user,id_people):
    db.session.query(User).get_or_404(id_user,f'There is no user with id "{id_user}"')
    db.session.query(People).get_or_404(id_people,f'There is no Planet with id "{id_people}"')
    favorite = Favorite(vehicle_id=None,planet_id=None,people_id = id_people, user_id =id_user)
    db.session.add(favorite)
    db.session.commit()
    return jsonify({"msg":"Done"}),201;
           
@app.route('/favorites/<int:id_user>/vehicles/<int:id_vehicle>',methods=['POST'])
def post_user_favorite_vehicle(id_user,id_vehicle):
    db.session.query(User).get_or_404(id_user,f'There is no user with id "{id_user}"')
    db.session.query(Vehicle).get_or_404(id_vehicle,f'There is no Planet with id "{id_vehicle}"')
    favorite = Favorite(people_id=None,planet_id=None,vehicle_id = id_vehicle, user_id =id_user)
    db.session.add(favorite)
    db.session.commit()
    return jsonify({"msg":"Done"}),201;

@app.route('/favorites/<int:id_user>/planets/<int:id_planet>',methods=['DELETE'])
def delete_user_favorite_planet(id_user,id_planet):
    db.session.query(User).get_or_404(id_user,f'There is no user with id "{id_user}"')
    db.session.query(Planet).get_or_404(id_planet,f'There is no Planet with id "{id_planet}"')
    toDelete =  db.session.query(Favorite).filter_by(user_id = id_user, planet_id = id_planet).first()      
    try:
        if toDelete is None:
            return jsonify({"msg":"There was no element to delete"}),404
        else:
            db.session.delete(toDelete)
            db.session.commit()
            return jsonify({"msg":"Element was deleted"}),204
    except Exception as err: 
        return jsonify({"error":"There was an unexpected error","msg":str(err)}),500
    
@app.route('/favorites/<int:id_user>/people/<int:id_people>',methods=['DELETE'])
def delete_user_favorite_people(id_user,id_people):
    db.session.query(User).get_or_404(id_user,f'There is no user with id "{id_user}"')
    db.session.query(People).get_or_404(id_people,f'There is no Planet with id "{id_people}"')
    toDelete =  db.session.query(Favorite).filter_by(user_id = id_user, people_id = id_people).first()      
    try:
        if toDelete is None:
            return jsonify({"msg":"There was no element to delete"}),404
        else:
            db.session.delete(toDelete)
            db.session.commit()
            return jsonify({"msg":"Element was deleted"}),204
    except Exception as err: 
        return jsonify({"error":"There was an unexpected error","msg":str(err)}),500

@app.route('/favorites/<int:id_user>/vehicles/<int:id_vehicle>',methods=['DELETE'])
def delete_user_favorite_vehicle(id_user,id_vehicle):
    db.session.query(User).get_or_404(id_user,f'There is no user with id "{id_user}"')
    db.session.query(Vehicle).get_or_404(id_vehicle,f'There is no Planet with id "{id_vehicle}"')
    toDelete =  db.session.query(Favorite).filter_by(user_id = id_user, vehicle_id = id_vehicle).first()      
    try:
        if toDelete is None:
            return jsonify({"msg":"There was no element to delete"}),404
        else:
            db.session.delete(toDelete)
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
         return ({"msg":"There are no characters in the list"})
     else: 
        result = list(map(lambda item: item.serialize(),query_result))     
        return jsonify(result), 200  
        
    except Exception as err:
        return ({"error":"There was an unexpected error","msg":str(err)})
    
@app.route('/people/<int:id>',methods=['GET'])
def get_specific_people(id):
    query_people = People.query.get_or_404(id)    
    result = query_people.serialize()   
    return jsonify(result)
    

""" PLANETS ENDPOITS """


@app.route('/planets',methods=['GET'])
def get_all_planets():
    """ query_planets2 =  Planet.query.all() """
    """ SON EQUIVALENTES """
    query_planets = db.session.query(Planet).all()  

    try:
        if query_planets == None:
            return ({"msg":"There are no planets registered yet"})
        else: 
            result = list(map(lambda item: item.serialize(),query_planets))
            return jsonify(result)
    except Exception as err:
        return ({"error":"There was an unexpected error","error":str(err)})
    
   
@app.route('/planets/<int:id>',methods=['GET'])
def get_specific_planet(id):
    query_planet = db.session.query(Planet).get_or_404(id,f'Sorry there is no planet with id "{id}" registered')
    result = query_planet.serialize()
    return jsonify(result)


""" VEHICLE ENDPOINTS """

@app.route('/vehicles',methods=['GET'])
def get_all_vehicles():
    query_vehicles = db.session.query(Vehicle).all()
    try:
        if query_vehicles == None:
            return ({"msg":"There are no vehicles registered yet"})
        else: 
            result = list(map(lambda item: item.serialize(),query_vehicles))
            return jsonify(result)
    except Exception as err:
        return ({"error":"There was an unexpected error","msg":str(err)})

@app.route('/vehicles/<int:vehicle_id>',methods=['GET'])
def get_specific_vehicle(vehicle_id):
    query_vehicle = db.session.query(Vehicle).get_or_error_404(vehicle_id)
    result = query_vehicle.serialize()
    return jsonify(result)



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

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

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

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





# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

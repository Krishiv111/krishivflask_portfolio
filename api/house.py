from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource # used for REST API building
from datetime import datetime

from model.housepick import Houses

house_api = Blueprint('house_api', __name__,
                   url_prefix='/api/houses')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(house_api)

class HouseAPI:        
    class _Create(Resource):
        def post(self):
            ''' Read data for json body '''
            body = request.get_json()
            
            ''' Avoid garbage in, error checking '''
            # validate name
            name = body.get('name')
            if name is None or len(name) < 2:
                return {'message': f'Name is missing, or is less than 2 characters'}, 210
            # validate uid
            uid = body.get('uid')
            if uid is None or len(uid) < 2:
                return {'message': f'User ID is missing, or is less than 2 characters'}, 210
            # look for password and dob
            baths = body.get('baths')
            if baths is None or len(baths) < 0:
                return {'message': f'Baths is missing, or is less than 2 characters'}, 210
            beds = body.get('beds')
            if beds is None or len(beds) < 1:
                return {'message': f'Beds is missing, or is less than 2 characters'}, 210
            price = body.get('price')
            if price is None or len(price) < 1:
                return {'message': f'Price is missing, or is less than 2 characters'}, 210
            
    

            ''' #1: Key code block, setup USER OBJECT '''
            uo = Houses(name=name, 
                      uid=uid)
            
            ''' Additional garbage error checking '''
            # set password if provided
            
            ''' #2: Key Code block to add user to database '''
            # create user in database
            house = uo.create()
            # success returns json of user
            if house:
                return jsonify(house.read())
            # failure returns error
            return {'message': f'Processed {name}, either a format error or User ID {uid} is duplicate'}, 210

    class _Read(Resource):
        def get(self):
            Houses = Houses.query.all()    # read/extract all users from database
            json_ready = [Houses.read() for users in Houses]  # prepare output in json
            return jsonify(json_ready)  # jsonify creates Flask response object, more specific to APIs than json.dumps

    # building RESTapi endpoint
    api.add_resource(_Create, '/create')
    api.add_resource(_Read, '/')
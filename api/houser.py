from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource # used for REST API building
from datetime import datetime
from model.housing import Houseadd


house_api = Blueprint('home_api', __name__, url_prefix='/api/houser')


# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(house_api)


class houseAPI:        
    class _Create(Resource):
        def post(self):
             ''' Read data for json body '''
             body = request.json
             
             ''' Avoid garbage in, error checking '''
            # validate name
             price = body.get('price')
             if price is None or len(price) < 2:
                return {'message': f'price is missing, or is less than 2 characters'}, 210
           
            # look for date, year
             beds = body.get('beds')
             if beds is None or len(beds) < 1:
                return {'message': f'Beds is missing, or is less than 2 characters'}, 210
             baths= body.get('baths')
             if baths is None or len(baths) < 1:
                return {'message': f'Baths is missing, or is less than 2 characters'}, 210


           
             uo = Houseadd(price, beds, baths)
           
             ''' Additional garbage error checking '''
           
           
             house = uo.create()
           
             if house:
                return jsonify(house.read())
            # failure returns error
             return {'message': f'Processed news error'}, 210


    class _Read(Resource):
        def get(self):
            houses = Houseadd.query.all()    # read/extract all users from database
            json_ready = [houses.read() for houses in houses]  # prepare output in json
            return jsonify(json_ready)  # jsonify creates Flask response object, more specific to APIs than json.dumps


    # building RESTapi endpoint
    api.add_resource(_Create, '/create')
    api.add_resource(_Read, '/')
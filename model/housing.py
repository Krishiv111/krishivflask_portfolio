from random import randrange
from datetime import date
import os, base64
import json

from __init__ import app, db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash

class Houseadd(db.Model):
    __tablename__ = 'HouseEnter'  
    
    id = db.Column(db.Integer, primary_key=True)
    _price = db.Column(db.String(255), nullable=False)
    _beds = db.Column(db.String(255), nullable=False)
    _baths = db.Column(db.String(255), nullable=False )
    
    def __init__(self, price, beds, baths):
        self._price = price
        self._beds = beds
        self._baths = baths
        
    @property
    def price(self):
        return self._price
    
    @price.setter
    def fact(self, price):
       self._price = price
    
    @property
    def beds(self):
        return self._beds
    
    @beds.setter
    def beds(self, beds):
       self._beds = beds
    
    @property
    def baths(self):
        return self._baths
    
    @baths.setter
    def baths(self, baths):
       self._baths = baths
    
    def __str__(self):
        return json.dumps(self.read())

    def create(self):
        try:
            db.session.add(self)  
            db.session.commit() 
            return self
        except IntegrityError:
            db.session.remove()
            return None

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None
    
    def read(self):
        return {
            "price" : self.price,
            "beds" : self.beds,
            "baths" : self.baths
        }
        
def details_table_empty():
    return len(db.session.query(Houseadd).all()) == 0

def initHousepost():
    # db.create_all()
    db.init_app(app)
    if not details_table_empty():
        return
    
    print("Creating test data")
    """Create database and tables"""
    """Tester data for table"""
    
    h1 = Houseadd(price="500 per night", beds="four beds", baths="three baths")
    h2 = Houseadd(price="200 per night", beds="1 beds", baths="2 baths")
    h3 = Houseadd(price="300 per night", beds="3 beds", baths="3 beds")

    
    housepick = [h1, h2, h3]
    

    for houses in housepick:
        try:
            db.session.add(houses)
            db.session.commit()
        except IntegrityError as e:
            print("Error: " +str(e))
            '''fails with bad or duplicate data'''
            db.session.rollback()

initHousepost()
    
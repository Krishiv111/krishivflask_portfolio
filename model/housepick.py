""" database dependencies to support sqliteDB examples """
from random import randrange
from datetime import date
import os, base64
import json
from __init__ import app, db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash


''' Tutorial: https://www.sqlalchemy.org/library.html#tutorials, try to get into Python shell and follow along '''


# Define the Post class to manage actions in 'posts' table,  with a relationship to 'users' table
class House1(db.Model):
   __tablename__ = 'houses'


   # Define the Notes schema
   id = db.Column(db.Integer, primary_key=True)
  # note = db.Column(db.Text, unique=False, nullable=False)
   image = db.Column(db.String, unique=False)
   beds = db.Column(db.String, unique=False)
   baths = db.Column(db.String, unique=False)
   price = db.Column(db.String, unique=False)
   # Define a relationship in Notes Schema to userID who originates the note, many-to-one (many notes to one user)
   userID = db.Column(db.Integer, db.ForeignKey('users.id'))


   # Constructor of a Notes object, initializes of instance variables within object
   def __init__(self, id, beds, baths, price):
       self.userID = id
       self.beds = beds
       self.baths = baths
       self.price = price


   # Returns a string representation of the Notes object, similar to java toString()
   # returns string
   def __repr__(self):
       return "Notes(" + str(self.id) + "," + self.note + "," + str(self.userID) + ")"


   # CRUD create, adds a new record to the Notes table
   # returns the object added or None in case of an error
   def create(self):
       try:
           # creates a Notes object from Notes(db.Model) class, passes initializers
           db.session.add(self)  # add prepares to persist person object to Notes table
           db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
           return self
       except IntegrityError:
           db.session.remove()
           return None


   # CRUD read, returns dictionary representation of Notes object
   # returns dictionary
   def read(self):
       # encode image
       path = app.config['UPLOAD_FOLDER']
       file = os.path.join(path, self.image)
       file_text = open(file, 'rb')
       file_read = file_text.read()
       file_encode = base64.encodebytes(file_read)
      
       return {
           "id": self.id,
           "userID": self.userID,
           "beds": self.beds,
           "price": self.price,
           "baths":self.baths,
           "base64": str(file_encode)
           
       }




# Define the User class to manage actions in the 'users' table
# -- Object Relational Mapping (ORM) is the key concept of SQLAlchemy
# -- a.) db.Model is like an inner layer of the onion in ORM
# -- b.) User represents data we want to store, something that is built on db.Model
# -- c.) SQLAlchemy ORM is layer on top of SQLAlchemy Core, then SQLAlchemy engine, SQL
class Houses(db.Model):
   __tablename__ = 'rents'  # table name is plural, class name is singular


   # Define the User schema with "vars" from object
   id = db.Column(db.Integer, primary_key=True)
   _name = db.Column(db.String(255), unique=False, nullable=False)
   _uid = db.Column(db.String(255), unique=True, nullable=False)
   _price = db.Column(db.String(255), unique=False, nullable=True)
   _beds = db.Column(db.String(255), unique=False, nullable=False)
   _baths = db.Column(db.String(255), unique=False, nullable=False)


   # Defines a relationship between User record and Notes table, one-to-many (one user to many notes)
   rents = db.relationship("rents", cascade='all, delete', backref='users', lazy=True)


   # constructor of a User object, initializes the instance variables within object (self)
   def __init__(self, name, uid, beds, baths ,price):
       self._name = name    # variables with self prefix become part of the object,
       self._uid = uid
       self._beds = beds
       self._baths = baths
       self._price = price


   # a name getter method, extracts name from object
   @property
   def name(self):
       return self._name
  
   # a setter function, allows name to be updated after initial object creation
   @name.setter
   def name(self, name):
       self._name = name
  
   # a getter method, extracts email from object
   @property
   def uid(self):
       return self._uid
  
   # a setter function, allows name to be updated after initial object creation
   @uid.setter
   def uid(self, uid):
       self._uid = uid


      
   # check if uid parameter matches user id in object, return boolean
   def is_uid(self, uid):
       return self._uid == uid


   @property
   def beds(self):
       return self._beds
  
   @beds.setter
   def beds(self, beds):
       self._beds = beds


   def is_beds(self, beds):
       return self._beds == beds
   

   @property
   def baths(self):
       return self._baths
  
   @baths.setter
   def baths(self, baths):
       self._baths = baths


   def is_baths(self, baths):
       return self._baths == baths
   


   @property
   def price(self):
       return self._price
  
   @price.setter
   def price(self, price):
       self._price = price


   def is_baths(self, price):
       return self._price == price
  
   # output content using str(object) in human readable form, uses getter
   # output content using json dumps, this is ready for API response
   def __str__(self):
       return json.dumps(self.read())


   # CRUD create/add a new record to the table
   # returns self or None on error
   def create(self):
       try:
           # creates a person object from User(db.Model) class, passes initializers
           db.session.add(self)  # add prepares to persist person object to Users table
           db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
           return self
       except IntegrityError:
           db.session.remove()
           return None


   # CRUD read converts self to dictionary
   # returns dictionary
   def read(self):
       return {
           "id": self.id,
           "name": self.name,
           "uid": self.uid,
           "beds": self.beds,
           "baths": self.baths,
           "price": self.price,
           "posts": [posts.read() for posts in self.posts]
       }


   # CRUD update: updates user name, password, phone
   # returns self
   def update(self, name="", uid="", beds="", baths="", price=""):
       """only updates values with length"""
       if len(name) > 0:
           self.name = name
       if len(uid) > 0:
           self.uid = uid
       if len(beds) > 0:
           self.beds = beds
       if len (baths) > 0:
           self.baths = baths 
       if len(price) > 0:
           self.price = price    
       db.session.commit()
       return self


   # CRUD delete: remove self
   # None
   def delete(self):
       db.session.delete(self)
       db.session.commit()
       return None


"""Database Creation and Testing """

# Builds working data for testing
def initHouses():
   """Create database and tables"""
   db.create_all()
   """Tester data for table"""
   h1 = Houses(name='House 1 ', uid='h1', beds = 'four', baths = 'three', price='three-hundred night')
   h2 = Houses(name='House 2 ', uid='h2', beds = 'five', baths = 'four', price='four-hundred night')
   
   

   house = [h1, h2]


   """Builds sample user/note(s) data"""
   for house in house:
       try:
           '''add a few 1 to 4 notes per user'''
           for num in range(randrange(1, 4)):
               house.post.append(House1(id=house.id, beds=house._beds, baths=house._baths ,price = house._price))
           '''add user/post data to table'''
           house.create()
       except IntegrityError:
           '''fails with bad or duplicate data'''
           db.session.remove()
           print(f"Records exist, duplicate email, or error: {house.uid}")
           
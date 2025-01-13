from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey


from flask_bcrypt import Bcrypt
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
import  pgeocode
from datetime import datetime, date
import re

# secondary

db = SQLAlchemy()
bcrypt = Bcrypt() 

class PetOwner(db.Model, SerializerMixin):
    __tablename__ = 'pet_owners'

    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String, nullable=False, unique=True)
    _hash_password = db.Column(db.String, nullable=False)

    appointments = db.relationship('Appointment', back_populates='pet_owner', cascade='all, delete-orphan')
    
    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute')
    
    @password.setter
    def password(self, password):
        pattern = re.compile(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[!@#$%^&*]).{8,}$')
        if not password or not isinstance(password, str):
            raise ValueError('Password is required and must be string.')
        if not pattern.match(password) or len(password) < 8:
            raise ValueError('Password must be at least 8 characters long. It must include at least 1 lowercase, 1 uppercase letter, and at least 1 (!@#$%^&*)')
        self._hash_password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self._hash_password, password)
    
        
    @validates('user_name')
    def user_name_validate(self, key, user_name):
        if not user_name or not isinstance(user_name, str):
            raise ValueError('Username is required and must be a string.')
        if len(user_name) < 5:
            raise ValueError('Username must be at least 5 characters long.')
        return user_name
    
    serialize_only = ('id', 'user_name')

    def to_dict(self):
        return{
            col: getattr(self, col) for col in self.serialize_only
        }
    

class PetSitter(db.Model, SerializerMixin):
    __tablename__ = 'pet_sitters'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)           
    location = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)

    appointments = db.relationship('Appointment', back_populates='pet_sitter', cascade='all, delete-orphan', )

    @validates('name')
    def name_validate(self, key, name):
        if not name or not isinstance(name, str):
            raise ValueError('Name is required and must be a string.')
        return name
    
    @validates('location')
    def location_validate(self, key, location):
        if not location or not isinstance(location, str):
            raise ValueError('Location is required and must be a string.')
        return location
    
    @validates('price')
    def price_validate(self, key, price):
        if not price or not isinstance(price, int):
            raise ValueError('price is required and must be an integer.')
        if price < 50 or price > 80:
            raise ValueError('Price must be between 50 and 80 inclusive.')
        return price
    
    serialize_only = ('id', 'name', 'location', 'price')

    def to_dict(self):
        return {
            field: getattr(self, field) for field in self.serialize_only
        }
    
class Appointment(db.Model, SerializerMixin):
    __tablename__ = 'appointments'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    duration = db.Column(db.Integer, nullable=False)

    pet_owners_id = db.Column(db.Integer, ForeignKey('pet_owners.id'), nullable=False)
    pet_sitters_id = db.Column(db.Integer, ForeignKey('pet_sitters.id'), nullable=False)

    pet_owner = db.relationship('PetOwner', back_populates='appointments')
    pet_sitter = db.relationship('PetSitter', back_populates='appointments')

    @validates('date')
    def date_validate(self, key, value):
        if not value or not isinstance(value, datetime):
            raise ValueError('Date is required and must be valid datetime.')
        if value < datetime.now():
            raise ValueError('Date and time must be in the future.')
        return value
    
    @validates('duration')
    def duration_validate(self, key, duration):
        if not duration or not isinstance(duration, int):
            raise ValueError('Duration is required and must be an integer.')
        if duration < 1 or duration > 10:
            raise ValueError('Duration must be between 1 and 10 inclusive.')
        return duration
    
    serialize_only = ('id', 'date', 'duration', 'pet_owners_id', 'pet_sitters_id')
    def to_dict(self):
        return {
            field: getattr(self, field) for field in self.serialize_only
        }
    

class Pet(db.Model, SerializerMixin):
    __tablename__ = 'pets'

    pets = ['cat', 'dog', 'bird']

    id = db.Column(db.Integer, primary_key=True)
    pet_name = db.Column(db.String, nullable=False, unique=True)           
    pet_type = db.Column(db.String, nullable=False, unique=True)  

    @validates('pet_name')
    def pet_name_validate(self, key, pet_name):
        if not pet_name or not isinstance(pet_name, str):
            raise ValueError('Pet name is required and must be a string.')
        return pet_name
    
    @validates('pet_type')
    def pet_type_validate(self, key, pet_type):

        if not pet_type or pet_type not in self.pets:
            raise ValueError('Pet type must be one of: cat, dog, bird')
        return pet_type
    

             


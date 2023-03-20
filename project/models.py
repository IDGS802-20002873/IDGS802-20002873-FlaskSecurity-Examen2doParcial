
from email.policy import default
from . import db
from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin


users_roles = db.Table('users_roles',
    db.Column('userId', db.Integer, db.ForeignKey('user.id')),
    db.Column('roleId', db.Integer, db.ForeignKey('role.id')))

class User(db.Model, UserMixin):
    
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean)
    confirmed_at = db.Column(db.DateTime)
    admin = db.Column(db.Boolean, nullable=True)
    roles = db.relationship('Role',
        secondary=users_roles,
        backref= db.backref('user', lazy='dynamic'))

class Role(RoleMixin, db.Model):

    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description =  db.Column(db.String(255))


class productos(db.Model):
    
    __tablename__ = 'productos'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    marca = db.Column(db.String(255), nullable=False)
    precio=db.Column(db.Integer,nullable= False)
    img = db.Column(db.String(255), nullable=False)
    active =  db.Column(db.Boolean, default=1)    
    
    def __init__(self,name,marca,precio,img): 
    
         self.name=name
         self.marca=marca
         self.precio=precio
         self.img=img
    
    
    
    
    
    
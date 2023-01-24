from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin


db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(45), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    pokemon = db.relationship('Pokemon', backref='author', lazy=True)
    catch = db.relationship('Catch', backref='author', lazy=True)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def saveToDB(self):
        db.session.add(self)
        db.session.commit()


class Pokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    pokename = db.Column(db.String(45), nullable=False, unique=True)
    img = db.Column(db.String)
    date_caught = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    catch = db.relationship('Catch', backref='catch', lazy=True)

    def __init__(self, id, user_id, pokename, img):
        self.id = id
        self.user_id = user_id
        self.pokename = pokename
        self.img = img
    
    def saveToDB(self):
        db.session.add(self)
        db.session.commit()

class Catch(db.Model):
    __tablename__ = 'catch'
    id = db.Column(db.Integer, primary_key=True)
    pokemon_id = db.Column(db.Integer, db.ForeignKey('pokemon.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, user_id, pokemon_id):
        self.user_id = user_id
        self.pokemon_id = pokemon_id
        

    


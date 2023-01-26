from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash


db = SQLAlchemy()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(45), nullable=False, unique=True)
    name = db.Column(db.String(45))
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    wins = db.Column(db.Integer)
    pokemon = db.relationship('Pokemon', backref='author', lazy=True)
    catch = db.relationship('Catch', backref='author', lazy=True)


    def __init__(self, username, name, email, password, wins=0):
        self.username = username
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)
        self.wins = wins

    def saveToDB(self):
        db.session.add(self)
        db.session.commit()

def databaseCommit():
    db.session.commit()


class Pokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    pokename = db.Column(db.String(45), nullable=False, unique=True)
    img = db.Column(db.String)
    base_xp = db.Column(db.Integer)
    base_hp = db.Column(db.Integer)
    base_atk = db.Column(db.Integer)
    base_def = db.Column(db.Integer)
    date_caught = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    catch = db.relationship('Catch', backref='catch', lazy=True)

    def __init__(self, id, user_id, pokename, img, base_xp, base_hp, base_atk, base_def):
        self.id = id
        self.user_id = user_id
        self.pokename = pokename
        self.img = img
        self.base_xp = base_xp
        self.base_hp = base_hp
        self.base_atk = base_atk
        self.base_def = base_def
    
    def saveToDB(self):
        db.session.add(self)
        db.session.commit()

    def removeFromDB(self):
        db.session.delete(self)
        db.session.commit()

class Catch(db.Model):
    __tablename__ = 'catch'
    id = db.Column(db.Integer, primary_key=True)
    pokemon_id = db.Column(db.Integer, db.ForeignKey('pokemon.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, user_id, pokemon_id):
        self.user_id = user_id
        self.pokemon_id = pokemon_id
        

    


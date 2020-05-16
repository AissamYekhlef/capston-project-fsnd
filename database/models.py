from sqlalchemy import Column, String, create_engine, Integer
from flask_sqlalchemy import SQLAlchemy
import json
import os
import datetime

database_filename = os.environ.get("DATABASE", "database.db")
project_dir = os.path.dirname(os.path.abspath(__file__))
database_path = "sqlite:///{}".format(os.path.join(project_dir, database_filename))


db = SQLAlchemy()

"""
setup_db(app)
    binds a flask application and a SQLAlchemy service
"""

def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

def db_drop_and_create_all():
    db.drop_all()
    db.create_all()


"""
Shows
Have actor_id and movie_id for many to many relationships between classes
"""
class Show(db.Model):
    __tablename__ = 'shows'
    actor_id = db.Column(db.Integer(), db.ForeignKey('actors.id'), primary_key=True)
    movie_id = db.Column(db.Integer(), db.ForeignKey('movies.id'), primary_key=True)
 
    def __init__(self, actor_id, movie_id):
        self.actor_id = actor_id
        self.movie_id = movie_id

    def format(self):
        return {"actor_id": self.actor_id, "movie_id": self.movie_id}

    def get_show(self):
        return {
            "actor_id": self.actor_id,
            "movie_id": self.movie_id
        }    

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.format())

"""
Movies
Have title and release year
"""


class Movie(db.Model):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    release_date = Column(String)

    def __init__(self, title, release_date=None):
        self.title = title
        self.release_date = release_date


    def format(self):
        return {"id": self.id, "title": self.title, "release_date": self.release_date}

    def get_movie(self):
        return {
            "id": self.id,
            "title": self.title,
            "release_date": self.release_date
        }    

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.format())


"""
Actors
Have name and age
"""


class Actor(db.Model):
    __tablename__ = "actors"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    gender = Column(String(80), nullable=False)

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def format(self):
        return {"id": self.id, "name": self.name, "age": self.age}

    def get_actor(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }
            

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.format())

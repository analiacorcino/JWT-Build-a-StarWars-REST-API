from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Users(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True, nullable=False)
    first_name = db.Column(db.String(250), unique=False, nullable=False)
    last_name = db.Column(db.String(250), unique=False, nullable=False)
    password = db.Column(db.String(250), unique=False, nullable=False)
    email = db.Column(db.String(250), unique=True, nullable=False)
    bookmarks = db.relationship('Bookmarks', backref='users', lazy=True)

    def __repr__(self):
        return '<Users %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
        }



class Bookmarks(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'))
    character_id = db.Column(db.Integer, db.ForeignKey('characters.id'))
   
    def __repr__(self):
        return '<Bookmarks %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id,
            "character_id": self.character_id,
            # do not serialize the password, its a security breach
        }


class Characters(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    birth_year = db.Column(db.Integer, unique=False, nullable=False)
    gender = db.Column(db.String(250), unique=False, nullable=False)
    height = db.Column(db.Integer, unique=False, nullable=False)
    skin_color = db.Column(db.String(250), unique=False, nullable=False)
    eye_color = db.Column(db.String(250), unique=False, nullable=False)
    bookmarks = db.relationship('Bookmarks', backref='characters', lazy=True)

    def __repr__(self):
        return '<Characters %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "birth_year": self.birth_year,
            "gender": self.gender,
            "height": self.height,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color,  
            
            # do not serialize the password, its a security breach
        }


class Planets(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    climate = db.Column(db.String(250), unique=False, nullable=False)
    diameter = db.Column(db.Integer, unique=False, nullable=False)
    orbital_period = db.Column(db.Integer, unique=False, nullable=False)
    rotation_period = db.Column(db.Integer, unique=False, nullable=False)
    population = db.Column(db.Integer, unique=False, nullable=False)
    bookmarks = db.relationship('Bookmarks', backref='planets', lazy=True)


    def __repr__(self):
        return '<Planets %r>' % self.name

    def serialize(self):
        return {
            "id" : self.id,
            "name" : self.name,
            "climate" : self.climate,
            "diameter" : self.diameter,
            "orbital_period" : self.orbital_period,
            "rotation_period" : self.rotation_period,
            "population" : self.population,
          
        }



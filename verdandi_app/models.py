from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
from flask_login import UserMixin, LoginManager
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


# --- User Model --- #

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    email = db.Column(db.String(150), nullable = False, unique = True)
    first_name = db.Column(db.String(150), nullable = True, default = '')
    last_name = db.Column(db.String(150), nullable = True, default = '')
    username = db.Column(db.String(150), nullable = False, unique = True)
    password = db.Column(db.String(150), nullable = True, default = '')
    user_token = db.Column(db.String, default = '', unique = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    movie = db.relationship('Movie', backref = 'owner', lazy=True)

    # friendlist = db.relationship('Friendlist', foreign_keys=['friendlist.friend_id'], backref = 'owner', lazy=True)
    # watchlist = db.relationship('Watchlist', foreign_keys='user.user_token', backref = 'owner', lazy=True)


    def __init__(self, email, username, first_name, last_name, password, id ='', user_token = ''):
        self.id = self.set_id()
        self.email = email
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password) 
        self.user_token = self.set_token(24)

    def set_id(self):
        return str(uuid.uuid4())

    def set_token(self, length):
        return secrets.token_hex(length)

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def __repr__(self):
        return f"User {self.email} has been added to the database!"
    

# --- Friendlist Model --- #

class Friendlist(db.Model):
    id = db.Column(db.String, primary_key = True)
    friend_id = db.Column(db.String, db.ForeignKey('user.id'), nullable=False)
    user_token = db.Column(db.String, db.ForeignKey('user.user_token'), nullable = False)

    def __init__(self, friend_id, user_token, id =''):
        self.id = self.set_id()
        self.friend_id = friend_id
        self.user_token = user_token


    
    def set_id(self):
        return str(uuid.uuid4())

    def __repr__(self):
        return f"<Friendlist(user_token='{self.user_token}', friend_id='{self.friend_id}')>"

class FriendlistSchema(ma.Schema):
    class Meta:
        model = Friendlist

friendlist_schema = FriendlistSchema()
friendlists_schema = FriendlistSchema(many=True)


# --- Movie Model --- #

class Movie(db.Model):
    id = db.Column(db.String, primary_key = True)
    title = db.Column(db.String(255))
    year = db.Column(db.String(4))
    rated = db.Column(db.String(10))
    release_date = db.Column(db.String(50))
    runtime = db.Column(db.String(20))
    genre = db.Column(db.String(255))
    director = db.Column(db.String(255))
    writer = db.Column(db.String(255))
    actors = db.Column(db.String(255))
    plot = db.Column(db.String(50000))
    language = db.Column(db.String(50))
    country = db.Column(db.String(50))
    awards = db.Column(db.String(255))
    poster_url = db.Column(db.String(255))
    metascore = db.Column(db.String(10))
    imdb_rating = db.Column(db.String(10))
    media_type = db.Column(db.String(20))
    dvd_release = db.Column(db.String(20))
    box_office = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_token = db.Column(db.String, db.ForeignKey('user.user_token'), nullable = False)



    def __init__(self, title, year, rated, release_date, runtime, genre, director, writer, actors, plot, language, country, awards, poster_url, metascore, imdb_rating, media_type, dvd_release, box_office, user_token, id =''):
        self.id = self.set_id()
        self.title = title
        self.year = year
        self.rated = rated
        self.release_date = release_date
        self.runtime = runtime
        self.genre = genre
        self.director = director
        self.writer = writer
        self.actors = actors
        self.plot = plot
        self.language = language
        self.country = country
        self.awards = awards
        self.poster_url = poster_url
        self.metascore = metascore
        self.imdb_rating = imdb_rating
        self.media_type = media_type
        self.dvd_release = dvd_release
        self.box_office = box_office
        self.user_token = user_token



    
    def set_id(self):
        return str(uuid.uuid4())

    def __repr__(self):
        return f"<Movie(title='{self.title}', year={self.year})>"


class MovieSchema(ma.Schema):
    class Meta:
        fields = ['title', 'year', 'rated', 'release_date', 'runtime', 'genre', 'director', 'writer', 'actors', 'plot', 'language', 'country', 'awards', 'poster_url', 'metascore', 'imdb_rating', 'media_type', 'dvd_release', 'box_office', 'user_token']

movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)


# --- Watchlist Model --- #

class Watchlist(db.Model):
    id = db.Column(db.String, primary_key = True)
    movie_id = db.Column(db.String, db.ForeignKey('movie.id'), nullable=False)
    user_token = db.Column(db.String, db.ForeignKey('user.user_token'), nullable = False)


    def __init__(self, movie_id, user_token, id =''):
        self.id = self.set_id()
        self.movie_id = movie_id
        self.user_token = user_token

    
    def set_id(self):
        return str(uuid.uuid4())

    def __repr__(self):
        return f"<Watchlist(user_id='{self.user_token}', movie_id='{self.movie_id}')>"

class WatchlistSchema(ma.Schema):
    class Meta:
        model = Watchlist

watchlist_schema = WatchlistSchema()
watchlists_schema = WatchlistSchema(many=True)
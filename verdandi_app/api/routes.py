from flask import Blueprint, request, jsonify
from ..helpers import token_required
from ..models import db, Movie, movie_schema, movies_schema


api = Blueprint('api',__name__, url_prefix='/api')

@api.route('/getdata')
@token_required
def getdata(our_user):
    return {'some': 'value'}


# --- Create Movie --- #
@api.route('/movies', methods = ['POST'])
@token_required
def create_movie(our_user):
    title = request.json['title']
    year = request.json ['year']
    rated = request.json['rated']
    release_date = request.json ['release_date']
    runtime = request.json ['runtime']
    genre = request.json ['genre']
    director = request.json ['director']
    writer = request.json ['writer']
    actors = request.json ['actors']
    plot = request.json ['plot']
    language = request.json ['language']
    country = request.json ['country']
    awards = request.json ['awards']
    poster_url = request.json ['poster_url']
    metascore = request.json ['metascore']
    imdb_rating = request.json ['imdb_rating']
    media_type = request.json ['media_type']
    dvd_release = request.json ['dvd_release']
    box_office = request.json ['box_office']
    user_token = our_user.user_token


    print(f"User Token: {our_user.user_token}")

    movie = Movie(title, year, rated, release_date, runtime, genre, director, writer, actors, plot, language, country, awards, poster_url, metascore, imdb_rating, media_type, dvd_release, box_office, user_token=user_token,)

    db.session.add(movie)
    db.session.commit()

    response = movie_schema.dump(movie)

    return jsonify(response)


# --- Retrieve All Movies --- #
@api.route('/movies', methods = ['GET'])
@token_required
def get_movies(our_user):
    owner = our_user.user_token
    movies = Movie.query.filter_by(user_token = owner).all()
    response = movies_schema.dump(movies)
    return jsonify(response)


# --- Retrieve One Movie --- #
@api.route('/movies/<id>', methods = ['GET'])
@token_required
def get_movie(our_user, id):
    owner = our_user.user_token
    if owner == our_user.user_token:
        movies = Movie.query.get(id)
        response = movie_schema.dump(movies)
        return jsonify(response)
    else:
        return jsonify({'message': 'Ya need an ID to get in here kid....'}), 401
    

# --- Update Movie --- #
@api.route('/movies/<id>', methods = ['PUT', 'POST'])
@token_required
def update_movie(our_user, id):
        movie = Movie.query.get(id)
        movie.title = request.json['title'] 
        movie.year = request.json['year']
        movie.rated = request.json['rated']
        movie.release_date = request.json['release_date']
        movie.runtime = request.json['runtime']
        movie.genre = request.json['genre']
        movie.director = request.json['director']
        movie.writer = request.json['writer']
        movie.actors = request.json['actors']
        movie.plot = request.json['plot']
        movie.language = request.json['language']
        movie.country = request.json['country']
        movie.awards = request.json['awards']
        movie.poster_url = request.json['poster_url']
        movie.metascore = request.json['metascore']
        movie.imdb_rating = request.json['imdb_rating']
        movie.media_type = request.json['media_type']
        movie.dvd_release = request.json['dvd_release']
        movie.box_office = request.json['box_office']
        movie.user_token = request.json['user_token']
        movie.user_token = our_user.user_token


        db.session.commit()
        response = movie_schema.dump(movie)
        return jsonify(response)


# --- Delete Movie --- #
@api.route('/movies/<id>', methods = ['DELETE'])
@token_required
def delete_movie(our_user, id):
        movie = Movie.query.get(id)
        db.session.delete(movie)
        db.session.commit()

        response = movie_schema.dump(movie)
        return jsonify(response)

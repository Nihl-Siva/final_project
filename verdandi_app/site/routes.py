from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from ..forms import MovieForm
from ..models import  Movie, db
from ..helpers import get_movie_info
import requests


site = Blueprint('site', __name__, template_folder='site_templates')

@site.route('/')
def home():
    return render_template('index.html')


# @site.route('/profile', methods = ['GET', 'POST'])
# @login_required
# def profile():
#     my_movie = MovieForm()
#     try:
#         if request.method == "POST" and my_movie.validate_on_submit():
#             title = my_movie.title.data
#             year = my_movie.year.data
#             rated = my_movie.rated.data
#             release_date = my_movie.release_date.data
#             runtime = my_movie.runtime.data
#             genre = my_movie.genre.data
#             director = my_movie.director.data
#             writer = my_movie.writer.data
#             actors = my_movie.actors.data
#             plot = my_movie.plot.data
#             language = my_movie.language.data
#             country = my_movie.country.data
#             awards = my_movie.awards.data
#             poster_url = my_movie.poster_url.data
#             metascore = my_movie.metascore.data
#             imdb_rating = my_movie.imdb_rating.data
#             media_type = my_movie.media_type.data
#             dvd_release = my_movie.dvd_release.data
#             box_office = my_movie.box_office.data
#             movie_info = get_movie_info(title)
#             title = movie_info.get('title', '')
#             year = movie_info.get('year', '')
#             rated = movie_info.get('rated', '')
#             release_date = movie_info.get('release_date', '')
#             runtime = movie_info.get('runtime', '')
#             genre = movie_info.get('genre', '')
#             director = movie_info.get('director', '')
#             writer = movie_info.get('writer', '')
#             actors = movie_info.get('actors', '')
#             plot = movie_info.get('plot', '')
#             language = movie_info.get('language', '')
#             country = movie_info.get('country', '')
#             awards = movie_info.get('awards', '')
#             poster_url = movie_info.get('poster_url', '')
#             metascore = movie_info.get('metascore', '')
#             imdb_rating = movie_info.get('imdb_rating', '')
#             media_type = movie_info.get('media_type', '')
#             dvd_release = movie_info.get('dvd_release', '')
#             box_office = movie_info.get('box_office', '')


#             user_token = current_user.user_token


#             movie = Movie(title, year, rated, release_date, runtime, genre, director, writer, actors, plot, language, country, awards, poster_url, metascore, imdb_rating, media_type, dvd_release, box_office, user_token)
#             print(movie)
#             db.session.add(movie)
#             db.session.commit()

#             return redirect(url_for('site.profile'))

#     except:
#         raise Exception("We aint takin that movie! Try again pal!")

#     user_token = current_user.user_token
#     movies = Movie.query.filter_by(user_token=user_token)

#     return render_template('profile.html', form=my_movie, movies=movies)



@site.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    my_movie = MovieForm()
    try:
        if request.method == 'POST' and my_movie.validate_on_submit():

            title = my_movie.title.data
            year = my_movie.year.data

           
            # Create and add movie to database
            user_token = current_user.user_token
            movie_info = get_movie_info(title, year)

            movie = Movie(
                title = movie_info['Title'],
                year = movie_info['Year'],
                rated = movie_info['Rated'],
                release_date = movie_info['Released'],
                runtime = movie_info['Runtime'],
                genre = movie_info['Genre'],
                director = movie_info['Director'],
                writer = movie_info['Writer'],
                actors = movie_info['Actors'],
                plot = movie_info['Plot'],
                language = movie_info['Language'],
                country = movie_info['Country'],
                awards = movie_info['Awards'],
                poster_url = movie_info['Poster'],
                metascore = movie_info['Metascore'],
                imdb_rating = movie_info['imdbRating'],
                media_type = movie_info['Type'],
                dvd_release = movie_info['DVD'],
                box_office = movie_info['BoxOffice'],
                user_token = current_user.user_token

            )

            db.session.add(movie)
            db.session.commit()

            return redirect(url_for('site.profile'))

    except:
        raise Exception("We ain't taking that movie! Try again pal!")

    user_token = current_user.user_token
    movies = Movie.query.filter_by(user_token=user_token)

    return render_template('profile.html', form=my_movie, movies=movies)


# def add_movie(title):
#     # Make API call to retrieve movie data
#     movie_data = get_movie_info(title)
#     my_movie = MovieForm()

#     try:
#         if movie_data and my_movie.validate_on_submit():
#             # Create a new Movie object and set its attributes
#             title = my_movie.title.data
#             movie = Movie()
#             movie.title = movie_data['Title']
#             movie.year = movie_data['Year']
#             movie.rated = movie_data['Rated']
#             movie.release_date = movie_data['Released']
#             movie.runtime = movie_data['Runtime']
#             movie.genre = movie_data['Genre']
#             movie.director = movie_data['Director']
#             movie.writer = movie_data['Writer']
#             movie.actors = movie_data['Actors']
#             movie.plot = movie_data['Plot']
#             movie.language = movie_data['Language']
#             movie.country = movie_data['Country']
#             movie.awards = movie_data['Awards']
#             movie.poster_url = movie_data['Poster']
#             movie.imdb_rating = movie_data['imdbRating']
#             movie.media_type = movie_data['Type']
#             movie.box_office = movie_data['BoxOffice']
#             # Add the movie object to the session and commit changes to the database
#             db.session.add(movie)
#             db.session.commit()
#             return True
#         else:
#             return False
#         return redirect(url_for('site.profile'))

#     except:
#         raise Exception("We aint takin that movie! Try again pal!")

#     user_token = current_user.user_token
#     movies = Movie.query.filter_by(user_token=user_token)

#     return render_template('profile.html', form=my_movie, movies=movies)



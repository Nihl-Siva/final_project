from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from ..forms import MovieForm, FriendlistForm
from ..models import  Movie, Friendlist, User, db
from ..helpers import get_movie_info, get_common_movies
import requests


site = Blueprint('site', __name__, template_folder='site_templates')

@site.route('/')
def home():
    return render_template('index.html')


@site.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    my_movie = MovieForm()
    my_friend = FriendlistForm()
    try:
        if request.method == 'POST' and my_movie.validate_on_submit():
            title = my_movie.title.data
            year = my_movie.year.data
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

            flash(f"{title.title()} was added to your watchlist.", "add-movie-successful")
            return redirect(url_for('site.profile'))

        
        elif request.method == 'POST' and my_friend.validate_on_submit():
            friend_username = my_friend.friend_username.data
            friend = User.query.filter_by(username=friend_username).first()
            if friend and friend.username != current_user.username:
                existing_friendship = Friendlist.query.filter_by(username=current_user.username, friend_username=friend_username).first()
                if existing_friendship:
                    flash(f"{friend_username} is already your friend.", "add-friend-failed")
                else:
                    username = current_user.username
                    friend_username = friend.username
                    user_token = current_user.user_token
                    friend_token = friend.user_token

                    friendlist = Friendlist(username=username, friend_username=friend_username, user_token=user_token, friend_token=friend_token)

                    db.session.add(friendlist)
                    db.session.commit()

                    flash(f"{friend_username.title()} was added to your friends list.", "add-friend-successful")
                    return redirect(url_for('site.profile'))
            else:
                if friend and friend.username == current_user.username:
                    flash("You can't add yourself as a friend! Sorry!", "add-self-failed")
                else:
                    flash("Failed to find friend in database. Please try again.", "add-friend-failed")
            return redirect(url_for('site.profile'))

    except:
        flash("We ain't got that movie! Try again pal!", "add-movie-failed")
        return redirect(url_for('site.profile'))

    user_token = current_user.user_token
    movies = Movie.query.filter_by(user_token=user_token)
    friends = Friendlist.query.filter_by(user_token=user_token)

    return render_template('profile.html', my_movie=my_movie, my_friend=my_friend, movies=movies, friends=friends)


# @site.route('/common_movies/<user_token>/<friend_token>')
# def common_movies(user_token, friend_token):
#     # Call your function here
#     movies = get_common_movies(user_token, friend_token)
#     friends = Friendlist.query.filter_by(user_token=user_token)

   
#     return render_template('common_movies.html', movies=movies, friends=friends)

@site.route('/common_movies/<user_token>/<friend_token>')
def common_movies(user_token, friend_token):
    # Call your function here
    movies = get_common_movies(user_token, friend_token)
    print(movies)  # Debugging line
    
    friend = User.query.filter_by(user_token=friend_token)
   
    return render_template('common_movies.html', movies=movies, friend=friend)

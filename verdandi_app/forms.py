from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, SelectField, IntegerField
from wtforms.validators import DataRequired, Email

class SignupForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit_user = SubmitField('Sign Up')

class SigninForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit_user = SubmitField('Sign In')

class FriendlistForm(FlaskForm):
    friend_username = StringField('Friend Username', validators=[DataRequired()])
    submit_friend = SubmitField('Add Friend')

class MovieForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    year = StringField('Year')
    rated = StringField('Movie Rating')
    release_date = StringField('Release Date')
    runtime = StringField('Runtime')
    genre = StringField('Genre')
    director = StringField('Director')
    writer = StringField('Writer')
    actors = StringField('Actors')
    plot = StringField('Plot')
    language = StringField('Language')
    country = StringField('Country')
    awards = StringField('Awards')
    poster_url = StringField('Poster URL')
    metascore = StringField('Metascore')
    imdb_rating = StringField('IMDb Rating')
    media_type = StringField('Media Type')
    dvd_release = StringField('dvd_release')
    box_office = StringField('Box Office')
    submit_movie = SubmitField('Add Movie')

class WatchlistForm(FlaskForm):
    movie_id = StringField('Movie Title', validators=[DataRequired()])
    submit_watchlist = SubmitField('Add To Watchlist')

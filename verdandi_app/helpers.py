from functools import wraps
import secrets
from flask import request, jsonify, json, render_template
from .models import User
# from .forms import MovieForm
import decimal
import requests


def token_required(our_flask_function):
    @wraps(our_flask_function)
    def decorated(*args, **kwargs):
        user_token = None

        if 'x-access-token' in request.headers:
            user_token = request.headers['x-access-token'].split(' ')[1]
            print(user_token)

        if not user_token:
            return jsonify({'message': 'No dice!'}), 401

        try:
            our_user = User.query.filter_by(user_token = user_token).first()
            print(our_user)
            if not our_user or our_user.user_token != user_token:
                return jsonify({'message': 'Nah fish!'})

        except:
            owner = User.query.filter_by(user_token=user_token).first()
            if user_token != owner.user_token and secrets.compare_digest(user_token, owner.user_token):
                return jsonify({'message': 'NOT TODAY SATAN!'})
        return our_flask_function(our_user, *args, **kwargs)
    return decorated


#  --- Request to OMDb for movie info --- #
def get_movie_info(title, year): 

    if year == False:
        year == ''

    headers = {
        'Accept': 'application/json',
        'Authorization': '6b12463b'
    }

    url = f'https://www.omdbapi.com/?apikey=6b12463b&t={title}&y={year}'

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print(response.json())
        return response.json()
    else:
        return {"error": f"Movie not found: {title}"}
    


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        return super(JSONEncoder, self).default(obj)
    

# print(get_movie_info('malignant'))
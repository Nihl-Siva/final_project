from flask import Blueprint, request, jsonify
from ..helpers import token_required
from ..models import db, Watchlist, watchlist_schema, watchlists_schema


api = Blueprint('api',__name__, url_prefix='/api')

@api.route('/getdata')
@token_required
def getdata(our_user):
    return {'some': 'value'}


@api.route('/watchlists', methods = ['POST'])
@token_required
def create_watchlist(our_user):
    title = request.json['title']
    rated = request.json['rated']
    user_token = our_user.token

    print(f"User Token: {our_user.token}")

    watchlist = Watchlist(title, rated, user_token = user_token)

    db.session.add(watchlist)
    db.session.commit()

    response = watchlist_schema.dump(watchlist)

    return jsonify(response)

@api.route('/watchlists', methods = ['GET'])
@token_required
def get_watchlists(our_user):
    owner = our_user.token
    watchlists = Watchlist.query.filter_by(user_token = owner).all()
    response = watchlists_schema.dump(watchlists)
    return jsonify(response)

@api.route('/watchlists/<id>', methods = ['GET'])
@token_required
def get_watchlist(our_user, id):
    owner = our_user.token
    if owner == our_user.token:
        watchlists = Watchlist.query.get(id)
        response = watchlist_schema.dump(watchlists)
        return jsonify(response)
    else:
        return jsonify({'message': 'Ya need an ID to get in here kid....'}), 401

@api.route('/watchlists/<id>', methods = ['PUT', 'POST'])
@token_required
def update_watchlist(our_user, id):
        watchlist = Watchlist.query.get(id)
        watchlist.title = request.json['title']
        watchlist.rated = request.json['rated']
        watchlist.user_token = our_user.token

        db.session.commit()
        response = watchlist_schema.dump(watchlist)
        return jsonify(response)

@api.route('/watchlists/<id>', methods = ['DELETE'])
@token_required
def delete_watchlist(our_user, id):
        watchlist = Watchlist.query.get(id)
        db.session.delete(watchlist)
        db.session.commit()

        response = watchlist_schema.dump(watchlist)
        return jsonify(response)

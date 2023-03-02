from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from ..forms import WatchlistForm
from ..models import Watchlist, db
# from ..helpers import wiki_how_generator



site = Blueprint('site', __name__, template_folder='site_templates')

@site.route('/')
def home():
    return render_template('index.html')

@site.route('/profile', methods = ['GET', 'POST'])
@login_required
def profile():
    my_watchlist = WatchlistForm()
    try:
        if request.method == "POST" and my_watchlist.validate_on_submit():
            make = my_watchlist.make.data.title().strip()
            model = my_watchlist.model.data.title().strip()
            year = my_watchlist.year.data
            color = my_watchlist.color.data.title().strip()
            user_token = current_user.token

            watchlist = Watchlist(make, model, year, color, user_token)

            db.session.add(watchlist)
            db.session.commit()

            return redirect(url_for('site.profile'))

    except:
        raise Exception("We aint takin that watchlist! Try again pal!")

    user_token = current_user.token
    watchlists = Watchlist.query.filter_by(user_token=user_token)

    return render_template('profile.html', form=my_watchlist, watchlists=watchlists)
from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..forms import SignupForm, SigninForm
from ..models import User, db
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, login_required


auth = Blueprint('auth', __name__, template_folder = 'auth_templates')



@auth.route('/signup', methods = ['GET', 'POST'])
def signup():
    form = SignupForm()
    try:
        if request.method == "POST" and form.validate_on_submit():
            email = form.email.data
            first_name = form.first_name.data
            last_name = form.last_name.data
            username = form.username.data
            password = form.password.data

            user = User(email, first_name, last_name, username, password)

            db.session.add(user)
            db.session.commit()

            flash(f"You have successfully created a User account {username}", "user-created")

            return redirect(url_for('auth.signin'))

    except:
        raise Exception('Invalid Form Data: Are you real?')

    return render_template('signup.html', form=form)


@auth.route('/signin', methods = ['GET', 'POST'])
def signin():
    form = SigninForm()
    try:
        if request.method == "POST" and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            print(email, password)

            logged_user = User.query.filter(User.email == email).first()
            if logged_user and check_password_hash(logged_user.password, password):
                login_user(logged_user)
                flash('You were logged in successfully!', 'auth-success')
                return redirect(url_for('site.profile'))
    except:
        raise Exception("Invalid Form Data: Ya better check yer facts!")
    return render_template('signin.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('site.home'))
# coding=utf-8
from flask import Flask, render_template, request, redirect, session, url_for, flash
from models import db, User
from forms import SignupForm, LoginForm, AddressForm
from flask_login import LoginManager, login_required, current_user, login_user, logout_user
from datetime import timedelta
from send_mail import send_mail
import os


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']


db.init_app(app)
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = "login"
login_manager.login_message = "Please login to access this page."
login_manager.init_app(app)

@app.before_request
def make_session_permant():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=5)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


app.secret_key = 'development-key'

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = SignupForm()
    if request.method == 'POST':
        if not form.validate():
            return render_template("signup.html", form=form)
        email = form.email.data
        user = User.query.filter_by(email=email).first()
        if user is not None:
            flash("Email has been used, please use another one!")
            return render_template("signup.html", form=form)
        else:
            newuser = User(form.first_name.data, form.last_name.data, form.email.data, form.password.data)
            db.session.add(newuser)
            db.session.commit()
            token = newuser.generate_confirmation_token()
            send_mail(newuser.email, token)
            return redirect(url_for('home'))
    elif request.method == 'GET':
        return render_template("signup.html", form=form)

@app.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('home'))
    if current_user.confirm(token):
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('home'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if request.method == 'POST':
        if not form.validate():
            return render_template('login.html', form=form)
        else:
            email = form.email.data
            password = form.password.data
            user = User.query.filter_by(email=email).first()
            if user is not None and user.check_password(password):
                login_user(user, form.remember_me.data)
                return redirect(url_for('home'))
            else:
                flash('Email address or password incorrect!')
                return render_template('login.html', form=form)
    elif request.method == 'GET':
        return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/home', methods=['POST', 'GET'])
@login_required
def home():
    form = AddressForm()
    if request.method == 'POST':
        if not form.validate():
            return render_template('home.html', form=form)
        else:
            pass
    elif request.method == 'GET':
        return render_template('home.html', form=form)

@app.route('/map')
def map():
    return render_template('map.html')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

if __name__ == "__main__":
    app.run('0.0.0.0', port=5000)

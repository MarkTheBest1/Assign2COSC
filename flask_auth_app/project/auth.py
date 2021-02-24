# auth.py

from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from .models import User
from . import db

auth = Blueprint('auth', __name__)
#when creating a new page you have to render it first
#then do the things after

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    name = request.form.get('name')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(name=name).first()

    # check if user actually exist
    # take the user supplied password, hash it, and compare it to the hashed password in database
    if not user or not check_password_hash(user.password, password): 
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) # if user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))

@auth.route('/profile', methods=['POST'])
def profile_post():
    name = request.form.get('name')
    address1 = request.form.get('Address1')
    address2 = request.form.get('Address2')
    city = request.form.get('city')
    state = request.form.get('State')
    zipCode = request.form.get('ZipCode')

    num_rows_updated = User.query.filter_by(name='name').update(dict(name='name'))
    db.session.commit()

    num_rows_updated = User.query.filter_by(Address_1='address1').update(dict(Address_1='address1'))
    db.session.commit()

    num_rows_updated = User.query.filter_by(Address_2='address2').update(dict(Address_2='address2'))
    db.session.commit()

    num_rows_updated = User.query.filter_by(City='city').update(dict(City='city'))
    db.session.commit()

    num_rows_updated = User.query.filter_by(State='state').update(dict(State='state'))
    db.session.commit()

    num_rows_updated = User.query.filter_by(Zip='zipcode').update(dict(Zip='zipcode'))
    db.session.commit()


   # user = User.query.filter_by(name=name).first()
    #remember = True if request.form.get('remember') else False
    # db.session.add(new_user)
    # db.session.commit()



    return redirect(url_for('main.profile'))

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():

    #email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    #if decide to implement email just change email with a different var
    user = User.query.filter_by(name=name).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again  
        flash('Name already exists')
        return redirect(url_for('auth.signup'))

    # create new user with the form data. Hash the password so plaintext version isn't saved.
    new_user = User( name=name, password=generate_password_hash(password, method='sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
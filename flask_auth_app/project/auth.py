# auth.py

from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from .models import User
from . import db
from sqlalchemy.orm.attributes import flag_modified
from sqlalchemy import update

auth = Blueprint('auth', __name__)
#when creating a new page you have to render it first
#then do the things after

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('name')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(username=username).first()

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
    user = User.query.filter_by(id= User.id).first() #finds the queried id and sets it to user


    #these variables will hold the info the user types in when they login
    newname = request.form.get('name')
    address1 = request.form.get('Address1')
    address2 = request.form.get('Address2')
    city = request.form.get('city')
    state = request.form.get('State')
    zipCode = request.form.get('ZipCode')


    #this then assigns the database's field with the variables above
    user.name = newname #sets the new name
    user.Address_1 = address1
    user.Address_2 = address2
    user.City = city
    user.State = state
    user.Zip = zipCode
    db.session.commit() #This updates the information in the database

    #this statement gets all of the data that is stored in the databse
    users = User.query.all()
    data = users #sets it to users object that is above

    #the return statement reloads the profile webpage with the newly entered information to show the user
    #that the info they put in is now saved
    #also passes data into the html file to be later displayed

    #shows new message at the top.
    message="If your information isn't up to date please fill in the form below"

    return render_template("profile.html", name=newname, Address_1=address1,Address_2=address2,
                           City=city, State=state,Zip=zipCode, data=data,message=message)


@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():

    #email = request.form.get('email')
    username = request.form.get('name')
    password = request.form.get('password')

    #if decide to implement email just change email with a different var
    user = User.query.filter_by(username=username).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again  
        flash('Name already exists')
        return redirect(url_for('auth.signup'))

    # create new user with the form data. Hash the password so plaintext version isn't saved.
    new_user = User( username=username, password=generate_password_hash(password, method='sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
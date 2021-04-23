# auth.py
import sqlite3

from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from .models import User
from .models import Fuel
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

@auth.route('/fuelquote', methods=['POST'])
def fuelquote_post():

    gallonsrequested = request.form.get('gallonsrequested')
    deliveryaddress = request.form.get('deliveryaddress')
    deliverydate = request.form.get('deliverydate')
    pricepergallon = 1.50

    locationFactor=0

    
    user = Fuel()
    user.gallons = int(gallonsrequested)
    user.address = deliveryaddress
    user.date = deliverydate
    user.price_gallon = float(pricepergallon)


    #finds the correct user by the id so the fuel module can then use the correct state that belongs to that user
    temp = User.query.filter_by(id= Fuel.id).first() #finds the queried id and sets it to user
    #print(temp.State)

    #
    # Sets the location factor based on where the user is found
    #
    if temp.State == "TX" :
        locationFactor=0.02
    else:
        locationFactor=0.04

    #
    # Sets the rate History Factor
    #
    missing = Fuel.query.filter_by(address=temp.Address_1).first() #queries by address; the users profiel address and
    #the delivery address has to be the same
    if missing is None :
        rateHistory = 0.0#if the address has NOT bought before then the person gets NO the discount
    else:
        rateHistory = 0.01 #if the address has bought before then the person gets the discount

    #
    # Gallons requested factor
    #
    galRequestfactor=0
    if int(gallonsrequested) > 1000:
        galRequestfactor = 0.02
    else:
        galRequestfactor = 0.03

    #
    # company profit factor
    #
    companyProfitFactor = 0.10

    #
    # marginfactor
    #
    margin = (locationFactor - rateHistory + galRequestfactor + companyProfitFactor) * pricepergallon

    #
    # suggested price & amount due
    #
    suggestedPrice_gallon = pricepergallon + margin

    amountdue = int(gallonsrequested) * suggestedPrice_gallon
    user.amount = amountdue

    #if the userclicks on the actual submit button then the data is actually added to db
    if "submit" in request.form:
        db.session.add(user)
        db.session.commit()
    elif "quote" in request.form:
        flash('$' + str(amountdue)) #sends the message to the html




    #gets the past fuel deliveries by address so data will only have the data for that one person
    pastFuel = Fuel.query.filter_by(address=temp.Address_1).all()

    data = pastFuel
    
    
    
    pricestring = "Suggested Price per Gallon: " + str(pricepergallon)
    amountduestring = "Total Amount Due: " + str(amountdue)
    return render_template('fuelquote.html', pricestring = pricestring, amountduestring = amountduestring, data=data)
################################################################################################################

@auth.route('/profile', methods=['POST'])
def profile_post():
    user = User.query.filter_by(id= User.id).first() #finds the queried id and sets it to user

    errors = False
    #these variables will hold the info the user types in when they login
    newname = request.form.get('name')
    if len(newname) > 50:
        flash('Name has to be less than 50 characters')
        errors=True

    address1 = request.form.get('Address1')
    if len(address1) > 100:
        flash('Address1 has to be less than 100 characters')
        errors = True

    address2 = request.form.get('Address2')
    if len(address2) > 100:
        flash('Address2 has to be less than 100 characters')
        errors = True

    city = request.form.get('city')
    if len(city) > 100:
        flash('City has to be less than 100 characters')
        errors = True

    state = request.form.get('State')
    if len(state) > 2:
        flash('State has to be 2 letter abbreviation')
        errors = True

    zipCode = request.form.get('ZipCode')
    if len(zipCode) <4 and len(zipCode) >9:
        flash('Zip code has to be more than 5 numbers and less than 9')
        errors = True

    if errors:
        return redirect(url_for('auth.profile_post'))


    #
    # After user has entered things we could do another check under here for the
    # required info


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
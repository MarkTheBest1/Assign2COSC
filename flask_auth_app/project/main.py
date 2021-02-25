# main.py

from flask import Blueprint, render_template
from flask_login import login_required, current_user

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    #this is the first render for profile, if the user is new then the html file will know to only display
    #the necessary title:Ex. Address1, Address 2...
    message="Please enter your information before continuing"
    return render_template('profile.html', name=current_user.name, Address_1=current_user.Address_1,
                           Address_2=current_user.Address_2,City=current_user.City,State=current_user.State,
                           Zip=current_user.Zip,message=message)
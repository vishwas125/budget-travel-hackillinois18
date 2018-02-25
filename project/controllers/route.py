from project import app
from flask import render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
import datetime
from project.models.data import User
from project.models.data import Travel
from project.models.place import Place


class CreateForm(FlaskForm):
    text = StringField('name', validators=[DataRequired()])


@app.route('/')
def start():
    return render_template('/views/index.html')


@app.route('/process', methods=['GET', 'POST'])
def process():
    if request.method=='POST':
        location=request.form['location']
        budget=request.form['budget']
        start=request.form['startdate']
        end=request.form['enddate']
        travelIsChecked='travel' in request.form
        accIsChecked='acc' in request.form
        foodIsChecked='food' in request.form
        start = datetime.datetime.strptime(start,'%d %B, %Y').strftime('%Y-%m-%d')
        end = datetime.datetime.strptime(end,'%d %B, %Y').strftime('%Y-%m-%d')

        User.origin_city=location
        User.return_date=end
        User.start_date=start
        User.user_budget=budget
        User.stay_preference=accIsChecked
        User.travel_preference=travelIsChecked
        User.food_preference=foodIsChecked
        

        user=User(location,start,end,budget)
        travelObj=Travel(user)
        places=travelObj.travel_start()


    return render_template('/views/submit.html',places=places)


@app.route('/place-details/<place>', methods=['GET','POST'])
def placedetails(place):
    return render_template('/views/place-details.html',item=place)

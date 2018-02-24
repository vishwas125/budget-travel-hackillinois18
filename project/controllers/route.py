from project import app
from flask import render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class CreateForm(FlaskForm):
    text = StringField('name', validators=[DataRequired()])


@app.route('/')
def start():
    return render_template('')


@app.route('/', methods=['GET', 'POST'])
def printer():
    form = CreateForm(request.form)
  
    return render_template('', form=form)

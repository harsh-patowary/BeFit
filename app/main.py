# from crypt import methods
from curses import flash
# Make routing calls noot just locally
import requests
import json
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort
# custom mods
from app.befit_utils import UserData

app = Flask(__name__)
app.config['SECRET_KEY'] = 'harsh004'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/bmi', methods = ['GET', 'POST']) 
def bmi():
    if request.method == 'POST':
        usr_name = request.form['name']
        usr_age = request.form['age']
        usr_height = request.form['height']
        usr_weight = request.form['weight']
        bmi_unit = request.form.get('unit')
        if not usr_height:
            flash("Your Height is required!!")
        elif not usr_weight:
            flash("Your Weight is Required!!")
        elif not bmi_unit:
            flash("The Unit is Required!!")
        else: 
            usr_data = UserData(usr_age, usr_weight, usr_height, usr_name, bmi_unit)
            usr_bmiStatus = usr_data.bmi_class()
            usr_bmi = round(usr_data._bmi)
            return render_template('bmi.html', usr_bmi=usr_bmi, usr_bmiStatus=usr_bmiStatus)
    
    return render_template('bmi.html')



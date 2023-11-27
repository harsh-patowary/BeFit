# from crypt import methods
from curses import flash
import requests
import json
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort
# custom mods
from app.befit_utils import UserData, BFUtils
import os
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = 'harsh004'
app_id = "d16a2064"
app_key = "754bc0f60796c0031d1da99d58a3f1da"
food_log = dict()
tot_calories = 0
user_data = UserData(None, None, None, None, None, None, None)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    # register user see if existing redirect to login page
    if request.method == 'POST':
        usr_name = request.form['name']
        usr_email = request.form['email']
        usr_password = request.form['usr_password']
        usr_age = request.form['age']
        usr_height = request.form['height']
        usr_weight = request.form['weight']
        bmi_unit = request.form.get('unit')
        print("extracted\n")
        if not usr_height:
            flash("Your Height is required!!")
        elif not usr_weight:
            flash("Your Weight is Required!!")
        elif not bmi_unit:
            flash("The Unit is Required!!")
        else: 
            user_data = UserData(usr_email, usr_password, usr_name, usr_age, usr_height, usr_weight, bmi_unit)
            data_list = user_data.convert_to_array()
            if not BFUtils.check_userValidity(user_data._name):
                BFUtils.insert_data(data_list)
                flash("User Registration complete!!")
                return redirect(url_for('login'))
            else:
                flash("User already exixts")
            
    return render_template('registration.html')

@app.route('/login',  methods = ['GET', 'POST'])
def login():
    # use login info to pull userData from sql/csv and initialize global User Object
    global user_data;
    if request.method == 'POST':
        usr_email = request.form['email']
        usr_password = request.form['usr_password']
        with open("data.csv", "r") as file:
            csvreader = csv.reader(file)
            for line in csvreader:
                if usr_email==line[0] and usr_password==line[1]:
                    user_data = user_data.load_user(usr_email)
                    return redirect(url_for('calorie_tracker'))
    return render_template('login.html')

@app.route('/bmi', methods = ['GET', 'POST']) 
def bmi():
    if request.method == 'POST':
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
            usr_data = UserData(usr_age, usr_weight, usr_height, usr_name, bmi_unit,)
            usr_bmiStatus = usr_data.bmi_class()
            usr_bmi = round(usr_data._bmi)
            BFUtils.insert_data("/data.csv", usr_data.convert_to_array())
            return render_template('bmi.html', usr_bmi=usr_bmi, usr_bmiStatus=usr_bmiStatus)
    
    return render_template('bmi.html')



@app.route('/calorietracker', methods = ['GET', 'POST'])
def calorie_tracker():
    global food_log
    global tot_calories
    global user_data
    name = user_data._name
    if request.method == 'POST':
        ingredient = request.form['ingredient']
        usr_ingr_amount = float(request.form['ingr_weight'])
        ENCODED_ingredient = BFUtils.remove_space(ingredient)
        
        if not ingredient:
            flash("Ingrediant is needed")
        else:
            
            api_url = f"https://api.edamam.com/api/nutrition-data?app_id={app_id}&app_key={app_key}&nutrition-type=logging&ingr={ENCODED_ingredient}"
            response = requests.get(api_url).json()
            fooCal = response["calories"]
            fooIngrWeight = response["totalWeight"]
            calories_perGram = BFUtils.cal_perGram(float(fooCal), float(fooIngrWeight))
            print(type(response))
            calories = calories_perGram * usr_ingr_amount
            print(f"Ingredients: {ingredient}, Calories: {calories}, {fooIngrWeight}, {fooCal}\n")
            food_details = {'calories' : round(calories), 'user_consumption' : usr_ingr_amount}
            flag = {ingredient: food_details}
            food_log.update(flag)
            tot_calories += round(calories)
            total_calories = round(tot_calories)
            print(food_log)
            return render_template('calorie-tracker.html', food_log=food_log, total_calories=total_calories, name=name)
            

    return render_template('calorie-tracker.html', food_log=food_log, total_calories=tot_calories, name=name)


@app.route("/submitting")
def submitting():
    # todo: submit given info with all user & food tracking info into csv/database with the submit button
    # idkkdkdkdkdk howwww
    return render_template('calorie-tracker.html')


@app.route('/delete_item/<food>')
def delete_item(food):
    global food_log
    global tot_calories
    foo = food_log.get(food)
    loo = foo["calories"]
    tot_calories -= loo
    food_log.pop(food)
    print(f"deleting.....{food}")
    print(food_log)
    
    return redirect(url_for('calorie_tracker'))

# @app.route('calorietracker/adding_food', methods = ['GET', 'POST'])
# def add_item():
    
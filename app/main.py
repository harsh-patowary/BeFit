# from crypt import methods
from curses import flash
from datetime import datetime, timedelta
import requests
import json
import numpy as np
from flask import Flask, render_template, request, url_for, flash, redirect, session
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
date = ""
user_data = UserData(None, None, None, None, None, None, None)

@app.route('/')
def index():
    if 'logged_in' in session:
        return render_template('index.html', logged_in=session['logged_in'])
    else:
        session['logged_in'] = False
        return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    # register user see if existing redirect to login page
    if request.method == 'POST':
        usr_name = request.form['name']
        usr_email = request.form['email']
        usr_password = request.form['usr_password']
        # usr_age = request.form['age']
        usr_dob = request.form['bday']
        usr_age=usr_dob
        usr_height = request.form['height']
        usr_weight = request.form['weight']
        bmi_unit = request.form.get('unit')
        print("extracted\n")
        print(usr_dob)
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
                BFUtils.insert_user(data_list)
                flash("User Registration complete!!")
                return redirect(url_for('login'))
            else:
                flash("User already exixts")
            
    return render_template('registration.html')

@app.route('/login',  methods = ['GET', 'POST'])
def login():
    # use login info to pull userData from sql/csv and initialize global User Object
    global user_data;
    if not session['logged_in']:
        if request.method == 'POST':
            usr_email = request.form['email']
            usr_password = request.form['usr_password']
            print(f"{usr_email} {usr_password}")
            login_state = False
            with open("data.csv", "r") as file:
                csvreader = csv.reader(file)
                for line in csvreader:
                    if usr_email==line[0] and usr_password==line[1]:
                        user_data = user_data.load_user(usr_email)
                        # print(user_data.calc_bmi)
                        # print(user_data._bmi)
                        session['logged_in'] = True
                        session['username'] = usr_email
                        print(session['username'])
                        print(session)
                        login_state = True
                        # return redirect(url_for('calorie_tracker'))
            if login_state:
                return redirect(url_for('calorie_tracker'))
            else:
                flash("Wrong Credentials")
    
    else: 
        flash('Already logged in')
        return redirect(url_for('calorie_tracker'))
                
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    session['logged_in'] = False
    return redirect(url_for('login'))

@app.route('/bmi', methods = ['GET', 'POST']) 
def bmi():
    if request.method == 'POST':
        usr_height = request.form['height']
        usr_weight = request.form['weight']
        bmi_unit = request.form['unitRadio']
        # bmi_unit = request.form.get('unit')
        # flag = request.form['unitRadio']
        # print(flag)
        if not usr_height:
            flash("Your Height is required!!")
        elif not usr_weight:
            flash("Your Weight is Required!!")
        elif not bmi_unit:
            flash("The Unit is Required!!")
        else: 
            usr_data = UserData("", "", "Guest", 0 , usr_height, usr_weight, bmi_unit)
            usr_bmiStatus = usr_data.bmi_class()
            usr_bmi = round(usr_data._bmi)
            # BFUtils.insert_data("/data.csv", usr_data.convert_to_array())
            return render_template('bmi.html', usr_bmi=usr_bmi, usr_bmiStatus=usr_bmiStatus, logged_in=session['logged_in'])
    
    return render_template('bmi.html', logged_in=session['logged_in'])



@app.route('/calorietracker', methods = ['GET', 'POST'])
def calorie_tracker():
    global food_log
    global tot_calories
    global user_data
    name = user_data._name
    global date
    
    logged_in=session['logged_in']
    
    if logged_in != True or logged_in == None:
        flash("You are not logged in")
        print(f"redirecting....")
        return redirect(url_for('login'))
        
    else:
        print(session['username'])
        if request.method == 'POST':
            if request.form['food_name']:
                
                food_name = request.form['food_name']
                
                usr_ingr_amount = float(request.form['ingr_weight'])
                ENCODED_ingredient = BFUtils.remove_space(food_name)
                
                if not food_name and usr_ingr_amount:
                    flash("Food and amount are needed")
                else:
                    
                    api_url = f"https://api.edamam.com/api/nutrition-data?app_id={app_id}&app_key={app_key}&nutrition-type=logging&ingr={ENCODED_ingredient}"
                    
                    response = requests.get(api_url).json()
                    fooCal = response["calories"]
                    # fooSugar = response["SUGAR"]["quantity"]
                    # fooFat = response["FAT"]["quantity"]
                    # fooCholestrol = response["CHOLE"]["quantity"]
                    # fooCarbs = response["CHOCDF.net"]["quantity"]
                    print(response)
                    nutrients_dict = {}
                    code = requests.head(api_url)
                    
                    if response['totalWeight'] > 0:
                        for ingredient in response['ingredients']:
                            
                            for item in ingredient['parsed']:
                                key = item['food']  # or any other unique identifier you prefer
                                nutrients_dict = item['nutrients']
                        
                        fooFoodWeight = response["totalWeight"]
                    
                        fooSugar = nutrients_dict['SUGAR']["quantity"]
                        fooCholestrol = nutrients_dict['CHOLE']["quantity"]
                        fooFat = nutrients_dict["FAT"]["quantity"]
                        fooCarbs = nutrients_dict["CHOCDF"]["quantity"]
                        print(nutrients_dict)
                        print(fooSugar)
                        print(fooCarbs)
                        calories_perGram = BFUtils.nutrients_perGram(float(fooCal), float(fooFoodWeight))
                        print((response))
                        calories = calories_perGram * usr_ingr_amount
                        sugar = (BFUtils.nutrients_perGram(float(fooSugar), float(fooFoodWeight))) * fooFoodWeight
                        fat = BFUtils.nutrients_perGram(float(fooFat), float(fooFoodWeight))
                        cholestrol = BFUtils.nutrients_perGram(float(fooCholestrol), float(fooFoodWeight))
                        carbs = (BFUtils.nutrients_perGram(float(fooCarbs), float(fooFoodWeight))) * fooFoodWeight
                        print(f"Ingredients: {food_name}, Calories: {calories}, Food Weight: {fooFoodWeight}, Sugar: {sugar}, Carbs : {carbs}\n")
                        food_details = {'calories' : round(calories, 3), 
                                        'user_consumption' : usr_ingr_amount, 
                                        'sugar' : round(sugar, 3),
                                        'fat': round(fat, 3),
                                        'cholestrol': round(cholestrol, 3),
                                        'carbs' : round(carbs, 3)}
                        flag = {food_name: food_details}
                        food_log.update(flag)
                        tot_calories += round(calories)
                        print(food_log)
                        total_calories = round(tot_calories)
                        print(food_log)
                        
                        return render_template('calorie-tracker.html', food_log=food_log, total_calories=total_calories, name=name, logged_in=logged_in)
                    
                    else: 
                        flash("Invalid response!!")
                    
            else:
                flash('Food, amount is needed')
                
            
        # return render_template('calorie-tracker.html', logged_in=logged_in)
        return render_template('calorie-tracker.html', food_log=food_log, total_calories=tot_calories, name=name, logged_in=logged_in)
            
            
        # return render_template('calorie-tracker.html', food_log=food_log, total_calories=tot_calories, name=name, logged_in=logged_in)

@app.route("/generate-pdf", methods=['GET', 'POST'])
def generate_analysis():
    global user_data
    logged_in=session['logged_in']
    
    if logged_in != True or logged_in == None:
        flash("You are not logged in")
        print(f"redirecting....")
        return redirect(url_for('login'))
    else:
        
        if request.method=='POST':
            date1 = request.form['date1']
            date2 = request.form['date2']
            print(f"{date1}  {date2}")
            start_date = datetime.strptime(date1, "%Y-%m-%d")
            end_date = datetime.strptime(date2, "%Y-%m-%d")

            # Generate dates between start_date and end_date
            dates_in_between = []
            current_date = start_date
            while current_date <= end_date:
                dates_in_between.append(current_date.strftime("%Y-%m-%d"))
                current_date += timedelta(days=1)

            print(dates_in_between)
            
            total_user_intake = BFUtils.load_user_intake(user_data._email)
            print(len(total_user_intake))
            
            index = 0
            
            ranged_intake=[]
            ranged_dates = []
            for intake in total_user_intake:
                # s1 = intake[0]
                # print(f"{intake[0]} : {intake[1]}")
                # s2 = dates_in_between[index]
                # print(dates_in_between[index])
                for date in dates_in_between:
                    if intake[0] == date:
                        print("intake.....step")
                        ranged_intake.append(intake)
                        ranged_dates.append(date)
                        
            print(ranged_intake)
            print(ranged_dates)
            mat = np.array(ranged_dates)
            calorie_points = np.array(BFUtils.get_calories(ranged_intake))
            carbs_points = np.array(BFUtils.get_carbs(ranged_intake))
            fat_points = np.array(BFUtils.get_fat(ranged_intake))
            sugar_points = np.array(BFUtils.get_sugar(ranged_intake))
            choles_points = np.array(BFUtils.get_cholestrol(ranged_intake))
            print(calorie_points) 
            print(carbs_points)
            print(fat_points)
            print(sugar_points)
            print(choles_points)
            calorie_fat = BFUtils.get_fat(ranged_intake)
            carbs_cholestrol = BFUtils.get_cholestrol(ranged_intake)
            p1 = BFUtils.generate_graphs(mat, calorie_points, "Total Calories", "calories")
            p2 = BFUtils.generate_graphs(mat, carbs_points, "Total Carbs", "carbohydrates")
            p3 = BFUtils.generate_graphs(mat, fat_points, "Total Fat", "fat")
            p4 = BFUtils.generate_graphs(mat, sugar_points, "Total Sugar", "Sugar")
            p5 = BFUtils.generate_graphs(mat, choles_points, "Total Cholestrol", "Cholestrol")
            
            BFUtils.generate_pdf("analysis.pdf")
            

            
    return render_template('generate-pdf.html', logged_in=logged_in)

    


@app.route("/submitting", methods=['GET', 'POST'])
def submitting():
    global food_log
    global tot_calories
    # todo: submit given info with all user & food tracking info into csv/database with the submit button
    # idkkdkdkdkdk howwww
    # daily_user_intake = [user_data._email, ]
    # date = request.form['date']
    if request.method == 'POST':
        date = request.form['date']
        print(type(date))
        food_name = next(iter(food_log))
        
        user_intake = [user_data._email, date, tot_calories, food_log[food_name]['carbs'], food_log[food_name]['fat'], food_log[food_name]['sugar'], food_log[food_name]['cholestrol']]
        print(user_intake)  # For demonstration, simply print the value. Process as needed.
        BFUtils.insert_food_data(user_intake)
        food_log.clear()
        return redirect(url_for('calorie_tracker'))
    # 
    return render_template('test.html')


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
    
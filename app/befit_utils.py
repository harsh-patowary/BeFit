# Util Contents
import os
import csv
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('agg')
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.graphics.shapes import Drawing
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.graphics.charts.barcharts import VerticalBarChart
# import numpy as np
class UserData:
    
    _age = None
    _weight = None
    _height = None
    _name = None
    _bmi = None
    _unit = None
    _email = None
    _password = None
    _calories_intake = None
    _goal_range = None
    
    
    
    def __init__(self, em, pwd, n, a, h, w, u):
        self._age = a
        self._weight = w
        self._height = h
        self._name = n
        self._unit = u
        self._email = em
        self._password = pwd
    
    
    def calc_bmi(self):
        # float(self._height)
        # float(self._weight)
        if self._unit == 'm':
            self._bmi = float(self._weight) / pow(float(self._height), 2)
            return self._bmi 
        elif self._unit == 'i':
            self._bmi  = (703 * float(self._weight))/ pow(float(self._height), 2)
            return self._bmi 
        else:
            return 'Basic Unit Error:IM/ME404'
        
    def bmi_class(self):
        self.calc_bmi()
        if self._bmi  > 0:
           if self._bmi  <= 16:
               return 'very underweight'
           elif self._bmi  <= 18.5:
               return 'underweight'
           elif self._bmi  <= 24:
               return 'healthy'
           elif self._bmi <= 30:
               return 'overweight'
           else:
               return 'very overweight'
        else:
            return 'Invalid Range Error:BMI/RA23'
        
        
    # def set_food_intake(self, food):
        
        
    def convert_to_array(self): 
        
        return [self._email, self._password, self._name, self._age, self._height, self._weight, self._unit, round(self.calc_bmi()), self._calories_intake]
    
    def convert_to_obj(self, data):
        return UserData(data[0], data[1], data[2], data[3], data[4], data[5], data[6])
      
    
    def load_user(self, email):
        with open("data.csv", "r") as file:
            users = csv.reader(file)
            for user in users:
                if user[0] == email:
                    return self.convert_to_obj(user)



class BFUtils:
    
    def load_user_intake(email):
        
        with open("user_diet_data.csv", "r") as file:
            intake_data = csv.reader(file)
            total_user_intake = []
            for intake_entry in intake_data:
                if intake_entry[0] == email:
                    flag = [intake_entry[1], intake_entry[2], intake_entry[3], intake_entry[4], intake_entry[5], intake_entry[6]]
                    total_user_intake.append(flag)
                    # print(total_user_intake)
                    
        return total_user_intake
                    
    
    def remove_space(ingr):
        newStr = ""
        for ch in ingr:
            if ch == " ":
                ch = "%20"
            newStr+=ch
        return newStr
    
    def insert_user(data):
        file_exists = os.path.isfile("data.csv")
        with open("data.csv", "a", newline='') as file:
            csvwriter = csv.writer(file)
                
            if not file_exists:
                header = ['Email','Password', 'Name', 'Age', 'height', 'weight', 'unit', 'bmi', 'calories']
                csvwriter.writerow(header)
                    
            csvwriter.writerow(data)
            
    def insert_food_data(data):
        file_exists = os.path.isfile("user_diet_data.csv")
        with open("user_diet_data.csv", "a", newline='') as file:
            csvwriter = csv.writer(file)
            if not file_exists:
                header = ['email', 'date', 'total_Calories', 'total_carbs', 'total_fat', 'total_sugar', 'total_cholestrol']
                csvwriter.writerow(header)
                
            csvwriter.writerow(data)
            
    def nutrients_perGram(nut, weigh):
        return float(nut/weigh)
    
    def check_userValidity(user):
        with open("data.csv", "r") as file:
            csvreader = csv.reader(file)
            for line in csvreader:
                if line[0] == user:
                    return True
                
            return False
        
    def generate_graphs(x, y, title, ylabel):
        plt.plot(x, y)
        plt.title("Linear Graph")
        plt.ylabel(ylabel)
        plt.xlabel("Dates")
        temp_fname = f"{ylabel}_plot.png"
        plt.savefig(temp_fname)
        plt.close()
        # for i in range(3):
        #     fig, ax = plt.subplots()
        #     # x = [1, 2, 3, 4, 5]
        #     # y = [i * val for val in x]
        #     ax.plot(x, y)
        #     ax.set_xlabel('X-axis')
        #     ax.set_ylabel('Y-axis')
        #     ax.set_title(f'Graph {title}')
            
        #     # Save the Matplotlib figure to a temporary file
        #     temp_filename = f'temp_plot_{i}.png'
        #     plt.savefig(temp_filename)
            
        #     # Add the Matplotlib figure to the PDF as an image
           
        #     plt.close()
    
    def get_calories(data):
        flag = []
        for entry in data:
            flag.append(entry[1])
        
        return flag
    
    def get_carbs(data):
        flag = []
        for entry in data:
            flag.append(entry[2])
        
        return flag
    
    def get_fat(data):
        flag = []
        for entry in data:
            flag.append(entry[3])
        
        return flag
    
    def get_sugar(data):
        flag = []
        for entry in data:
            flag.append(entry[4])
        
        return flag

    def get_cholestrol(data):
        flag = []
        for entry in data:
            flag.append(entry[5])
        
        return flag
    
    def generate_pdf(filename):
                # initializing variables with values
        fileName = filename
        documentTitle = 'BEFIT Nutrional Analysis'
        title = 'BEfit'
        subTitle = 'Nutritional report'
        textLines = [
            f'The Following graphs represt the food intake of the user',
            f'',
        ]
        image1 = 'calories_plot.png'
        image2 = 'carbohydrates_plot.png'
        image3 = 'fat_plot.png'
        image4 = 'sugar_plot.png'
        image5 = 'cholestrol_plot.png'
        
        pdf = canvas.Canvas(fileName)
        
        pdf.setTitle(documentTitle)
        
        pdf.drawCentredString(300, 770, title)
        
        pdf.setFillColorRGB(0, 0, 255)
        pdf.setFont("Courier-Bold", 24)
        pdf.drawCentredString(290, 720, subTitle)
        
        # drawing a line
        pdf.line(30, 710, 550, 710)
        
        # creating a multiline text using 
        # textline and for loop
        text = pdf.beginText(40, 680)
        text.setFont("Courier", 18)
        text.setFillColor(colors.red)
        for line in textLines:
            text.textLine(line)
        pdf.drawText(text)
        
        # drawing a image at the 
        # specified (x.y) position
        pdf.drawInlineImage(image1, 50, 100, 400, 450, preserveAspectRatio=True)
        pdf.drawInlineImage(image2, 50, 100, 400, 450, preserveAspectRatio=True)
        pdf.drawInlineImage(image3, 50, 100, 400, 450, preserveAspectRatio=True)
        pdf.drawInlineImage(image4, 50, 100, 400, 450, preserveAspectRatio=True)
        pdf.drawInlineImage(image5, 50, 100, 400, 450, preserveAspectRatio=True)
        
        # saving the pdf
        pdf.save()

        
    
    
# if __name__ == "__main__":
    # print(BFUtils.check_userValidity("ollie"))
#     user1_utils = Utils(45, 60, 1.64, 'rick')
#     us1_bmi = user1_utils.calc_bmi('m')
#     print(f"bmi: {us1_bmi}")
#     us1_status = user1_utils.bmi_class()
#     print(f"status: {us1_status}")
    # ingredient = "mashed potatoes"
#     newString = BFUtils.remove_space(ingredient)
#     print(ingredient)
#     print(newString)
    # BFUtils.generate_pdf("example.pdf")
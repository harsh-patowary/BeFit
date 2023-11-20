# Util Contents
import os
import csv
import numpy as np
class UserData:
    
    _age = None
    _weight = None
    _height = None
    _name = None
    _bmi = None
    _unit = None
    _calories_intake = None
    _goal_range = None
    
    def __init__(self, a, w, h, n, u, gr):
        self._age = a
        self._weight = float(w)
        self._height = float(h)
        self._name = n
        self._unit = u
        self._unit = gr
    
    
    def calc_bmi(self):
        if self._unit == 'm':
            self._bmi = self._weight / pow(self._height, 2)
            return self._bmi 
        elif self._unit == 'i':
            self._bmi  = (703 * self._weight)/ pow(self._height, 2)
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
        return [self._name, self._age, self._height, self._weight, self._unit, round(self._bmi), self._calories_intake]
      
      
       
class BFUtils:
    
    def remove_space(ingr):
        newStr = ""
        for ch in ingr:
            if ch == " ":
                ch = "%20"
            newStr+=ch
        return newStr
    
    def insert_data(file_path, data):
        file_exists = os.path.isfile("data.csv")
        with open("data.csv", "a", newline='') as file:
            csvwriter = csv.writer(file)
                
            if not file_exists:
                header = ['Name', 'Age', 'height', 'weight', 'unit', 'bmi', 'calories']
                csvwriter.writerow(header)
                    
            csvwriter.writerow(data)#
            
    def cal_perGram(cal, weigh):
        return float(cal/weigh)
        
    
    
# if __name__ == "__main__":
#     user1_utils = Utils(45, 60, 1.64, 'rick')
#     us1_bmi = user1_utils.calc_bmi('m')
#     print(f"bmi: {us1_bmi}")
#     us1_status = user1_utils.bmi_class()
#     print(f"status: {us1_status}")
    # ingredient = "mashed potatoes"
#     newString = BFUtils.remove_space(ingredient)
#     print(ingredient)
#     print(newString)
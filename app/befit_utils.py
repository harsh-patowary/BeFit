# Util Contents

class UserData:
    
    _age = None
    _weight = None
    _height = None
    _name = None
    _bmi = None
    _unit = None
    
    def __init__(self, a, w, h, n, u):
        self._age = a
        self._weight = float(w)
        self._height = float(h)
        self._name = n
        self._unit = u
    
    
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
           elif self._bmi  <=30:
               return 'overweight'
           else:
               return 'very overweight'
        else:
            return 'Invalid Range Error:BMI/RA23'
       

# if __name__ == "__main__":
#     user1_utils = Utils(45, 60, 1.64, 'rick')
#     us1_bmi = user1_utils.calc_bmi('m')
#     print(f"bmi: {us1_bmi}")
#     us1_status = user1_utils.bmi_class()
#     print(f"status: {us1_status}")
    
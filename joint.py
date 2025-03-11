import tkinter.__init__ .Variable as Variable

class  Joint(Variable):
    def __init__(self, name, value, min, max, step):
        self.name = name
        self.value = value
        self.min = min
        self.max = max
        self.step = step
        
    def get_name(self):

    def set_value(self, value):
        self.value = value

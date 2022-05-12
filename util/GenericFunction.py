from datetime import datetime
import time


class GenericFunction:

    def __init__(self):
         pass

    def generated_value(self, value):
        value = value.split("()")
        return self.switch(value[0])

    def switch(self, value):
        switcher = {
            "DANASNJIDAN": lambda: self.generated_date(),
            "DANASNJEVREME": lambda: self.generated_date_and_time(),
            "GENBROJ": lambda: self.generated_number(),
            "KREIRAJ": lambda: self.write_variables(value),
            "CITAJ": lambda: self.read_variables()

        }
        func = switcher.get(value, lambda: self.def_value(value))
        return func()

    def generated_date(self):
        now = datetime.now()
        return now.strftime("%d.%m.%Y")

    def generated_date_and_time(self):
        now = datetime.now()
        return now.strftime("%d.%m.%Y %H:%M:%S")

    def generated_number(self):
        return 'AT' + str(round(time.time() * 1000))

    #upispromenjljive NEJASNO
    def write_variables(self, value):
        gen_number = self.generated_number()
        value = gen_number
        return value

    def def_value(self, value):
        return value

'''s = SpecialFunction()
print("DATE:", s.generated_value("DANASNJIDAN()"))
print("DATETIME:", s.generated_value("DANASNJEVREME()"))
print("GEN_NUMBER",  s.generated_value("GENBROJ()"))'''




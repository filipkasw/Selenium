import re


class Parser:
    
    def __init__(self):
        pass
    
    def parseLoginData(self, text):
        a = text.replace(" ", "")
        data = a.split(',')
        return data

    def split_strip(self, data, criteria):
        return [x.strip() for x in data.split(criteria)]

    def split_by_line(self, value):
        list = re.split(', |\n', value)
        return list

    def delimit_element_from_value(self, value):
        list = re.split(': ', value)
        return list

    def pripere_btn_parameter(self, pp2):
        print("Neobradjeni:", pp2)
        lines = len(pp2.splitlines())
        print("Broj linija", lines)
        if lines > 1:
            print("line")
            prepare_parameter = re.split("\n", pp2)
        else:
            print("zapeta")
            prepare_parameter = re.split(", ", pp2)
        print("Pripremljeni: ", prepare_parameter)
        data = []
        for y in prepare_parameter:
            if ':' in y:
                a = y.split(': ')
                data.append(a[0])
            else:
                data.append(y)
        return data








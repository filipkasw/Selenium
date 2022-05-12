from selenium_python.util.ParseParameter import Parser
from colorama import Fore, Back, Style


class FormSwitch:

    def __init__(self,logger, dominus_action):
        self.logg = logger
        self.da = dominus_action
        self.par = Parser()

    def process_form(self, list_parameter):
        self.logg.log_INFO("FormSwitch", "process_form: ", list_parameter)
        self.da.find_highest_z_index(True)
        #field_commands = self.par.split_by_line(pp2)
        #print("Ukupna lista za rad:",  list_parameter)
        for i in list_parameter:
                list_values = self.par.split_strip(i, ": ")
                self.logg.log_INFO("------------------------------------")
                self.logg.log_INFO(Fore.GREEN  +"Values pripere for swichunos FORM: ", i , " "+Style.RESET_ALL)
                self.logg.log_INFO("------------------------------------")
                self.swichunos(list_values)

    def swichunos(self, list_values):
        switcher = {
            "/d": lambda: self.da.drop_down_by_label(list_values[1],list_values[2]),
            "//": lambda: self.form_btns(list_values),
            "/": lambda: self.da.drop_down_filter(list_values[2], list_values[1], "editForm:")
            ##"veleprodajna_input": lambda: self.da.proba(list_values)

            #"Uneli ste podatak": self.da.error_summary(list_values[0].lower())
        }
        func = switcher.get(list_values[0].lower(), lambda: self.default_unos(list_values))
        func()

    def form_btns(self, list_values):
        if len(list_values) > 2:
            self.da.form_btns(list_values[1].lower(), list_values[2].lower())
        else:
            self.da.form_btns(list_values[1].lower(), "")



    def default_unos(self, list_values):
        self.logg.log_INFO("FormSwitch", "default_unos: ", list_values)
        if 'close' in list_values[1] or 'odustani' in list_values[1] :
            self.logg.log_INFO("FormSwitch", "default_unos: ", "CLOSE")
            self.da.click_on_x()
        else:
            self.logg.log_INFO("FormSwitch", "default_unos: ", "SET")
            self.da.set_or_check_input(list_values)



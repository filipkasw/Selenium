import pandas as pd
from colorama import Fore, Style
from selenium_python.configuration.ReadJson import ReadJson


class ReadAT():

    def __init__(self, logger, ce):
        self.logg = logger
        self.pd = pd
        self.ce = ce
        self.jc = ReadJson("config.json")
        self.ja = ReadJson("action.json")
        #self.eve = events

    def processDataAndExecute(self, AT_name):
       file = self.pd.read_excel(self.jc.get_value("excel_folder") + AT_name, sheet_name=self.jc.get_value("excel_sheet"))
       self.logg.log_INFO("ReadExcel", "AUTOMATSKI TEST: " + AT_name)
       for index, row in file.iterrows():
           command = row[0]
           pp1 = row[1]
           pp2 = row[2]
           pp3 = row[3]
           self.logg.log_INFO(Fore.LIGHTYELLOW_EX + "**********", str(index+2) + '. ' + command,"**********" + Style.RESET_ALL)
           self.setValueToConfig(AT_name, index, command, pp1, pp2)
           self.switch(command, pp1, pp2, pp3)

    def switch(self, command, pp1, pp2, pp3):
        switcher = {
            # WEB
           # "korak": lambda: self.logg.log_INFO(Fore.YELLOW + "Lambda na KORAK komandi" + Style.RESET_ALL),
            "login": lambda: self.ce.login(pp1, pp2),
           # "logincas:": lambda: self.eve.CasLogin(pp1),  # ovo nemam pojma sta je, pitaj
            "aplikacija": lambda: self.ce.select_app_orgjed(pp1, pp2),
            "promeni": lambda: self.ce.change_app_orgjed(pp1, pp2),
          #  "provera": lambda: self.eve.provera(pp1),
           # "dugmici": lambda: self.eve.databuttons(pp1, pp2),
           # "dugmići": lambda: self.eve.databuttons(pp1, pp2),
            "forma": lambda: self.ce.forma(pp1, pp2),
            "navigacija": lambda: self.ce.navigacija(pp1, pp2),
            "script": lambda: self.ce.execute_script(pp1, pp2),
            "putanja": lambda: self.ce.putanja(pp1),
            "toolbar": lambda: self.ce.toolbar(pp1, pp2),
            "lookup": lambda: self.ce.lookup(pp1, pp2),
            "dokument": lambda: self.ce.dokument(pp1, pp2),
            "stavka": lambda: self.ce.stavka(pp1, pp2, pp3),
            # FILE
           # "openfile": lambda: self.eve.open_file(pp1),
           # "savefile": lambda: self.eve.save_file(pp1, pp2),
           # "proverafajla": lambda: self.eve.compare_files(pp1, pp2),
            # SQL
            "sql": lambda: self.ce.sql_compare(pp1, pp2)
            # "close": lambda : self.eve.close_test(),
        }
        func = switcher.get(command.lower(), lambda: self.logg.log_INFO(Fore.YELLOW + "Komanda nije implementirana" + Style.RESET_ALL))
        return func()


    def setValueToConfig(self, at_name, index_command, command, parameter1, parameter2):
        self.ja.set_value("current_at", at_name)
        self.ja.set_value("index_command", index_command + 2)
        self.ja.set_value("current_command", command)
        self.ja.set_value("current_parameter1", parameter1)
        self.ja.set_value("current_parameter2", parameter2)


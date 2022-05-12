from selenium_python.util.ParseParameter import Parser
from selenium_python.configuration.ReadJson import ReadJson
from selenium_python.script.ScriptController import ScriptController
from selenium_python.file.SQL_CSV import SQL_CSV
from selenium_python.web.ToolbarSwitch import ToolbarSwitch
from selenium_python.web.FormSwitch import FormSwitch
from selenium_python.web.ButtonsInside import ButttonsInside
from selenium_python.db.Oracle import OracleDB
from selenium_python.web.ButtonOutside import ButtonOutside
from selenium_python.db.Oracle import OracleDB
import numpy as np


class CommandEvent():

    def __init__(self, logger, dominus_action):
        self.logg = logger
        self.da = dominus_action
        self.pd = Parser()
        self.ja = ReadJson("action.json")
        self.sc = ScriptController(self.logg)
        self.scsv = SQL_CSV(logger)
        self.form = FormSwitch(self.logg, self.da)
        self.dbtn = ButttonsInside(self.logg, self.da)
        self.outsidebtn = ButtonOutside(self.logg, self.da)
        self.oradb = OracleDB(self.logg)
       # self.sel = selenium
       # self.log = logika
      #  self.parser = Parser()
       # self.img = img
       # self.f = Files(self.sel)

    def login(self, url, credentials="adm,service"):
        data = self.pd.parseLoginData(credentials)
        self.logg.log_INFO("CommandEvent, PRIPREMLJENI PODACI, login:", data[0], data[1])
        return self.da.login_to_dominus(url, data[0], data[1])

    def select_app_orgjed(self, application=None, organization=None, mesto="start:"):
        if application:
            self.logg.log_INFO("CommandEvent", "IZBORA APLIKACIJE: ", application)
            self.da.drop_down_filter(application, 'aplikacija', mesto)
        if organization:
            self.logg.log_INFO("CommandEvent", "IZBOR ORG_JED: ", organization)
            self.da.drop_down_filter(str(organization), 'orgjed', mesto)
        if mesto == "start:":
            self.logg.log_INFO("CommandEvent", "START")
            self.da.click_dominus_taster('Start')
        else:
            self.logg.log_INFO("CommandEvent", "POTVRDI")
            self.da.click_dominus_taster('Potvrdi')
        self.da.check_app_org(application, organization)

    def change_app_orgjed(self, pp1, pp2):
        self.da.click_app_org_container()
        self.select_app_orgjed(pp1, pp2, "sesijaForm:")

    def putanja(self, pp1):
        self.ja.set_value("current_path", pp1)
        list = self.pd.split_strip(pp1, ", ")
        self.logg.log_INFO("CommandEvent", "putanja", "data_list: ", list)
        self.da.menubar_container(list)

    def lookup(self, pp1, pp2):
        list = self.pd.split_by_line(pp1)
        self.da.lookup_window(list)
        list_btn_action = self.pd.pripere_btn_parameter(pp2)
        tip_dugmica = ""
        data = self.oradb.execute_query("SELECT * FROM db_parametri WHERE sifra = 'izdvojeniRowB'")
        for i in data:
            tip_dugmica = i[1]
        if tip_dugmica == "D":
            self.outsidebtn.action_on_btn(list_btn_action)
        if tip_dugmica == "N":
            self.dbtn.action_on_btn(list_btn_action)

    #print(list_btn_action)
        #self.da.data_buttons(list_btn_action)
    def execute_script(self, pp1, pp2):
        self.sc.find_script_and_excute(pp1, pp2)

    def sql_compare(self, pp1, pp2):
        self.scsv.sql_to_compare(pp1, pp2)

    def toolbar(self, pp1, pp2):
        list_command = pp1.splitlines()
        self.logg.log_INFO("CommandEvent", "toolbar", "data_list TOOLBAR: ", list_command)
        ts = ToolbarSwitch(self.logg, self.da)
        ts.toolbar_action(list_command)
        print("-------------------------------------", pp2)
        if str(pp2) != "nan":
            self.logg.log_INFO("CommandEvent", "toolbar", "data_list FORM: ", list_command)
            list_form = pp2.splitlines()
            form = FormSwitch(self.logg, self.da)
            form.process_form(list_form)

    def forma(self, pp1, pp2):
        list_form = pp2.splitlines()
        form = FormSwitch(self.logg, self.da)
        form.process_form(list_form)

    def dokument(self, pp1, pp2):
        list_command = pp1.splitlines()
        self.logg.log_INFO("CommandEvent", "DOKUMENT", "data_list DOKUMENT: ", list_command)
        ts = ToolbarSwitch(self.logg, self.da)
        ts.toolbar_action(list_command)
        #print("-------------------------------------", pp2)
        if str(pp2) != "nan":
            list_form = pp2.splitlines()
            self.logg.log_INFO("CommandEvent", "DOKUMENT", "data_list FORM: ", list_form)
            self.form.process_form(list_form)

    def stavka(self, pp1,pp2,pp3):
        if str(pp1) != "nan":
            list_command = pp1.splitlines()
            self.logg.log_INFO("CommandEvent", "STAVKA", "data_list STAVKA: ", list_command)
            ts = ToolbarSwitch(self.logg, self.da)
            ts.toolbar_action(list_command)

        if str(pp2) != "nan":
            list_form = pp2.splitlines()
            self.logg.log_INFO("CommandEvent", "STAVKA", "data_list FORM: ", list_form)
            #form = FormSwitch(self.logg, self.da)
            self.form.process_form(list_form)

    def navigacija(self, pp1, pp2):
        self.logg.log_INFO("CommandEvent", "NAVIGACIJA", "VALUE: ", pp1)
        self.da.navigation_click_on(pp1)
        if str(pp2) != "nan":
            list_form = pp2.splitlines()
            self.logg.log_INFO("CommandEvent", "DOKUMENT", "data_list FORM: ", list_form)
            form = FormSwitch(self.logg, self.da)
            form.process_form(list_form)






















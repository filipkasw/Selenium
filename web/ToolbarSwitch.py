from selenium_python.util.ParseParameter import Parser
class ToolbarSwitch:

    def __init__(self,logger, dominus_action):
        self.logg = logger
        self.da = dominus_action
        self.par = Parser()

    def toolbar_action(self, list_parameter):
        self.logg.log_INFO("ToolbarSwitch", "toolbar_action: ", list_parameter)
        #form = self.log.find_highest_z_index()
        #field_commands = self.par.split_by_line(pp2)
        print("Ukupna lista za rad:",  list_parameter)
        for i in list_parameter:
                values = self.par.split_strip(i, ":")
                self.logg.log_INFO("------------------------------------")
                self.logg.log_INFO("Values pripere for swichunos TOOLBAR: ", values)
                self.logg.log_INFO("------------------------------------")
                self.swichunos(values)


    def swichunos(self, values):
        switcher = {
            #"brisanje": lambda: self.da.toolbar_btn(values[0].lower()),
            "novi": lambda: self.da.toolbar_btn(values[0].lower()),
            "proknjiži" : lambda: self.da.toolbar_btn(values[0].lower()),
            "//": lambda: self.da.toolbar_btn(values[1].lower()),
            "/a": lambda: self.da.click_by_text(values[1]),
            "/d": lambda: self.da.drop_down_by_label(values[1],values[2])
        }
        func = switcher.get(values[0].lower(), print("Nije pronadjena kljucna rec u switcheru...TOOLSWITCH"))
        func()
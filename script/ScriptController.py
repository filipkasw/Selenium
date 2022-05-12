from selenium_python.script.VLP.cenovnici001_vratiCene import VLP as vlp
from selenium_python.script.VLP.excelScript import excelScript


class ScriptController:

    def __init__(self, logg):
        self.logg = logg
        self.vlp = vlp(logg)
        self.es = excelScript(logg)

    def find_script_and_excute(self, pp1, pp2):
        pp1 = "Parameter1 je prazan" if str(pp1) == "nan" else pp1
        pp2 = "Parameter2 je prazan" if str(pp2) == "nan" else pp2
        self.logg.log_INFO("ScriptController", "find_script_and_excute")
        self.logg.log_INFO("ScriptController", "NAZIV SCRIPTE: ", pp1)
        method_name = pp1
        parameters_db = pp2.split(", ")
        a = self.switch_find_and_execute(method_name, parameters_db)
        return a

    def switch_find_and_execute(self, method_name, parametera_db):
        self.logg.log_INFO("ScriptController", "Ulazak u switcher i traženje metode: " + method_name)
        switcher = {
           #VLP
            'vratiCene_cenProdaje': lambda: self.vlp.vratiCene_cenProdaje(parametera_db[0], parametera_db[1]),
            'updateParametara': lambda: self.es.VratiKalkulacijaRuc(parametera_db[2])
        }
        fun = switcher.get(method_name, lambda: print("Nije pronadjena skripta"))
        return fun()
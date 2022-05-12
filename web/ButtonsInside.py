from selenium_python.util.ParseParameter import Parser
from colorama import Fore, Back, Style


class ButttonsInside:

    def __init__(self, logger, dominus_action):
        self.logg = logger
        self.da = dominus_action
        self.par = Parser()

    def action_on_btn(self, list_parameter):
        self.logg.log_INFO("ButttonsInside", "action_on_btn: ", list_parameter)
        for i in list_parameter:
                list_values = self.par.split_strip(i, "/")
                for j in list_values:
                    print("000000000000000000000000", list_values)
                    self.logg.log_INFO("------------------------------------")
                    self.logg.log_INFO(Fore.GREEN + "Values pripere for swichunos BUTTONS: ", j, " " + Style.RESET_ALL)
                    self.logg.log_INFO("------------------------------------")
                    self.swichunos(j)

    def swichunos(self, key_word):
        switcher = {
            "geer": lambda: self.find_btn_and_click("//div[contains(@class,'table')]//*[contains(@class,'fa fa-gear')]"),
            "otvaranje": lambda: self.find_btn_and_click("//div[contains(@class,'aswoverlaypanel')]//*[contains(text(),'Otvaranje')] | //div[contains(@class,'table')]//*[contains(@class,'fa fa-unlock')]"),
            "zatvaranje": lambda: self.find_btn_and_click("//div[contains(@class,'aswoverlaypanel')]//*[contains(text(),'Zatvaranje')] | //div[contains(@class,'table')]//*[contains(@class,'fa fa-lock')]"),
            "da": lambda: self.find_btn_and_click("//button//*[contains(@class,'fa fa-check') or contains(@class, 'fa fa-check-square-o') or contains(text(), 'Da')]"),
            "edit": lambda: self.find_btn_and_click("//div[contains(@class,'table')]//*[contains(@class,'fa fa-pencil') or contains(@class, 'asw_edit_icon')]"),
            "detalj": lambda: self.find_btn_and_click("//div[contains(@class,'table')]//*[contains(@class,'fa fa-eye') or contains(@class, 'fa fa-eyel') or contains(@class, 'asw_view_icon')]"),
            "stavke": lambda: self.find_btn_and_click("//div[contains(@class,'table')]//*[contains(@class,'fa fa-sitemap') or contains(@class, 'asw_masterdetail_icon')]"),
            "brisanje": lambda: self.find_btn_and_click("//div[contains(@class,'table')]//*[contains(@class,'fa fa-trash') or contains(@class, 'asw_delete_icon')]"),
            "brisisve": lambda: self.da.delete_all_result("//div[contains(@class,'table')]//*[contains(@class,'fa fa-trash') or contains(@class, 'asw_delete_icon')]", "//button//*[contains(@class,'fa fa-check') or contains(@class, 'fa fa-check-square-o') or contains(text(), 'Da')]"),
            "brisisve()": lambda: self.da.delete_all_result("//div[contains(@class,'table')]//*[contains(@class,'fa fa-trash') or contains(@class, 'asw_delete_icon')]","//button//*[contains(@class,'fa fa-check') or contains(@class, 'fa fa-check-square-o') or contains(text(), 'Da')]"),
            "potvrdi": lambda: self.find_btn_and_click("//div[contains(@class,'table')]//*[contains(@class,'fa fa-check') or contains(@class, 'fa fa-check-square-o')]"),
            "potvrda": lambda: self.find_btn_and_click("//div[contains(@class,'table')]//*[contains(@class,'fa fa-check') or contains(@class, 'fa fa-check-square-o')]"),
            "close": lambda: self.da.click_on_x(),
            "stampa1": lambda: self.find_btn_and_click("//div[contains(@class,'table')]//*[contains(@class,'fa fa-print')]"),
            "kopiranje1": lambda: self.find_btn_and_click("//div[contains(@class,'table')]//*[contains(@class,'fa fa-copy')]"),
            "vezivanje1": lambda: self.find_btn_and_click("//div[contains(@class,'table')]//*[contains(@class,'fa fa-chain')]"),
            "kalkulator1": lambda: self.find_btn_and_click("//div[contains(@class,'table')]//*[contains(@class,'fa fa-calculator')]")


        }
        func = switcher.get(key_word.lower(), lambda:  self.logg.log_INFO(Fore.RED + " NEMA BUTTONS XPATH UPITA " +Style.RESET_ALL) )
        func()

    def find_btn_and_click(self, xpath_query):
        self.da.datatable_buttons(xpath_query)




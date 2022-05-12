from selenium_python.util.ParseParameter import Parser


class ButtonOutside:

    def __init__(self, log, dominus_action):
        self.log = log
        self.da = dominus_action
        self.par = Parser()

    def action_on_btn(self, parameters):
        self.log.log_INFO("ButtonOutside", "action_on_btn:", parameters)
        for i in parameters:
            parameter_value = self.par.split_strip(i, "/")
            for j in parameter_value:
                self.swichunos(j)

    def swichunos(self, elem):
        switcher = {
            "izmena": lambda: self.find_btn_and_click("//div[contains(@class,'fieldset')]//*[contains(@class,'fa fa-pencil')]"),
            "detalj": lambda: self.find_btn_and_click("//div[contains(@class,'fieldset')]//*[contains(@class,'fa fa-eye')]"),
            "brisanje": lambda: self.find_btn_and_click("//div[contains(@class,'fieldset')]//*[contains(@class,'fa fa-trash-o')]"),
            "geer": lambda: self.find_btn_and_click("//div[contains(@class,'ui-fieldset-content')]//*[contains(@class,'fa fa-gear')]"),
            "prava": lambda: self.find_btn_and_click("//div[contains(@class,'ui-fieldset-content')]//*[contains(@class,'fa fa-chain')]"),
            "dodela": lambda: self.find_btn_and_click("//div[contains(@class,'ui-fieldset-content')]//*[contains(@class,'fa fa-plus')]"),
            "odblokiranje": lambda: self.find_btn_and_click("//div[contains(@class,'ui-fieldset-content')]//*[contains(@class,'fa fa-times')]"),
            "zahtev_za_promenu_lozinke": lambda: self.find_btn_and_click("//div[contains(@class,'ui-fieldset-content')]//*[contains(@class,'fa fa-tag')]"),
            "kopiranje": lambda: self.find_btn_and_click("//div[contains(@class, 'ui-fieldset-content')]//*[contains(@class, 'fa fa-print')]"),
            "potvrda_dokumenta": lambda: self.find_btn_and_click("//div[contains(@class, 'ui-fieldset-content')]//*[contains(@class, 'fa fa-check-square-o')]"),
            "otvaranje": lambda: self.find_btn_and_click("//div[contains(@class, 'ui-fieldset-content')]//*[contains(@class, 'fa fa-unlock')]"),
            "podredjeni": lambda: self.find_btn_and_click("//div[contains(@class, 'ui-fieldset-content')]//*[contains(@class, 'fa fa-sitemap')]"),
            "zatvaranje": lambda: self.find_btn_and_click("//div[contains(@class, 'ui-fieldset-content')]//*[contains(@class, 'fa fa-lock')]"),
            "specifikacija_cekova": lambda: self.find_btn_and_click("//div[contains(@class, 'ui-fieldset-content')]//*[contains(@class, 'fa fa-file-o')]"),
            "uvid_u_stanje_blagajne": lambda: self.find_btn_and_click("//div[contains(@class, 'ui-fieldset-content')]//*[contains(@class, 'fa fa-cubes')]"),
            "kopiranje_tekuceg_dokumenta": lambda: self.find_btn_and_click("//div[contains(@class, 'ui-fieldset-content')]//*[contains(@class, 'fa fa-copy')]"),
            "komentar": lambda: self.find_btn_and_click("//div[contains(@class, 'ui-fieldset-content')]//*[contains(@class, 'fa fa-comment-dots')]"),
            "ostalo": lambda: self.find_btn_and_click("//div[contains(@class, 'ui-fieldset-content')]//*[contains(@class, 'fa fa-ellipsis-h')]"),
            "storno": lambda: self.find_btn_and_click("//div[contains(@class, 'ui-fieldset-content')]//*[contains(@class, 'fa fa-close')]"),
            "podela_na_rate": lambda: self.find_btn_and_click("//div[contains(@class, 'ui-fieldset-content')]//*[contains(@class, 'fa fa-calculator')]"),
            "import": lambda: self.find_btn_and_click("//div[contains(@class, 'ui-fieldset-content')]//*[contains(@class, 'fa fa-sign-in')]"),
            "kasa_skonto": lambda: self.find_btn_and_click("//div[contains(@class, 'ui-fieldset-content')]//*[contains(@class, 'fa fa-percent')]")

        }
        func = switcher.get(elem.lower(), lambda: self.log.log_INFO("NEMA BUTTONS XPATH UPITA"))
        func()

    def find_btn_and_click(self, xpath_value):
        self.da.datatable_buttons(xpath_value, False)

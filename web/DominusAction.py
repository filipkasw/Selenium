#import time

#import sel
import time

from selenium.common.exceptions import NoSuchElementException
from selenium_python.exception.CustomException import UnexpectedElementDesplayed, BadCredentials,NoSuchElement, NoResultInTable, ErrorSummary, ComparisonNotCorrect
from selenium_python.configuration.ReadJson import ReadJson
from selenium_python.exception.CustomException import BadAppOrOrgJed
from selenium_python.util.ParseParameter import Parser
from selenium_python.util.GenericFunction import GenericFunction
from selenium_python.configuration.GlobalVariable import GlobalVariable


from colorama import Fore, Style
import re


class DominusAction():

    def __init__(self, logger, selenium):
        self.logg = logger
        self.sel = selenium
        self.ja = ReadJson("action.json")
        self.pd = Parser()
        self.gv = GlobalVariable()
        #self.log = logika
        #self.parser = Parser()
        #self.img = img
        #self.f = Files(self.sel)

    def login_to_dominus(self, url="http://t-rex:8891/dominus_testlilly/", username="adm", password="service"):
        self.logg.log_INFO("DominusAction", "login_to_dominus:", username, password)
        self.sel.getSelUrl(url)
        self.sel.set_value_to_input(self.sel.waitForNameElement(10, 'j_username'), username, True, False)
        self.sel.set_value_to_input(self.sel.waitForNameElement(10, 'j_password'), password, True, False)
        btn_prijava = self.dominus_taster('Prijava')
        self.sel.clickElement(btn_prijava)
        self.check_error_login("//*[contains(text(),'Neispravna lozinka')]")

    def dominus_taster(self, taster_text):
        self.logg.log_INFO("DominusAction", "dominus_taster:", "//button[.='" + taster_text + "']")
        btn = self.sel.waitForXpathElement(10, "//button[.='" + taster_text + "']")
        if btn:
            return btn
        else:
            raise NoSuchElementException

    def click_dominus_taster(self, taster_text):
        return self.sel.clickElement(self.dominus_taster(taster_text), True)

    def check_error_login(self, xpath_query):
        try:
            self.logg.log_INFO("DominusAction", "check_error:", xpath_query)
            return self.sel.is_error_desplayed(xpath_query)
        except UnexpectedElementDesplayed:
            self.sel.stopDriver()
            raise BadCredentials()

    def drop_down_filter(self, app, tip, mesto):
        self.logg.log_INFO("FILTER U DROP_DOWN: ", mesto, tip, app)
        self.sel.clickElement(self.sel.waitForIdElement(10, mesto + tip + "_label"))
        self.sel.set_value_to_input(self.sel.waitForIdElement(10, mesto + tip + "_filter"), app, True, True)

    def drop_down_filter_using_xpath(self, app, tip, mesto):
        self.logg.log_INFO("FILTER U DROP_DOWN USING XPATH: ", mesto, tip, app)
        xpath_query_label = "//*[@id='" + mesto + tip + "_label" +  "']"

        self.sel.clickElement(self.sel.findElem(xpath_query_label, True, 10))
        self.sel.set_value_to_input(self.sel.waitForIdElement(10, mesto + tip + "_filter"), app, True, True)

    def check_app_org(self, app=None, org=None):
        app = app.upper().replace("-", "").replace("(", "").replace(")", "").replace("  ", " ")
        org = org.upper().replace("-", "").replace("(", "").replace(")", "").replace("  ", " ")
        contan_text = self.app_org_container().text.upper().replace("-", "").replace("(", "").replace(")", "").replace("  ", " ")
        self.logg.log_INFO("PROVERA APP I ORG: ", app, org, contan_text)
        if not app in contan_text and org in contan_text:
            self.logg.log_INFO("BadAppOrOrgJed", app, org, contan_text)
            raise BadAppOrOrgJed( app +" i " + org, contan_text)
        else:
            self.logg.log_INFO("POSLI PROVERU", app, org, contan_text)
            self.ja.set_value("current_app", app)
            self.ja.set_value("current_orgjed", org)

    def app_org_container(self):
        tag_a = self.sel.findElem("//*[@id='izmenaAplOrgjed']", True, 5)
        self.logg.log_INFO("APP i ORG CONTAINER CONTENT: ", tag_a.text)
        return tag_a

    def click_app_org_container(self):
        self.logg.log_INFO("DominusAction", "click_app_org_container")
        self.sel.clickElement(self.app_org_container(), 5)

    def menubar_container(self, list_link):
        for i in list_link:
            self.sel.hoverAction(self.sel.findByLinkAndWait(i))
        self.sel.clickElement(self.sel.findByLinkAndWait(list_link[-1]))

    def lookup_window(self, value_list):
        self.find_highest_z_index()
        self.click_dominus_taster('Upit')
        self.find_highest_z_index()
        self.set_value_to_window(value_list)
        self.click_dominus_taster('Izvrši')
        self.get_result_datatable(True)

    def get_result_datatable(self, empty_is_negativ=False):
        try:
            self.sel.wait_loader()
            self.logg.log_INFO("SERVICE", "get_result_datatable")
            xpath_query = "//span[contains(@class,'ui-paginator-current')]"
            result_list = self.sel.waitForXpathElement(5, xpath_query).text.split(" / ")
            result = int(result_list[1])
            print("Result", result)
            if result == 0 and empty_is_negativ:
                self.sel.stopDriver()
                raise NoResultInTable
            else:

                return result
        except NoSuchElement as er:
            raise NoSuchElement(er.message, "element in :get_result_datatable()")

    def find_highest_z_index(self, change=True):
        try:
            self.logg.log_INFO("POSTAVLJANJE NAJVECEG Z-INDEX")
            max_form = 0
            default_index = 0
            # vrati samo driver na pocetni
            self.sel.returnToDefContent()
            # nadji elemente sve koji sada u driver(primer ima da vidi sve pop up prozore)
            all_forms = self.sel.findElements(
                "//div[(contains(@style,'z-index')) and (contains(@style,'display: block')) and not(contains(@class,'datepicker'))  and  not(contains(@class,'ui-tooltip')) and not(contains(@class,'growl-info growl'))]")
            if all_forms is None:
                return None
            for m, form in enumerate(all_forms):
                # proveri i ako nije prikazan daj mu ostavku
                if not form.is_displayed():
                    all_forms.pop(m)
                # iterira i kupim vrednost z_index_value
            if all_forms is not None and all_forms:
                for i, item in enumerate(all_forms):
                    z_index_value = int(self.sel.getAttributeValue(item, 'style').split("z-index:")[1].split(";")[0].strip())
                    print("--------------z", default_index)
                    print("++++++++++++++z", z_index_value)
                    if default_index < z_index_value:
                        default_index = z_index_value
                        max_form = i  # i je index vrednost forme
                if change:
                    tag = self.sel.getAttributeValue(all_forms[max_form], "tag") #tag proveri da li je iframe ili div to je poenta
                    self.check_for_iframe(tag)
                """if change:  # ako je true, onda proveri da li ima iframe, jer neki pop up prozori mogu da budu iframe
                    #l =  self.sel.getAttributeValue(all_forms[max_form], "id")
                    return self.sel.switchToFrame()
                # ako budemo naglasili da ne zelimo da proveri da li ima iframe onda samo zameni prozor all_forms[max_form]
                """
                return all_forms[max_form]
        except NoSuchElement:
            self.logg.log_INFO("NEMA PROZORA Z-INDEX")
            pass

    def reset_lookup(self):
        self.logg.log_INFO("RESET LOOKUP")
        btn_reset = self.sel.findElem("//a[contains(@id,'resetBtn') and contains(@class,'fa fa-refresh')]", True, 5)
        self.sel.clickElement(btn_reset, True)

    def set_value_to_window(self, values, reset=True):
        try:
            self.logg.log_INFO("OBRADA LOOKUP UPITA:", values)
            if reset:
                self.reset_lookup()
                time.sleep(5)
                print("Lista upita:",  values)
                for i, item in enumerate(values):
                    print("i:", i, "  item: ------", item, "-----------")
                    if i > 0:
                        btn_add = self.sel.findElem("//a[contains(@id,'addConditionBtn') and contains(@class,'fa fa-plus-circle')]")
                        self.sel.clickElement(btn_add, True)
                    data = self.pd.delimit_element_from_value(values[i])
                    self.drop_down(data[0], 'columnSelect' + str(i))
                    if '/' in data[1]:
                        self.drop_down(data[2], 'inputValue1Combo' + str(i))
                    else:
                        if i != 1:
                            my_btn = self.sel.findElem("//input[contains(@id,'searchForm:inputValue1') and contains(@id,'" + str(i) + "')]")
                            print(i)
                        else:
                            my_btn = self.sel.findElem("//input[contains(@id,'searchForm:inputValue1') and contains(@id,'" + str(i) + "') and not(contains(@id,'0'))]")
                        if ("(" in data[1]) and (")" in data[1]):
                            sp = GenericFunction()
                            data[1] = sp.generated_value(data[1])
                        self.sel.set_value_to_input(my_btn, data[1], True, True)
        except NoSuchElement as no:
            self.logg.log_ERROR("GREŠKA! OBRADA UPITA: ", values)
            raise NoSuchElement(no.message, "set_value_to_window")

    def drop_down(self, _drop, xpath_query):
        self.logg.log_INFO("DROP DOWN SPUSTANJE:", _drop, xpath_query)
        if "_label" in xpath_query or "_" in xpath_query:
            elem = self.sel.findElements("//label[contains(@id,'" + xpath_query + "')]", True, 10)[0]
            self.sel.clickWithPerform(elem)
            self.drop_down_select(_drop, xpath_query)
        else:
            text = xpath_query + "_label"
            elem = self.sel.findElements("//label[contains(@id,'" + text+ "') or contains(@id,'" + text.lower() + "')]", True, 10)[0]
            self.sel.clickWithPerform(elem)
            self.drop_down_select(_drop, xpath_query)

    def drop_down_select(self, drop, upit=""):
        temp = str(drop).split(">")
        print("+++++++++++++", temp)
        self.logg.log_INFO("DROP DOWN ODABIR:", drop, upit)
        if len(temp) > 1:
            print("Ovde 1")
            a = self.sel.findElements(
                "//div[contains(@id,'" + upit + "')]//div[contains(@class,'ui-selectonemenu-items-wrapper')]" +
                "//li[contains(@class,'selectonemenu-item-group') and .='" + temp[0] + "']" +
                "/following-sibling::li[.='" + temp[1] + "']")
        else:
            # b = "//input[contains(@id,'aswdatatable:searchForm:"+upit+"_filter')]"
            # q  ="//input[contains(@id,'aswdatatable:searchForm:"+upit+"_filter')]"
            # a  = self.sel.findElem(q, False, 3)
            # self.sel.set_value_to_input(a, drop, True, True)
            a = self.sel.findElements(
                "//div[contains(@class,'ui-selectonemenu-items-wrapper')]" +
                "//li[contains(.,'" + temp[0] + "') or contains(.,'" + temp[0].lower() + "') or contains(.,'" + temp[
                    0].capitalize() + "')]")
            if a:
                for i in a:
                    if i.text == drop or i.text.lower() == drop.lower():
                        return self.sel.clickElement(i, True)

    """def data_buttons(self, btn_action_list):
        # ovde se zakaci na bazu i proveri sa koji dugmicima radi
        stari = True
        for i in btn_action_list:
            self.logg.log_INFO("DominusAction", "data_buttons_action: ", i)
            if "bris" in i:
                comm_del = "brisanje/ Da"
                data = re.split('/ ', comm_del)
                self.logg.log_INFO("DominusAction", "GO to: delete_all_in_table: ", data)
                self.delete_all_in_table(data)
            else:
                act_list = re.split('/ ', i)
                self.logg.log_INFO("DominusAction", "GO to: data_buttons_action: ", act_list)
                self.get_result_datatable(True)
                self.data_buttons_action(act_list)

    def delete_all_in_table(self, data):
        self.logg.log_INFO("DominusAction", "delete_all_in_table")
        while self.get_result_datatable() > 0:
           self.data_buttons_action(data)

    def data_buttons_action(self, action_list):
        for j in action_list:
            self.logg.log_INFO("DominusAction", "ACTION: ", j)
            variables = self.gv.createRegular()
            located = True
            msg = ""
            if isinstance(variables[j], tuple):

                for a in variables[j]:
                    try:
                        xpath_query = "//div[contains(@class,'table')]//*[contains(@class,'" + a + "')] | //div[contains(@class,'aswoverlaypanel')]//*[contains(text(),'" +j.capitalize()+ "')] | //button//*[contains(@class,'" + a + "') or contains(text(), '" + j + "')] | //a//*[contains(@class,'" + a + "')]"
                        self.logg.log_INFO("DominusAction", "TUPLE: ", xpath_query)
                        first_btn = self.sel.findElem(xpath_query, True, 10)
                        if first_btn:
                            self.sel.clickElement(first_btn, True)
                            located = True
                            break
                    except NoSuchElement as e:
                        located = False
                        msg = e.message
                        self.logg.log_INFO(Fore.LIGHTYELLOW_EX + e.message + Style.RESET_ALL)

            else:
                try:
                    not_tuple = "//div[contains(@class,'table')]//*[contains(@class,'" + variables[j] + "')] | //div[contains(@class,'aswoverlaypanel')]//*[contains(text(),'" +j.capitalize()+ "')] | //button//*[contains(@class,'" + variables[j] + "') or contains(text(), '" + j + "')] | //a//*[contains(@class,'" + variables[j] + "')]"
                    self.logg.log_INFO("DominusAction", "NOT TUPLE: ", not_tuple)
                    # print("not tuple:", not_tuple)
                    f_btn = self.sel.findElem(not_tuple, True, 10)
                    self.sel.clickElement(f_btn, True)
                except NoSuchElement as no:
                    self.sel.stopDriver()
                    raise NoSuchElement("DUGMIC NIJE PRONADJEN! PROVERI PARAMETAR2 u AT", no.message, "")
            if not located:
                self.sel.stopDriver()
                raise NoSuchElement("DUGMIC NIJE PRONADJEN !!! PROVERI PARAMETAR2 u AT", msg, "")
        self.error_summary()"""

    def toolbar_btn(self, value):
        variables = self.gv.createRegular()
        located = True
        msg = ""
        if isinstance(variables[value], tuple):
            for a in variables[value]:
                try:
                    if a == 'fa fa-gear':
                        first_btn = self.sel.findElem("//div[contains(@class,'ui-toolbar')]//span[contains(@class,'" + a + "') and not(contains(@class,'fa fa-gears'))]",  True, 10)
                        if first_btn:
                            self.sel.clickElement(first_btn, True)
                            located = True
                            break
                    else:
                        first_btn = self.sel.findElem("//div[contains(@class,'ui-toolbar')]//span[contains(@class,'" + a + "')]",  True, 10)
                        if first_btn:
                            self.sel.clickElement(first_btn, True)
                            located = True
                            break
                except NoSuchElement as e:
                    located = False
                    msg = e.message
                    self.logg.log_INFO(Fore.LIGHTYELLOW_EX + e.message + Style.RESET_ALL)

        else:
            try:
                sec_btn = self.sel.findElem("//div[contains(@class,'ui-toolbar')]//span[contains(@class,'" + variables[value] + "')]", True, 5)
                self.sel.clickElement(sec_btn, True)
            except NoSuchElement as no:
                self.sel.stopDriver()
                raise NoSuchElement(" TOOLBAR DUGMIC NIJE PRONADJEN!", no.message, "")
        if not located:
            self.sel.stopDriver()
            raise NoSuchElement("TOOLBAR DUGMIC NIJE PRONADJEN !!!", msg, "")

    def error_summary(self, expected_mes=""):
        xpath_query = "//*[@id='errorForm:globalErrors']/div/ul/li/span | //*[@id='editForm:message']/div/ul/li/span"
        try:
            self.logg.log_INFO("DominusAction", "SUMMARY ERR, error_summary:", xpath_query)
            return self.sel.is_error_desplayed(xpath_query)
        except UnexpectedElementDesplayed:
            err_elem = self.sel.findElem(xpath_query, True, 2)
            err_text = err_elem.text
            if expected_mes == "":
                self.logg.log_INFO("DominusAction", "SUMMARY ERR, PRONADJEN!!!:", xpath_query)
                self.sel.hoverAction(err_elem)
                raise ErrorSummary("Greška: " + err_text)
            else:
                if expected_mes in err_text.lower():
                    self.logg.log_INFO("DominusAction", "PROSLO POREDJENJE, error_summary")
                    self.sel.hoverAction(err_elem)
                else:
                    raise ErrorSummary("Očekivana greška ne sadrži očekivan text:" + expected_mes)

    def click_by_text(self, text_value):
        self.logg.log_INFO("DominusAction", "click_by_text", text_value)
        #self.find_highest_z_index()
        web_element = self.sel.findByLinkAndWait(text_value)
        self.sel.clickElement(web_element, True)

    def drop_down_by_label(self, labela_name, text_value):
        self.logg.log_INFO("DominusAction", "drop_down_by_label", labela_name)
        label_not_replace = labela_name
        labela_replaced = labela_name.replace("_", "")
        labela = labela_replaced + "_label"
        drop_down = self.sel.findElem("//label[contains(@id,'" +labela.lower()+ "')] | //label[contains(@id,'" +label_not_replace.lower()+ "')]", True, 5)
        self.sel.clickElement(drop_down)
        self.drop_down_select(text_value)

    def set_or_check_input(self, list_values, check=False):
        self.logg.log_INFO("DominusAction", "fill_in_input: " +list_values[1], "Argument for XPATH: " + list_values[0])
        text = list_values[1] #vrednost koja ce biti setovana
        unput_field = self.find_input_on_form(list_values[0]) #vrednost za finElem
        if "(" and ")" in list_values[1]:
            new_value = GenericFunction().generated_value(list_values[1])
            text = new_value
        if check:
            if unput_field.get_attribute('value') != text:
                self.logg.log_INFO("Vrednosti unete posotjane i trazene nisu iste", text, unput_field.get_attribute('value'))
                raise ComparisonNotCorrect("Vrednosti iz testa: " +text + " i " + unput_field.get_attribute('value') + " nisu ISTE!!!")

        else:
            self.logg.log_INFO("DominusAction", "SETOVANJE VREDNOSTI: ", text)
            self.sel.set_value_to_input(unput_field, text, True, True)

    def set_or_check_input_script(self, list_values, check=False):
        self.logg.log_INFO("DominusAction", "fill_in_input: " +list_values[1], "Argument for XPATH: " + list_values[0])
        text = list_values[1] #vrednost koja ce biti setovana
        unput_field = self.find_input_on_form(list_values[0]) #vrednost za finElem
        if "(" and ")" in list_values[1]:
            new_value = GenericFunction().generated_value(list_values[1])
            text = new_value
        if check:
            if unput_field.get_attribute('value') != text:
                self.logg.log_INFO("Vrednosti unete posotjane i trazene nisu iste", text, unput_field.get_attribute('value'))
                raise ComparisonNotCorrect("Vrednosti iz testa: " +text + " i " + unput_field.get_attribute('value') + " nisu ISTE!!!")

        else:
            self.logg.log_INFO("DominusAction", "SETOVANJE VREDNOSTI: ", text)
            self.sel.set_value_to_input_script(unput_field, text, True, True)

    def find_input_on_form(self, value):
        self.logg.log_INFO("DominusAction", "find_input", value)
        if "_input" not in value:
            return self.find_input_by_label(value)
        else:
            return  self.find_input_by_suffix(value)

    def find_input_by_label(self, value):
        self.logg.log_INFO("DominusAction", "find_input_by_label: ", value)
        value = value.replace("_", "")
        id_value = "_label_" + value.lower()
        xpath_query = "//label[contains(@id, '" + id_value + "')]/following::input[1]"
        input_element = self.sel.findElem(xpath_query, False, 2)
        return input_element

    def find_input_by_suffix(self, value):
        self.logg.log_INFO("DominusAction", "find_input_by_suffix: ", value)
        suffix = ":" + value.strip()
        input_element = self.sel.findElem("//input[contains(@id,'" + suffix + "')] | //textarea[contains(@id,'" + suffix + "')]", False, 5)
        return input_element

    def click_on_x(self):
        x = self.sel.findElem("//a[contains(@class,'close')]", True, 5)
        self.sel.clickElement(x, True)
        #self.sel.returnToDefContent()


    def form_btns(self, value, expected_message=""):
        self.logg.log_INFO("DominusAction", "FORM_BTNS: ", value)
        variables = self.gv.createRegular()
        located = True
        msg = ""
        if isinstance(variables[value], tuple):
            for a in variables[value]:
                try:
                    xpath_query = "//*[contains(@class,'" + a + "')]"
                    first_btn = self.sel.findElem(xpath_query,  True, 10)
                    if first_btn:
                        self.sel.clickElement(first_btn, True)
                        located = True
                        break
                except NoSuchElement as e:
                    located = False
                    msg = e.message
                    self.logg.log_INFO(Fore.LIGHTYELLOW_EX + e.message + Style.RESET_ALL)

        else:
            try:
                xpath_query = "//*[contains(@class,'" + variables[value] + "')]"
                sec_btn = self.sel.findElem(xpath_query, True, 5)
                self.sel.clickElement(sec_btn, True)
            except NoSuchElement as no:
                self.sel.stopDriver()
                raise NoSuchElement("DUGMIC NA FORMI NIJE PRONADJEN!", no.message, "")
        if not located:
            self.sel.stopDriver()
            raise NoSuchElement("DUGMIC NA FORMI NIJE PRONADJEN !!!", msg, "")
        if value == "stavke" or value == "dalje":
            print("********************", "STAVKE I DALJE")
            self.find_highest_z_index()
            self.error_summary(expected_message)
        else:
            self.error_summary(expected_message)
            self.sel.returnToDefContent()

    def navigation_click_on(self, text_value):
        self.sel.returnToDefContent()
        text_value = text_value.strip()
        #self.find_highest_z_index()
        xpath_query = "//div[@id='current-position-container-target']//a[contains(text(),'" + text_value + "')]"
        elem = self.sel.findElem(xpath_query)
        self.sel.clickElement(elem, True)

    def datatable_buttons(self, xpath_query, is_inside=True):
        if is_inside:
            elem = self.sel.findElem(xpath_query)
            self.sel.clickElement(elem, True)
            self.error_summary()
        else:
            self.sel.clickElement("//span[contains(@class, 'ui-button-icon-left ui-icon ui-c fa fa-search')]")
            select_element = "//div[contains(@class, 'ui-datatable-scrollable-body')]//*[contains(@class, 'ui-widget-content ui-datatable-odd ui-datatable-selectable')]"
            self.sel.clickElement(select_element)
            elem = self.sel.findElem(xpath_query)
            self.sel.clickElement(elem, True)
            self.error_summary()

    def delete_all_result(self, xpath_query_trash, xpath_query_confirm ):
        self.logg.log_INFO("DominusAction", "delete_all_result")
        while self.get_result_datatable() > 0:
            self.datatable_buttons(xpath_query_trash)
            self.datatable_buttons(xpath_query_confirm)
        self.sel.returnToDefContent()














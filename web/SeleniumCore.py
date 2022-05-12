import time
from selenium import webdriver as webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import StaleElementReferenceException
from selenium_python.configuration.ReadJson import ReadJson
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_python.exception.CustomException import UnexpectedElementDesplayed,NoSuchElement
from selenium.webdriver.common.action_chains import ActionChains
from selenium_python.web.Photo import ScreenShoot
from selenium.webdriver.remote.webelement import WebElement
import re
from selenium_python.util.Logger import Logger as log


class SeleniumCore():

    def __init__(self, logg):
        self.log = logg
        self.jc = ReadJson("config.json")
        self.ja = ReadJson("action.json")
        self.directory = self.jc.get_value("download_directory")
        options = webdriver.ChromeOptions()
        options.add_argument(
            "user-agent='Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36'")
        prefs = {'profile.default_content_settings.popups': 0,
                 'plugins.always_open_pdf_externally': True,
                 'download.default_directory': self.directory}
        options.add_experimental_option('prefs', prefs)
        self.driver = webdriver.Chrome(options=options, executable_path=self.jc.get_value("chrome_driver"))
        self.log.log_INFO("SeleniumCore", "DRIVER", "Driver je pokrenut...")
        self.driver.implicitly_wait(10)
        self.driver.maximize_window()
        self.ss = ScreenShoot(self.driver, self.log)

    def getSelUrl(self, url):
        self.ja.set_value("current_url", url)
        driver = self.driver.get(url)
        self.log.log_INFO("SeleniumCore", "getSelUrl", url)
        return driver


    """CORE FINDING"""
    def findById(self, elem_id):
        element = self.driver.find_element_by_id(elem_id)
        self.log.log_INFO("SeleniumCore", "findById: " + elem_id)
        #self.ss.make_screenshot(element, "#007999")
        return element

    def findByName(self, elem_name):
        elem = self.driver.find_element_by_name(elem_name)
        self.log.log_INFO("SeleniumCore", "findByName: " + elem_name)
        #self.ss.make_screenshot(elem, "#3e3069")
        return elem

    def findByXpath(self, xpath_query):
        elem = self.driver.find_element_by_xpath(xpath_query)
        self.log.log_INFO("SeleniumCore", "findByXpath: " + xpath_query)
        #self.ss.make_screenshot(elem, "#3e3069")
        return elem

    def findByLink(self, elem_name):
        elem = self.driver.find_element_by_link_text(elem_name)
        self.log.log_INFO("SeleniumCore", "findByLink: " + elem_name)
        #self.ss.make_screenshot(elem, "#3e3069")
        return elem


    '''WAIT FINDING'''

    def findAllById(self, id_value):
        elem = WebDriverWait(self.driver, 5).until(EC.presence_of_all_elements_located((By.ID, id_value)))
        self.log.log_INFO("SeleniumCore", "findAllById with WAIT:", id_value)
        #self.ss.make_screenshot(elem, "#009947")
        return elem

    def findByLinkAndWait(self, content_text):
        try:
            elem = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.LINK_TEXT, str(content_text))))
            self.log.log_INFO("SeleniumCore", "findByLinkAndWait with WAIT: " + content_text)
            #self.ss.make_screenshot(elem, "#7a1f40")
            return elem
        except TimeoutException:
            self.log.log_INFO("SeleniumCore.findByLinkAndWait", "NIJE PRONADJEN: " + content_text)
            raise NoSuchElement("SeleniumCore.findByLinkAndWait, vrednost:", content_text)

    def findByClassAndWait(self, class_value):
        elem = WebDriverWait(self.driver, 7).until(
            EC.presence_of_element_located((By.CLASS_NAME, str(class_value))))
        self.log.log_INFO("SeleniumCore", "findByClassAndWait with WAIT: " + str(class_value))
        #self.ss.make_screenshot(elem, "#998400")
        return elem


    def findByTag(self, elem_tags, displayed=True, tolerance = 5):
        try:
            self.log.log_INFO("SeleniumCore", "findByTag with WAIT and ALL: ", elem_tags)
            all_elem = WebDriverWait(self.driver, tolerance).until(EC.presence_of_all_elements_located((By.TAG_NAME, elem_tags)))
            if displayed:
                displayed_elem = self.only_displayed_element(all_elem)
                # self.file.highlight(avaible_elem)
                return displayed_elem
            return all_elem
        except TimeoutException:
            raise NoSuchElement("SeleniumCore.findByTag with WAIT and ALL", elem_tags)

    def findElem(self, xpath_query, displayed=True, tolerance=5):
        self.log.log_INFO("SeleniumCore", "findElem")
        temp = self.findElements(xpath_query, displayed, tolerance)
        self.log.log_INFO("SeleniumCore", "findElem, dobijen broj elemenata: " + str(len(temp)))
        return temp[0]

    def findElements(self, xpath_query, displayed=True, tolerance=10):
        try:
            self.log.log_INFO("SeleniumCore", "findElements with WAIT", xpath_query)
            tmpob = WebDriverWait(self.driver, tolerance).until(EC.presence_of_all_elements_located((By.XPATH, xpath_query)))
            # tmpob = self.driver.find_elements_by_xpath(value)
            self.log.log_INFO("SeleniumCore", "UKUPAN broj elemenata: " + str(len(tmpob)))
            if displayed:
                elem_desplayed = self.only_displayed_element(tmpob)
                if elem_desplayed:
                    self.log.log_INFO("SeleniumCore", "Filtrirano, VIDLJIVIH: " + str(len(elem_desplayed)))
                    #self.ss.make_screenshot(tmpob[0])
                    return elem_desplayed
                else:
                    self.log.log_INFO("SeleniumCore", "Filtrirano, NEMA VIDLJIVIH!!!")
                    raise TimeoutException

            return tmpob

        except TimeoutException:
            raise NoSuchElement("SeleniumCore.findElements", xpath_query)


    def hoverAction(self, web_element):
        actions = ActionChains(self.driver).move_to_element(web_element)
        self.log.log_INFO("SeleniumCore", "hoverAction")
        actions.perform()
        self.ss.make_screenshot(web_element)

    def wait_loader(self, timeout=10):
        q =  "//span[(contains(@class,'ajax-status')) and (contains(@style, 'display: block'))]"
        WebDriverWait(self.driver, timeout).until(EC.invisibility_of_element_located((By.XPATH, q)))

    def clickElement(self, web_element, wait=False):
        self.ss.make_screenshot(web_element)
        self.log.log_INFO("SeleniumCore", "Click na: ", web_element.text)
        if wait:
            web_element.click()
            self.wait_loader(25)
        else:
            web_element.click()

    def clickWithPerform(self,  web_element, wait=False):
        self.ss.make_screenshot(web_element)
        self.log.log_INFO("SeleniumCore", "clickWithPerform na: ", web_element.text)
        if wait:
            actions = ActionChains(self.driver)
            actions.move_to_element(web_element).click().perform()
            self.wait_loader(10)
        else:
            actions = ActionChains(self.driver)
            actions.move_to_element(web_element).click().perform()





    def clickElementWithOutScreenshot(self, web_element):
        self.log.log_INFO("SeleniumCore", "Click na BEZ ZAPISA: ", web_element.text)
        web_element.click()


    # cekajElementID
    def waitForIdElement(self, time, id_value):
        try:
            elem = WebDriverWait(self.driver, time).until(EC.element_to_be_clickable((By.ID, id_value)))
            self.log.log_INFO("SeleniumCore", "waitForIdElement", "Vreme: " + str(time), "ID value: " + id_value)
            #self.ss.make_screenshot(elem)
            return elem
        except TimeoutException:
            raise NoSuchElement("SeleniumCore.waitForIdElement", id_value)

    def waitForNameElement(self, time, name_value):
        try:
            elem = WebDriverWait(self.driver, time).until(EC.element_to_be_clickable((By.NAME, name_value)))
            self.log.log_INFO("SeleniumCore", "waitForIdElement", "Vreme:" + str(time), "ID value:" + name_value)
            #self.ss.make_screenshot(elem)
            return elem
        except TimeoutException:
            raise NoSuchElement("SeleniumCore.waitForNameElement", name_value)


    def waitForXpathElement(self, time, xpath_value):
        try:
            elem = WebDriverWait(self.driver, time).until(EC.element_to_be_clickable((By.XPATH, xpath_value)))
            self.log.log_INFO("SeleniumCore", "waitForXpathElement", xpath_value)
            #self.ss.make_screenshot(elem)
            return elem
        except TimeoutException:
            raise NoSuchElement("SeleniumCore.waitForNameElement", xpath_value)

    def getAttributeValue(self, element, attribute):
        elem = element.get_attribute(attribute)
        self.log.log_INFO("SeleniumCore", "getAttributeValue:", elem)
        return elem

    def switchToFrame(self):
        try:
            #self.log.log_INFO("SeleniumCore","Promena frejma prema TAGU")
            elem = self.findByTag("iframe", True, 3)

            self.log.log_INFO("SeleniumCore", "Pozicioniranje na prvi 'IFRAME'")
            return self.driver.switch_to.frame(elem[0])
        except:
            self.log.log_INFO("SeleniumCore", "NISAM NASAO IFRAME!!!!")
        # return self.returnToDefContent()


    def returnToDefContent(self):
        self.log.log_INFO("SeleniumCore", "Povratak driver na default")
        self.driver.switch_to.default_content()


    # eklo iz common
    def only_displayed_element(self, tmpob):
        self.filter_desplayed(tmpob)
        if len(tmpob) == 0:
            return None
        return tmpob

    def filter_desplayed(self, tmpob):
        i = 0
        while i < len(tmpob):
            if not tmpob[i].is_displayed():
                tmpob.pop(i)
            else:
                i = i + 1
        return tmpob

    def stopDriver(self):
        self.log.log_INFO("SeleniumCore", "Driver se zaustavla...!")
        return self.driver.quit()

    def getCurentURl(self):
        self.log.log_INFO("SeleniumCore", "Vracam trenutni URL")
        url = self.driver.current_url
        return url

    def set_value_to_input(self, web_element , text_value, clear_field=True, use_tab=False):
        if clear_field:
            # pre nego kreneš da radiš bilo sta daaj mi vrdnost iz polja
            current_value = self.getAttributeValue(web_element, "value")
            # proveri da li je number current_value
            isNumber = re.search(r'(^\d+(?:[.]\d+)*$)', current_value)
            # proveri da li je datum current_value
            isDate = re.search(r'\d{1,2}.\d{1,2}.\d{4}', current_value)
            # proveri da li je obican text current_value
            isText = re.search(r'^[A-Za-z0-9]+$|^$', current_value)

            if isNumber:
                # ako je broj isprazni sa skriptom
                self.log.log_INFO("SeleniumCore", "Pražnjenje podataka NUMBER")
                self.driver.execute_script('arguments[0].value = "";', web_element)
            if isText:
                # ako je text isprazni normalno
                self.log.log_INFO("SeleniumCore", "Pražnjenje podataka TEXT")
                web_element.clear()
                time.sleep(2)
            if isDate:
                # ako je datum nemoj da praznis iako se to od tebe očekuje
                self.log.log_INFO("SeleniumCore", "DATUM, ne mogu da ispraznim vrednost!!!")

            self.log.log_INFO("SeleniumCore", "Postavljenje novih podataka u input: ", text_value)
            web_element.send_keys(text_value)
            self.ss.make_screenshot(web_element)
        else:
            self.log.log_INFO("SeleniumCore", "Postavljenje novih podataka u input, bez brisanje stare vrednosti : ", text_value)
            web_element.send_keys(text_value)
            time.sleep(2)
            self.ss.make_screenshot(web_element)
        if use_tab:
            self.log.log_INFO("SeleniumCore", "Koristim TAB nakon unosa...")
            web_element.send_keys(Keys.TAB)
            time.sleep(2)


    def set_value_to_input_script(self, web_element , text_value, clear_field=True, use_tab=False):
        if clear_field:
            self.log.log_INFO("SeleniumCore", "Pražnjenje prethodniih podataka iz polja SCRIPT...")
            self.driver.execute_script('arguments[0].value = "";', web_element)
            self.ss.make_screenshot(web_element)
            self.log.log_INFO("SeleniumCore","Postavljenje novih podataka u input: SCRIPT", text_value)
            #self.driver.execute_script('arguments[0].value ='+'"'+text_value+'"'+';', web_element)
            web_element.send_keys(text_value)
            self.ss.make_screenshot(web_element)
            self.clickElementWithOutScreenshot(web_element)
            time.sleep(3)

        else:
            self.log.log_INFO("SeleniumCore", "Postavljenje novih podataka u input, bez brisanje stare vrednosti : ", text_value)
            self.clickElementWithOutScreenshot(web_element)
            self.driver.execute_script('arguments[0].value ='+'"'+text_value+'"'+';', web_element)
            time.sleep(3)
            #self.ss.make_screenshot(web_element)
        if use_tab:
            self.log.log_INFO("SeleniumCore", "Koristim TAB nakon unosa...")
            web_element.send_keys(Keys.TAB)
            time.sleep(2)


    ## def set_with_js(self):
    ##   self.driver.execute_script("document.getElementById('editForm:veleprodajna_input').value='123'")
    ## time.sleep(20)




    def is_error_desplayed(self, xpath_query):
        try:
            elements = self.findElements(xpath_query, True, 2)
            if len(elements) > 0:
                raise UnexpectedElementDesplayed("SeleniumCore.is_error_desplay", xpath_query)

        except NoSuchElement:
            self.log.log_INFO("SeleniumCore", "Očekivani izuzetak, nije pronadjen ERROR na stranici:", xpath_query)

        except UnexpectedElementDesplayed:
            self.log.log_INFO("SeleniumCore", "Neočekivani ERROR, element sa greskom na stranici postoji:", xpath_query)
            #self.stopDriver()
            raise UnexpectedElementDesplayed("SeleniumCore.is_error_desplay", xpath_query)





































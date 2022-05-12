from PIL import Image as img
import os
from selenium_python.configuration.ReadJson import ReadJson
from selenium_python.db.MySQL import MySqlConnector

import time



class ScreenShoot():

    def __init__(self, driver, logger):
        self.img = img
        self.vars = vars
        self.driver = driver
        self.logg = logger
        self.jc = ReadJson("config.json")
        self.ja = ReadJson("action.json")
        self.db = MySqlConnector()

    def make_screenshot(self, element, color='#087830'):
        driver = element._parent
        def apply_style(s):
            driver.execute_script("arguments[0].setAttribute('style', arguments[1]);", element, s)
        original_style = element.get_attribute('style')
        apply_style("border: 5px solid {0};".format(color))
        text = element.text if element.text else element.get_attribute('class')
        self.screenshot_and_save_img(text)
        apply_style(original_style)

    def screenshot_and_save_img(self, text):
        log_directory_path = self.jc.get_value("log_folder")
        test_log_folder = self.ja.get_value("current_at")
        if not os.path.exists(log_directory_path+test_log_folder):
            os.makedirs(log_directory_path + test_log_folder)
        generate_number = str(round(time.time() * 1000))
        self.screenshotCurrentLocation(log_directory_path + test_log_folder + '\\' + generate_number+".png")
        self.ja.set_value("name_img", generate_number)
        self.ja.set_value("message", "Uspešno")
        self.db.save_to_log()

    def screenshotCurrentLocation(self, save_location):
        self.driver.save_screenshot(save_location)
        self.logg.log_INFO("Photo", "Zapis sacuvan na lokaciji: ", save_location)






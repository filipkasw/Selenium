import logging
from colorama import Back, Fore, Style
from selenium_python.configuration.ReadJson import ReadJson


class Logger:
    
    __path__ = " "
    __URL__ = " "
    __TAG__ = " "
    __level__ = logging.DEBUG
   
    def __init__(self):
        self.jc = ReadJson("config.json")
        self.logger = logging.getLogger(__class__.__name__)
        self.logger.setLevel(logging.DEBUG)
        # create file handler which logs even debug messages
        self.fh = logging.FileHandler(self.jc.get_value("logger_location"), "w", 'utf-8')

        self.fh.setLevel(Logger.__level__)
        # create console handler with a higher log level
        self.ch = logging.StreamHandler()
        self.ch.setLevel(Logger.__level__)
        # create formatter and add it to the handlers
        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.ch.setFormatter(self.formatter)
        self.fh.setFormatter(self.formatter)
        # add the handlers to logger
        self.logger.addHandler(self.ch)
        self.logger.addHandler(self.fh)


    def log_INFO(self, Poruka, path = __path__ , URL = __URL__, TAG = __TAG__):
        self.logger.info("- {} - {} - {} - {} - ".format(Poruka,path, URL, TAG))
 
    def log_DEBUG(self, Poruka, path = __path__, URL = __URL__, TAG = __TAG__):
        self.logger.debug(Back.RED +"- {} - {} - {} - {} - ".format(Poruka,path, URL, TAG) + Style.RESET_ALL)
        
    def log_WARNING(self, Poruka, path = __path__, URL = __URL__, TAG = __TAG__):
        self.logger.warning("- {} - {} - {} - {} - ".format(Poruka,path, URL, TAG))
        
    def log_ERROR(self, Poruka, path = __path__, URL = __URL__, TAG = __TAG__):
        self.logger.error(Back.RED +"- {} - {} - {} - {} - ".format(Poruka,path, URL, TAG) + Style.RESET_ALL)
        
    def log_CRITICAL(self, Poruka, path = __path__, URL = __URL__, TAG = __TAG__):
        self.logger.critical("- {} - {} - {} - {} - ".format(Poruka,path, URL, TAG))

    
        
   

      


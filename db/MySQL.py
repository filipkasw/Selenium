import mysql.connector
from selenium_python.configuration.ReadJson import ReadJson


class MySqlConnector():

     # konfiguracija konekcije
    def __init__(self):
        #self.logg = logg
        self.jc = ReadJson("config.json")
        self.ja = ReadJson("action.json")
        self.mydb = mysql.connector.connect(
            host=self.jc.get_value("db_host"),
            port=self.jc.get_value("db_port"),
            user=self.jc.get_value("db_username"),
            password=self.jc.get_value("db_password"),
            database=self.jc.get_value("db_schema")
        )

    # Upit koji mi puni tabelu u bazi podataka, tabela se zove status, polja koja ima vidite u metodi.
    def insertToLog(self, test_name, app, orgjed, path, url, index_command, command, parameter1, parameter2, error, message, photo):
        insert_query = ("""INSERT INTO vezbanje (test_name, app, orgjed, path, url, index_command, command, parameter1, parameter2, error, message, photo) 
                           VALUES 
                           ("{}", "{}", "{}", "{}", "{}", {}, "{}", "{}", "{}", {}, "{}" , "{}")""".format(test_name, app, orgjed, path, url, index_command, command, parameter1, parameter2, error, message, photo))
        #print(insert_query)
        cursor = self.mydb.cursor()
        cursor.execute(insert_query)
        self.mydb.commit()

    # Upit koji mi brise sve iz tabele vezan ya test koji se ucitava, dobra stvar da se ne gomila u tabeli podakte narocito sada u toku razvoja.
     #Pustim test proverim da li taj test ranije pustan ako jeste obrisem sve iz tabele vezano za njega
    def delete_all_by_test_name(self, test_name):
        insert_query = ("""DELETE FROM vezbanje WHERE vezbanje.test_name = '{}'""".format(test_name))
        #print(insert_query)
        cursor = self.mydb.cursor()
        cursor.execute(insert_query)
        self.mydb.commit()

    # ove lezi ZEC, videli ste kako se popunjava action.json tokom izvrasavanja program.
     # onda se nakon svake komande pokupi iz tog fajla trenutno stanje i snimi u bazu.
    def save_to_log(self):
        test_name = self.ja.get_value("current_at")
        app = self.ja.get_value("current_app")
        orgjed = self.ja.get_value("current_orgjed")
        path = self.ja.get_value("current_path")
        url = self.ja.get_value("current_url")
        index_command = self.ja.get_value("index_command")
        command = self.ja.get_value("current_command")
        parameter1 = self.ja.get_value("current_parameter1")
        parameter2 = self.ja.get_value("current_parameter2")
        photo = self.ja.get_value("name_img")
        error = self.ja.get_value("error")
        message = self.ja.get_value("message")
        self.insertToLog(test_name, app, orgjed, path, url, index_command, command, parameter1, parameter2, error, message, photo)







#m = MySqlConnector()
#m.insertToLog("test", "ulazni racuni", "magacin", "sifarnici/artikli", "www.google.com", "looup", "parameter",0,"nema greske", "0000")
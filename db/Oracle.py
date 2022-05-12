import cx_Oracle as ora
from selenium_python.configuration.ReadJson import ReadJson
from colorama import Back, Fore, Style
# trebace vam ovaj "ora_instantclient": "C:\\instantclient\\instantclient-basic-windows.x64-19.10.0.0.0dbru\\instantclient_19_10",
# gore ovaj client lokacija nalazi se u config.json, poslacu vam ceo moj config json.
# 1. takodje morate da skinete ovaj instantclient_19_10 proguglajte
# 2. trebace vam i cx_Oracle pogledajte kako se instalira pip install ora...tako nesto u consoli
insta_cl = ReadJson("config.json")
print(insta_cl.get_value("ora_instantclient"))
ora.init_oracle_client(lib_dir=insta_cl.get_value("ora_instantclient"))


class OracleDB():

    def __init__(self, logg):
        self.logg = logg
        self.jc = ReadJson("config.json")
        self.ora = ora

    def make_connection(self):
        users = self.jc.get_value("ora_username")
        passwords = self.jc.get_value("ora_password")
        ip = self.jc.get_value("ora_ip")
        port = self.jc.get_value("ora_port")
        sid = self.jc.get_value("ora_sid")
        self.logg.log_INFO("OracleDB", "make_connection with USER: "+ users, "PASSWORD: "+ passwords)
        dsn_tns = self.ora.makedsn(ip, port, service_name=sid)
        conn = self.ora.connect(users, passwords, dsn=dsn_tns, encoding="UTF-8")
        conn.autocommit = True
        self.logg.log_INFO(conn)
        return conn

    def execute_query(self, sql_query):
        self.logg.log_INFO(Fore.MAGENTA + "OracleDB", "execute_query", "ŠALJEM UPIT: " + sql_query + Style.RESET_ALL)
        conn = self.make_connection().cursor()
        cursor = conn.execute(sql_query)
        self.logg.log_INFO(Fore.GREEN + "OracleDB", "**ZAVRŠEN UPIT**" + Style.RESET_ALL)
        return cursor
# Ovde vam fali Logger jer ga tada nisam imao kad sam pravio i testirao ovaj modul..
# importujte Logger i probajte modul da pustite samostalno bez selenium i bilo cega
#o = OracleDB("Logger koji fali pise u komentaru iznad")
#Kad sredite objeka pustite ovaj upit
#select = "SELECT * FROM artikli"
#c = o.execute_query(select)
#for row in c:
#    print (row[0], '-', row[1]) # this only shows the first two columns. To add an additional column you'll need to add , '-', row[2], etc.
#conn.close()



#OVO ISPOD NE PUSTAJTE DA NE BI STE BRLJALI BAZU, ALI SAM OSTAVIO DA IMATE PROMER INSERTA
#insert = "INSERT INTO artikli VALUES (00202020202, '54545' ,'BORISAV TESTIRAO BRISI', 'Test', 5071 , 1, 'D','R', 'BOT')"
#delete ="DELETE from artikli where id=00202020202 "




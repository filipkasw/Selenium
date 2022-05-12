#from test_inter_OOP.pLogger import Logger
import pandas as pd
import cx_Oracle as ora
#lib_dir = r"C:\instantclient\instantclient-basic-windows.x64-19.10.0.0.0dbru\instantclient_19_10"
#ora.init_oracle_client(lib_dir=lib_dir)





#C:\\workspace\\dominus_test\\testsJSF\\Roba\\cenovnici\\files\\cenovnik001.xls, cenDob_vratiCene_Unos, testlilly
from selenium_python.file.ReadDocuments import ReadExcel
from selenium_python.db.Oracle import OracleDB
from selenium_python.configuration.GlobalVariable import GlobalVariable
from selenium_python.exception.CustomException import ComparisonNotCorrect

class excelScript:

    def __init__(self, logg):

        self.logg = logg
        self.re = ReadExcel(logg)
        self.ora = OracleDB(logg)
        self.gv = GlobalVariable()

    def VratiKalkulacijaRuc(self, check_value, sema_baze="testlilly"):
        self.logg.log_INFO("VLP_excelScript", "--- VratiKalkulacijaRuc ---", check_value)
        self.logg.log_INFO("excelScript", "VratiKalkulacijaRuc")
        conn = self.ora.execute_query("select vrijednost from db_parametri where sifra='kalkulacijaRUC'")
        result = conn.fetchall()
        for i in result:
            if i[0] != check_value:
                self.logg.log_INFO("excelScript", "Result: ", result)
                raise ComparisonNotCorrect("VratiKalkulacijaRuc, vrednost: " + check_value +" ne poklapa se sa: " + i[0] )
        conn.close()
        return result





















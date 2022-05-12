from selenium_python.db.Oracle import OracleDB
from selenium_python.file.ReadDocuments import ReadExcel
from selenium_python.configuration.ReadJson import ReadJson
from selenium_python.db.MySQL import MySqlConnector
from selenium_python.exception.CustomException import ComparisonNotCorrect
import pandas as pd
import os
import csv
import functools
import operator
from colorama import Fore, Back, Style


class SQL_CSV():

    def __init__(self,  logg):
        self.logg = logg
        self.jc = ReadJson("config.json")
        self.ja = ReadJson("action.json")
        self.ora = OracleDB(logg)
        self.csv = ReadExcel(logg)
        self.db = MySqlConnector()

    def sql_to_compare(self, pp1, pp2):
        pp2 = "prazan" if str(pp2) == "nan" else pp2
        pp2 = str(pp2) if str(pp2) == "0" else pp2
        self.logg.log_INFO("SQL_CSV", "sql_to_compare")
        self.logg.log_INFO("------------------------------------")
        self.logg.log_INFO(Fore.GREEN + "Values, SQL-COMPARE: ", pp2, " " + Style.RESET_ALL)
        self.logg.log_INFO("------------------------------------")
        self.swichunos(pp1, pp2)

    def swichunos(self, pp1, pp2):
        switcher = {
            "0": lambda: self.compare_sql_and_zero(pp1, pp2),
            "prazan": lambda: self.compare_sql_and_zero(pp1, pp2),
            "C:\\workspace\\dominus_test\\testsJSF\\SQL\\DbPar_Cen.csv": lambda: self.compare_with_prepared_csv(pp1, pp2),

        }
        func = switcher.get(pp2, lambda: self.compare_query_and_csv(pp1, pp2))
        func()

    def compare_with_prepared_csv(self, query, file_path, delimiter=";"):
        self.logg.log_INFO("SQL_CSV", "compare_query_and_csv", query, file_path)
        cursor = self.ora.execute_query(query)
        db_data = self.cursor_to_dataframe(cursor)
        order_value = str(db_data.columns[0])
        db_data = db_data.sort_values(by=order_value, ascending=True).reset_index(drop=True)
        csv_data = self.csv.read_csv(file_path, delimiter, order_value).sort_values(by=order_value,
                                                                                    ascending=True).reset_index(
            drop=True)
        # print(Fore.RED, db_data[order_value])
        # print(Fore.RED, type(db_data))
        # print(Fore.RED, db_data)
        # print(Fore.BLUE, csv_data[order_value])
        # print(Fore.GREEN, type(csv_data))
        # print(Fore.GREEN,  csv_data)
        csv_data.fillna(-999999, inplace=True)
        csv_data = csv_data.apply(pd.to_numeric, errors='coerce').fillna(csv_data)
        db_data.fillna(-999999, inplace=True)
        db_data = db_data.apply(pd.to_numeric, errors='coerce').fillna(db_data)
        return self.comparison(db_data, csv_data, delimiter)

    def compare_query_and_csv(self, query, file_name, delimiter=";"):
        self.logg.log_INFO("SQL_CSV", "compare_query_and_csv", query, file_name)
        cursor = self.ora.execute_query(query)
        db_data = self.cursor_to_dataframe(cursor)

        order_value = str(db_data.columns[0])
        folder_path = self.jc.get_value("csv_sql_folder") + self.ja.get_value("current_at")
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        file_path = folder_path+"\\"+ file_name
        file_path = file_path+".csv" if not ".csv" in file_path else file_path
        if not os.path.isfile(file_path):
                db_data.to_csv(file_path, quoting=csv.QUOTE_NONNUMERIC, index=False, doublequote=True, header=True,sep=';', quotechar='"')  # Don't forget to add '.csv' at the end of the path

        db_data = db_data.sort_values(by=order_value, ascending=True).reset_index(drop=True)
        csv_data = self.csv.read_csv(file_path, delimiter, order_value).sort_values(by=order_value, ascending=True).reset_index(drop=True)
        #print(Fore.RED, db_data[order_value])
        #print(Fore.RED, type(db_data))
        #print(Fore.RED, db_data)
        #print(Fore.BLUE, csv_data[order_value])
       # print(Fore.GREEN, type(csv_data))
       # print(Fore.GREEN,  csv_data)
        csv_data.fillna(-999999, inplace=True)
        csv_data = csv_data.apply(pd.to_numeric, errors='coerce').fillna(csv_data)
        db_data.fillna(-999999, inplace=True)
        db_data = db_data.apply(pd.to_numeric, errors='coerce').fillna(db_data)
        return self.comparison(db_data, csv_data, delimiter)

    def compare_sql_and_zero(self, pp1, pp2):
        db_data = self.ora.execute_query(pp1)
        db_data = self.cursor_to_dataframe(db_data)
        order_value = str(db_data.columns[0])
        db_data = db_data.sort_values(by=order_value, ascending=False).reset_index(drop=True)
        if "count" in pp1:
            self.logg.log_INFO("CSV", "compare_sql_and_zero(COUNT)", pp1, pp2)
            db_result = db_data['COUNT(*)'].tolist()[0]
            if db_result == int(pp2):
                self.logg.log_INFO(Fore.GREEN + "ELEMENTI SU ISTI: ", "COUNT" + Style.RESET_ALL)
                self.ja.set_value("message", "Poredjenje SQL sa COUNT je uspesno!")
                self.ja.set_value("name_img", "compare_sql_success")
                self.db.save_to_log()
            else:
                self.ja.set_value("name_img", "compare_sql_error")
                self.logg.log_INFO(Back.RED + "SQL_CSV", "Razliku u podacima je u: \n", db_result, pp2 + Style.RESET_ALL)
                self.ja.set_value("name_img", "compare_sql_error")
                raise ComparisonNotCorrect("Razliku u podacima je u: " + db_result + " != " + pp2)

        elif "sifra" in pp1 and "," not in pp2:
            self.logg.log_INFO("CSV", "compare_SQL_and_expected_result(SIFRA)", pp1, pp2)
            db_result = db_data['SIFRA'].tolist()[0]
            if int(db_result) == int(pp2):
                self.logg.log_INFO("ELEMENTI SU ISTI: ", "SIFRA" )
                self.ja.set_value("message", "Poredjenje SQL sa SIFRA je uspesno!")
                self.ja.set_value("name_img", "compare_sql_success")
                self.db.save_to_log()
            else:
                self.ja.set_value("name_img", "compare_sql_error")
                self.logg.log_INFO("SQL_CSV", "Razliku u podacima je u: \n", db_result, pp2)
                self.ja.set_value("name_img", "compare_sql_error")
                raise ComparisonNotCorrect("Razliku u podacima je u: " + db_result + " != " + pp2)

        elif pp2 == "prazan":

            self.logg.log_INFO("CSV", "compare_SQL_and_expected_result(NULL)", pp1, pp2)
            result_set = db_data
            print(result_set.values)
            if len(result_set) != 0:
                self.logg.log_INFO(Fore.RED + "CSV", "Podaci imaju su veći od očekivane NULLE" + Style.RESET_ALL)
                self.ja.set_value("name_img", "compare_sql_error")
                self.logg.log_INFO("SQL_CSV", "Razliku u podacima je u: \n", result_set, pp2)
                self.ja.set_value("name_img", "compare_sql_error")
                raise ComparisonNotCorrect("Razliku u podacima, trenutni RESULTAT JE: " + result_set + ", OCEKIVAN JE: " + pp2)
            else:
                self.logg.log_INFO("ELEMENTI SU ISTI: ", "SIFRA")
                self.ja.set_value("message", "Poredjenje SQL sa SIFRA je uspesno!")
                self.ja.set_value("name_img", "compare_sql_success")
                self.db.save_to_log()

    def cursor_to_dataframe(self, cursor, st=False):
        df_multindex = []
        for e in cursor:
            if st:
                rtest = self.convert_tuple(e)
                df_multindex.append(rtest)
            else:
                e = list(e)
                for a, item in enumerate(e):
                    az = str(type(item))
                    if 'datetime.datetime' in az:
                        e[a] = str(item)
                tuple(e)
                df_multindex.append(e)
        return pd.DataFrame(df_multindex, columns=[row[0] for row in cursor.description])

    def convert_tuple(self, tup):
        self.logg.log_INFO("CSV", "convert_tuple: ", tup)
        stri = functools.reduce(operator.add, (tup))
        return str(stri)


    def comparison(self, db_data, csv_data, delimiter=""):
        self.logg.log_INFO("SQL_CSV", "comparison data from DB : \n", db_data)
        self.logg.log_INFO("SQL_CSV", "type: ", type(db_data))
        self.logg.log_INFO("SQL_CSV", "comparison data from CSV : \n ", csv_data)
        self.logg.log_INFO("SQL_CSV", "type: ", type(csv_data))
        if delimiter != "":
            db_data = self.organize_data(db_data, delimiter)
            csv_data = self.organize_data(csv_data, delimiter)
        if self.compare_sizes(csv_data, db_data):
            comparison = csv_data.values == db_data.values
            is_same = comparison.all()
            if not is_same:
                diff = self.return_difference(csv_data, db_data)
                self.ja.set_value("name_img", "compare_sql_error")
                self.logg.log_INFO("SQL_CSV", "Razliku u podacima je u: \n", diff)
                self.ja.set_value("name_img", "compare_sql_error")
                raise ComparisonNotCorrect("Razliku u podacima je u: " +  str(diff))

            else:
                self.logg.log_INFO(Fore.GREEN + "ELEMENTI SU ISTI: ", is_same,  Style.RESET_ALL)
                self.ja.set_value("message", "Poredjenje parametra1 i parametra2 uspešno!")
                self.ja.set_value("name_img", "compare_sql_success")
                self.db.save_to_log()

    def organize_data(self, data, delimiter):
        self.logg.log_INFO("SQL_CSV", "organize_data", )
        delimiter = delimiter.upper().split(", ")
        izbaci = []
        for i in delimiter:
            if i in data.columns:
                izbaci.append(i)
        return data.drop(izbaci, axis=1)

    def compare_sizes(self,csv_data, db_data, kolods=0, rowods=0):
        self.logg.log_INFO("SQL_CSV", "compare_sizes", "ulazi")
        if csv_data.shape[1] != db_data.shape[1]:
            return self.correction(csv_data.shape[1], db_data.shape[1], "kolona", kolods)
        if csv_data.shape[0] != db_data.shape[0]:
            return self.correction(csv_data.shape[0], db_data.shape[0], "rezultata", rowods)
        return True

    def correction(self, Num1, Num12, tekst, kolods=0):
        self.logg.log_INFO("SQL_CSV", "correction", )
        if kolods != 0:
            if Num1 > Num12:
                if Num1 - kolods != Num12:
                    print("Razlicit broj " + tekst + " - " + str(Num1) + " nije jednako " + str(Num12))
                    return False
            elif Num12 - kolods != Num1:
                print("Razlicit broj " + tekst + " - " + str(Num1) + " nije jednako " + str(Num12))
                return False
            return True

    def return_difference(self,oldFrame, newFrame):
        diff1 = []
        for i in oldFrame.values:
            for j in newFrame.values:
                a = set(i)
                b = set(j)
                if a != b:
                    diff1.append(i)
                    diff1.append(j)
                    return diff1
        return "Nisam našao razliku"

import pandas as pd


class ReadExcel():

    def __init__(self, logg):
        self.logg = logg
        self.pd = pd

    def read_excel(self, location, sheet):

        self.logg.log_INFO("READ DATA FROM EXCEL: " + location, "SHEET: " + sheet)
        return self.pd.read_excel(location, sheet_name=sheet)

    def read_csv(self, location, delimiter, field):
        self.logg.log_INFO("READ DATA FROM CSV: " + location, "DELIMITER: " + delimiter)
        return self.pd.read_csv(location, delimiter=delimiter,  dtype={field: object})


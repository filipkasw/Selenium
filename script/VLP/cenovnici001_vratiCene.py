from selenium_python.file.ReadDocuments import ReadExcel
from selenium_python.db.Oracle import OracleDB
from selenium_python.configuration.GlobalVariable import GlobalVariable

class VLP:

    def __init__(self, logg):
        self.logg = logg
        self.re = ReadExcel(logg)
        self.ora = OracleDB(logg)
        self.gv = GlobalVariable()



    def vratiCene_cenProdaje(self, excel, sheet):
        self.logg.log_INFO("VLP","Method:"," vratiCene_cenProdaje ")
        abs_path = self.gv.get_absolute_path(excel)
        print(abs_path)
        excel_content = self.re.read_excel(abs_path, sheet)
        for index, row in excel_content.iterrows():
            artikal = row['artikal']
            komitenttip = row['komitenttip']
            vremeod = row['vremeod']
            komitent = row['komitent']
            tipceneobjekta = row['tipceneobjekta']
            updatevremeod = row['updatevremeod']
            vremeod_prvogIntervala = row['vremeod_prvogIntervala']

            self.logg.log_INFO("VLP", "SQL", "UPDATE cenovnikprodaje...", "1")
            self.ora.execute_query("""update cenovnikprodaje set vremeod=to_timestamp('{}','dd.mm.yyyy hh24:mi:ss'), 
                                                                 potvrdjen = 'D', 
                                                                 vremepotvrde = sysdate 
                                                             where artikal = artiklipkg.getId('{}') 
                                                             and tipceneobjekta = '{}' 
                                                             and vremeod=to_timestamp('{}','dd.mm.yyyy hh24:mi:ss')""".format(updatevremeod, artikal, tipceneobjekta, vremeod))

            self.logg.log_INFO("VLP", "SQL","UPDATE cenovnikprodaje","2")
            self.ora.execute_query("""update cenovnikprodaje set vremedo=to_timestamp('{}','dd.mm.yyyy hh24:mi:ss'), 
                                                                 potvrdjen = 'D', 
                                                                 vremepotvrde = sysdate 
                                                            where artikal = artiklipkg.getId('{}') 
                                                            and tipceneobjekta = '{}'
                                                            and vremeod=to_timestamp('{}','dd.mm.yyyy hh24:mi:ss')""".format(
                    updatevremeod, artikal, tipceneobjekta, vremeod_prvogIntervala))

            self.logg.log_INFO("VLP", "SQL","UPDATE cenovnikdobavljaca","3")
            self.ora.execute_query("""update cenovnikdobavljaca set vremeod=to_timestamp('{}','dd.mm.yyyy hh24:mi:ss') 
                                             where artikal = artiklipkg.getId('{}') 
                                             and komitenttip = '{}' 
                                             and komitent = '{}' 
                                             and tipcenedobavljaca = '{}'
                                             and vremeod=to_timestamp('{}','dd.mm.yyyy hh24:mi:ss')""".format(updatevremeod, artikal, komitenttip, komitent, tipceneobjekta, vremeod))

            self.logg.log_INFO("VLP", "SQL", "UPDATE cenovnikdobavljaca","4")
            self.ora.execute_query("""update cenovnikdobavljaca set vremedo=to_timestamp('{}','dd.mm.yyyy hh24:mi:ss') 
                                             where artikal = artiklipkg.getId('{}') 
                                             and komitenttip = '{}' 
                                             and komitent = '{}' and tipcenedobavljaca = '{}' 
                                             and vremeod=to_timestamp('{}','dd.mm.yyyy hh24:mi:ss')""".format(updatevremeod, artikal, komitenttip, komitent, tipceneobjekta, vremeod_prvogIntervala))

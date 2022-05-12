


class GlobalVariable:

    def __init__(self):  # key[key_in_key]
        self.btn_map_state = {("izmena", "izmeni", "edit"): ("fa fa-pencil", "asw_edit_icon"),
                              ("realizacija", "fajl"): ('fa fa-file-o'),
                              ("copy", "kopiraj"): ('fa fa-copy'),
                              ('geer', 'gear'): ("fa fa-gear"),
                              ('zavrsetak', 'završetak', 'zatvaranje', 'likvidacija', 'zaključaj', 'zakljucaj'): (
                                  'fa fa-lock'),
                              ('otvaranje', 'otkljucaj'): ('fa fa-unlock', "Otvaranje"),
                              ('potvrda', 'potvrdi', 'Da', 'da'): ('fa fa-check','fa fa-check-square-o', 'Da'),
                              ('stampaj', 'štampaj'): ('fa fa-print'),
                              ('iks', 'close'): ('closethick', 'fa fa-close'),
                              "detalj": ('asw_view_icon', 'fa fa-eye', 'fa fa-eyel'),
                              "stavke": ("asw_masterdetail_icon", "fa fa-sitemap"),
                              "brisanje": ('fa fa-trash', 'asw_delete_icon'),
                              'zupcanici': ('fa fa-gears'),
                              'izvestaji': ('fa fa-bar-chart-o'),
                              'popust': ('fa fa-book'),
                              'veza': ('fa fa-chain'),
                              'vezi': ('fa fa-chain'),
                              'kalkulacija': ('fa fa-calculator'),
                              'upit': ('fa fa-search'),
                              'novi': ('fa-plus-circle'),
                              'import': ('fa-sign-in'),
                              'odustani':('fa fa-ban'),
                              'proknjiži': ('fa-check-square-o'),
                              'dalje': ('fa fa-angle-double-down')
                          }

    def createRegular(self):
        btn_map_regular = {}
        for key in self.btn_map_state:
            if type(key).__name__ == 'tuple':
                for key_in_key in key:
                    btn_map_regular[key_in_key] = self.btn_map_state[key]
            else:
                btn_map_regular[key] = self.btn_map_state[key]

        return btn_map_regular

    def get_absolute_path(self, relative_path):
        path = {
            r"..\\..\\testsJSF\\Roba\\cenovnici\\files\\cenovnik001.xls": r"C:\\workspace\\dominus_test\\testsJSF\\Roba\\cenovnici\\files\\cenovnik001.xls",
        }
        return path[relative_path]




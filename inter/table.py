import flet as ft
from flet import *
from inter.filter import FilterUI

# CLASE QUE CREA UNA INTERFAZ DE TABLA PARA LOS TRABAJADORES Y SUS FILTROS
class Tables:
    def __init__(self, page: Page,app_state):
        self.filter_ui = FilterUI(page,app_state)
        self.page = page

    def datatable(self):
        return self.filter_ui.data_table_container

    def table(self):
        return self.filter_ui.ui_container
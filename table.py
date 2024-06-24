import flet as ft
from flet import *
from filter import FilterUI

class Tables:
    def __init__(self, page: Page):
        self.filter_ui = FilterUI(page)
        self.page = page

    def datatable(self):
        return self.filter_ui.data_table_container

    def table(self):
        return self.filter_ui.ui_container
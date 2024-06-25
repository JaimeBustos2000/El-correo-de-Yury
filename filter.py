import flet as ft
from flet import *
import sqlite3
from bsdclass import bsdinteraction

# CLASE QUE CREA UNA INTERFAZ DE FILTRO PARA LOS TRABAJADORES

class FilterUI:
    def __init__(self, page: ft.Page):
        self.page = page
        self.bsd_interaction = bsdinteraction()
        self.con = bsdinteraction().connection()
        self.data_table_container = ft.Column()  # Inicializamos aquí para evitar AttributeError
        self.build_filter_ui()

    def build_filter_ui(self):
        self.cargo_filter = ft.Dropdown(
            label="Cargo",
            label_style=ft.TextStyle(color="WHITE"),
            color="BLACK",
            options=[
                ft.dropdown.Option("1", text="Gerente de RR.HH."),
                ft.dropdown.Option("2", text="Personal de RR.HH."),
                ft.dropdown.Option("3", text="Jefe de envíos"),
                ft.dropdown.Option("4", text="Repartidor")
            ],
            on_change=self.apply_filters
        )

        self.sexo_filter = ft.Dropdown(
            label="Sexo",
            label_style=ft.TextStyle(color="WHITE"),
            color="BLACK",
            options=[
                ft.dropdown.Option("M", text="Masculino"),
                ft.dropdown.Option("F", text="Femenino")
            ],
            on_change=self.apply_filters
        )

        self.area_filter = ft.Dropdown(
            label="Área",
            label_style=ft.TextStyle(color="WHITE"),
            color="BLACK",
            options=[
                ft.dropdown.Option("1", text="Envios"),
                ft.dropdown.Option("2", text="recursos humanos")
            ],
            on_change=self.apply_filters
        )

        self.reset = ft.TextButton(
            text="Reiniciar",
            on_click=self.reset_filters,
            style=ft.ButtonStyle(bgcolor="BLACK", color="WHITE")
        )

        filters_container = ft.Column(
            controls=[
                ft.Row(controls=[self.cargo_filter, self.sexo_filter, self.area_filter, self.reset])
            ]
        )

        self.apply_filters(None)

        self.ui_container = ft.Column(
            controls=[Row(width=100),filters_container, self.data_table_container],
            expand=True,
            scroll=True
        )

        return self.ui_container

    def apply_filters(self, e):
        cargo = self.cargo_filter.value
        sexo = self.sexo_filter.value
        area = self.area_filter.value

        print(cargo, sexo, area)
        filtros = []
        if cargo:
            filtros.append(f"c.id_cargo='{cargo}'")
        if sexo:
            filtros.append(f"e.sexo='{sexo}'")
        if area:
            filtros.append(f"d.id_depto='{area}'")

        if len(filtros) > 1:
            filtro = " AND ".join(filtros) if filtros else ""
            data_table = self.bsd_interaction.consultar_trabajadores(filtro)
        elif len(filtros) == 0:
            data_table = self.bsd_interaction.consultar_trabajadores(filtro="")
        else:
            data_table=self.bsd_interaction.consultar_trabajadores(filtro=filtros[0])
            

        self.data_table_container.controls.clear()
        self.data_table_container.controls.append(data_table)
        self.page.update()

    def reset_filters(self, e):
        self.cargo_filter.value = ""
        self.sexo_filter.value = ""
        self.area_filter.value = ""
        self.apply_filters(None)
        self.page.update()
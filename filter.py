import flet as ft
from flet import *
import sqlite3

class FilterUI:
    def __init__(self, page: Page):
        self.page = page
        self.data_table_container = Column()  # Inicializamos aquí para evitar el AttributeError
        self.build_filter_ui()

    def build_filter_ui(self):
        self.cargo_filter = Dropdown(
            label="Cargo",
            options=[
                dropdown.Option("1",text="Jefe de envíos"),
                dropdown.Option("2",text="Gerente de RR.HH."),
                dropdown.Option("3",text="Personal de RR.HH."),
                dropdown.Option("4",text="Repartidor")
            ],
            on_change=self.apply_filters
        )

        self.sexo_filter = Dropdown(
            label="Sexo",
            options=[
                dropdown.Option("M", text="Masculino"),
                dropdown.Option("F", text="Femenino")
            ],
            on_change=self.apply_filters
        )

        self.area_filter = Dropdown(
            label="Área",
            options=[
                dropdown.Option("1",text="Envios"),
                dropdown.Option("2",text="recursos humanos")
            ],
            on_change=self.apply_filters
        )
        
        self.reset=ft.TextButton(text="Reiniciar",on_click=self.reset_filters,style=ButtonStyle(bgcolor="BLACK",color="WHITE"))

        filters_container = Column(
            controls=[
                Row(controls=[self.cargo_filter, self.sexo_filter, self.area_filter,self.reset])
            ]
        )

        self.apply_filters(None)

        self.ui_container = Column(controls=[filters_container, self.data_table_container], expand=True,scroll=True)

        return self.ui_container

    def apply_filters(self, e):
        cargo = self.cargo_filter.value
        sexo = self.sexo_filter.value
        area = self.area_filter.value

        filtros = []
        if cargo:
            filtros.append(f"cargo='{cargo}'")
        if sexo:
            filtros.append(f"sexo='{sexo}'")
        if area:
            filtros.append(f"area_y_departamento='{area}'")
            

        filtro = " AND ".join(filtros) if filtros else "1=1"  # Default to no filter
        data_table = self.consultar(filtro)

        self.data_table_container.controls.clear()
        self.data_table_container.controls.append(data_table)
        self.page.update()


    def reset_filters(self,e):
        self.cargo_filter.value=""
        self.sexo_filter.value=""
        self.area_filter.value=""
        self.apply_filters(None)
        self.page.update()
        
    def consultar(self, filtro=""):
        database = "correosyury.db"

        mydt = DataTable(
            bgcolor="WHITE",
            heading_row_color=ft.colors.BLACK87,
            border=ft.border.all(2, "BLACK"),
            border_radius=10,
            vertical_lines=ft.border.BorderSide(1, "BLACK"),
            horizontal_lines=ft.border.BorderSide(2, ""),
            columns=[
                ft.DataColumn(ft.Text(value="#")),
                ft.DataColumn(ft.Text(value="Rut")),
                ft.DataColumn(ft.Text(value="Nombre")),
                ft.DataColumn(ft.Text(value="Sexo")),
                ft.DataColumn(ft.Text(value="Direccion")),
                ft.DataColumn(ft.Text(value="Telefono")),
                ft.DataColumn(ft.Text(value="Cargo")),
                ft.DataColumn(ft.Text(value="Fecha-ingreso")),
                ft.DataColumn(ft.Text(value="Area y depto."))
            ],
            rows=[]
        )

        # Connect to the database
        conn = sqlite3.connect(database)
        cur = conn.cursor()

        # Execute the query with the filter
        query = f"SELECT * FROM trabajadores WHERE {filtro}"
        cur.execute(query)

        # Fetch the results
        result = cur.fetchall()

        # Get column names
        columns = [column[0] for column in cur.description]

        # Create a dictionary for each row
        rows = [dict(zip(columns, row)) for row in result]

        # Add rows to the DataTable
        for i, row in enumerate(rows):
            i += 1
            mydt.rows.append(
                DataRow(cells=[
                    DataCell(ft.Text(str(i), color="BLACK")),
                    DataCell(ft.Text(value=row["rut"], color="BLACK")),
                    DataCell(ft.Text(value=row["nombre"], color="BLACK")),
                    DataCell(ft.Text(value=row["sexo"], color="BLACK")),
                    DataCell(ft.Text(value=row["direccion"], color="BLACK")),
                    DataCell(ft.Text(value=row["telefono"], color="BLACK")),
                    DataCell(ft.Text(value=row["cargo"], color="BLACK")),
                    DataCell(ft.Text(value=row["fecha_ingreso"], color="BLACK")),
                    DataCell(ft.Text(value=row["area_y_departamento"], color="BLACK"))
                ])
            )

        conn.close()
        return mydt
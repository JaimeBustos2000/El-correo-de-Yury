import flet as ft
from flet import *
from cdyury.bsdclass import bsdinteraction
from cdyury.appstatus import AppState
from datetime import datetime



class DashboardPage:
    def __init__(self, page:Page,app_state):
        self.page = page
        self.app_state = app_state
        
        self.listaEmp = ElevatedButton(text="Lista de empleados", on_click=lambda _: page.go("/tables"))
        self.start = ElevatedButton(text="Inicio", bgcolor="GREEN", color="BLACK", on_click=lambda _: page.go("/inicio"))
        self.forms = ElevatedButton(text="Formulario", on_click=lambda _: page.go("/formularios"))
        self.datos = ElevatedButton(text="Cuenta", on_click=self.dataemp)

        self.navbar = AppBar(
            leading=IconButton(icons.DOOR_BACK_DOOR_OUTLINED, on_click=self.disconnectt),
            center_title=False,
            bgcolor="#365097",
            actions=[self.start, self.listaEmp, self.forms, self.datos]
        )

        self.inicio = Container(
            # Add the components of the inicio (home) page here.
            content=Text("Bienvenido al sistema de correos de yury", size=24, color="WHITE")
        )

        self.build_dashboard_page()

    # Funcion que construye la pagina de inicio con marcadores de las otras paginas
    def build_dashboard_page(self):
        # Customize the initial state of the buttons as needed
        self.listaEmp.bgcolor, self.listaEmp.color = "", ""
        self.forms.bgcolor, self.forms.color = "", ""
        self.datos.color, self.datos.bgcolor = "", ""
        self.start.color, self.start.bgcolor = "BLACK", "GREEN"
    # Funcion que construye la pagina de inicio con marcadores de las otras paginas
    def build_account_page(self):
        self.listaEmp.bgcolor, self.listaEmp.color = "", ""
        self.forms.bgcolor, self.forms.color = "", ""
        self.datos.color, self.datos.bgcolor = "BLACK", "GREEN"
        self.start.color, self.start.bgcolor = "", ""
    # Funcion que construye la pagina de inicio con marcadores de las otras paginas        
    def build_lista_emp(self):
        self.listaEmp.bgcolor, self.listaEmp.color = "GREEN", "BLACK"
        self.forms.bgcolor, self.forms.color = "", ""
        self.datos.color, self.datos.bgcolor = "", ""
        self.start.color, self.start.bgcolor = "", ""
    # Funcion que construye la pagina de inicio con marcadores de las otras paginas       
    def build_forms(self):
        self.listaEmp.bgcolor, self.listaEmp.color = "", ""
        self.forms.bgcolor, self.forms.color = "GREEN", "BLACK"
        self.datos.color, self.datos.bgcolor = "", ""
        self.start.color, self.start.bgcolor = "", ""   
    
    # funcion que obtiene datos del empleado       
    def dataemp(self,e):
        current_user = bsdinteraction()
        username=self.app_state.get_username()
        data = current_user.fetch_data(username)
        self.app_state.set_data(data)
        self.page.go("/cuenta")
        
    # funcion que desconecta al usuario             
    def disconnectt(self, e):
        self.page.go("/")
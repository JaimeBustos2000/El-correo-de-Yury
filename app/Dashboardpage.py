import flet as ft
from flet import *
from cdyury.bsdclass import bsdinteraction
from cdyury.appstatus import AppState
from datetime import datetime
from app.Loginpage import LoginPage

class DashboardPage:
    def __init__(self, page: Page, app_state):
        self.page = page
        self.app_state = app_state
        self.filters = False
        self.build_dashboard_page()

    # Función que construye la página de inicio con marcadores de las otras páginas
    def build_dashboard_page(self):
        self.listaEmp = ElevatedButton(text="Lista de empleados", on_click=lambda _: self.page.go("/tables"))
        self.start = ElevatedButton(text="Inicio", bgcolor="GREEN", color="BLACK", on_click=lambda _: self.page.go("/inicio"))
        self.forms = ElevatedButton(text="Formulario", on_click=lambda _: self.page.go("/formularios"))
        self.datos = ElevatedButton(text="Cuenta", on_click=self.dataemp)

        self.role = self.app_state.retornar_rol()
        
        print("ROL EN DASHBOARD", self.role)
        
        if self.role == "comun":
            self.filters = False
            self.listaEmp.visible = False
            self.forms.visible = False
            self.app_state.set_filters(self.filters)
        elif self.role == "pro":
            self.filters = False
            self.listaEmp.visible = True
            self.forms.visible = True
            self.app_state.set_filters(self.filters)
        elif self.role == "master":
            self.filters = True
            self.listaEmp.visible = True
            self.forms.visible = True
            self.app_state.set_filters(self.filters)
        
        self.navbar = AppBar(
            leading=IconButton(icons.DOOR_BACK_DOOR_OUTLINED, on_click=self.disconnectt),
            center_title=False,
            bgcolor="#365097",
            actions=[self.start, self.listaEmp, self.forms, self.datos]
        )

        self.inicio = Container(
            # Agregar los componentes de la página de inicio aquí.
            content=Text("Bienvenido al sistema de correos de yury", size=24, color="WHITE")
        )
        # Personaliza el estado inicial de los botones según sea necesario
        if not self.listaEmp.visible:
            pass
        else:
            self.listaEmp.bgcolor, self.listaEmp.color = "", ""
        if not self.forms.visible:
            pass
        else:
            self.forms.bgcolor, self.forms.color = "", ""
            
        self.datos.color, self.datos.bgcolor = "", ""
        self.start.color, self.start.bgcolor = "BLACK", "GREEN"
    # Funcion que construye la pagina de inicio con marcadores de las otras paginas
    def build_account_page(self):
        if not self.listaEmp.visible:
            pass
        else: 
            self.listaEmp.bgcolor, self.listaEmp.color = "", ""
        if not self.forms.visible:
            pass
        else:
            self.forms.bgcolor, self.forms.color = "", ""
            
        self.datos.color, self.datos.bgcolor = "BLACK", "GREEN"
        self.start.color, self.start.bgcolor = "", ""
    # Funcion que construye la pagina de inicio con marcadores de las otras paginas        
    def build_lista_emp(self):
        if not self.listaEmp.visible:
            pass
        else:
            self.listaEmp.bgcolor, self.listaEmp.color = "GREEN", "BLACK"
        
        if not self.forms.visible:
            pass
        else:
            self.forms.bgcolor, self.forms.color = "", ""
            
        self.datos.color, self.datos.bgcolor = "", ""
        self.start.color, self.start.bgcolor = "", ""
    # Funcion que construye la pagina de inicio con marcadores de las otras paginas       
    def build_forms(self):
        if not self.listaEmp.visible:
            pass
        else:
            self.listaEmp.bgcolor, self.listaEmp.color = "", ""
            
        if not self.forms.visible:
            pass
        else:
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
        
    def return_role(self):
        self.role = self.app_state.get_rol()
        return self.role
    # funcion que desconecta al usuario             
    def disconnectt(self, e):
        self.page.go("/")
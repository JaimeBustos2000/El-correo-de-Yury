import flet as ft
from flet import *
from cdyury.bsdclass import bsdinteraction
from cdyury.appstatus import AppState

class LoginPage:
    def __init__(self, page:Page,app_state):
        self.page = page
        self.state=app_state
        self.build_login_page()
        
    def build_login_page(self):
        self.text_user = TextField(
            border_radius=20, label="Usuario", label_style=TextStyle(color="#ffffff"),
            border_color="#198357", text_size=20, value="",color="WHITE"
        )
        
        self.text_pass = TextField(
            border_radius=20, label="Contraseña", label_style=TextStyle(color="#ffffff"),
            border_color="#198357", text_size=20, password=True, value="",color="WHITE",can_reveal_password=True
        )

        self.ingresobtn = ElevatedButton(
            "Ingresar", bgcolor="green", color="white", scale=1.5, on_click=self.inicio
        )
        
        self.forgotpass = TextButton(
            "Es nuevo en la plataforma? Registrese aqui!",
            scale=1.5, style=(ButtonStyle(color="#ffffff")), on_click=self.go_register
        )

        self.login_card = Card(
            width=500, height=500, color="#3e4784", elevation=5,
            content=Container(
                border_radius=15, bgcolor="#283757",
                content=Column(
                    width=200, height=200, spacing=5,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    controls=[
                        Divider(height=20, color="transparent"),
                        Text("LOGIN", size=23, color="#ffffff"),
                        Divider(height=20, color="transparent"),
                        Text("Usuario", size=23, color="#ffffff"),
                        Container(height=70, width=320, content=Row(alignment=MainAxisAlignment.CENTER, controls=[self.text_user])),
                        Text("Contraseña", size=23, color="white"),
                        Container(height=70, width=320, content=Row(alignment=MainAxisAlignment.CENTER, controls=[self.text_pass])),
                        Divider(height=30, color="transparent"),
                        self.ingresobtn,
                        Divider(height=20, color="transparent"),
                        self.forgotpass
                    ]
                )
            )
        )
    
    def inicio(self, e):
        user = self.get_username()
        password = self.get_password()
        conexion = bsdinteraction()
        validacion = conexion.login(user, password)
        if validacion:
            self.state.set_username(user)
            self.page.go("/inicio")
        else:
            self.show_error_dialog("Usuario o contraseña incorrectos, ingrese nuevamente")

    def go_register(self, e):
        self.page.go("/crear_cuenta")
        
    def get_username(self):
        return self.text_user.value
    
    def get_password(self):
        return self.text_pass.value

    def show_error_dialog(self, message):
        dialog = AlertDialog(title=Text(message))
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()
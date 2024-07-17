import flet as ft
from flet import *
from cdyury.bsdclass import bsdinteraction
from datetime import datetime
import time

class RegisterPage:
    def __init__(self, page:Page):
        self.page = page
        self.build_register_page()
    
    def build_register_page(self):
        self.rut_user = TextField(
            border_radius=20, label="Rut", color="#ffffff",
            label_style=TextStyle(color="#ffffff"), border_color="#22AF74",
            text_size=20, value=""
        )

        self.verify_button = TextButton(
            text="Verificar", scale=1.5,
            style=(ButtonStyle(bgcolor="GREEN", color="#ffffff")),
            on_click=self.new_user
        )

        self.volver_button = TextButton(
            "Volver", scale=1.5, style=(ButtonStyle(color="#ffffff")),
            on_click=self.go_login
        )

        self.register_card = Card(
            width=500, height=500, color="#3e4784", elevation=5,
            content=Container(
                border_radius=15, bgcolor="#283757",
                content=Column(
                    width=200, height=200, spacing=5,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    controls=[
                        Divider(height=20, color="transparent"),
                        Text("Ingresa tu rut sin puntos y con guion", size=23, color="#ffffff"),
                        Divider(height=50, color="transparent"),
                        self.rut_user,
                        Divider(height=20, color="transparent"),
                        self.verify_button,
                        Divider(height=20, color="transparent"),
                        self.volver_button
                    ]
                )
            )
        )
    
    # Funcion que verifica si el rut ingresado es correcto y si no existe en la base de datos,
    # si es correcto y no existe, se procede a crear el usuario
    def new_user(self, e):
        rut = self.rut_user.value
        conexion = bsdinteraction()
        validate = conexion.check_user(rut)
        
        if validate:
            dialog = AlertDialog(title=Text("Usuario creado correctamente, su usario consta de su nombre y las primeras dos letras de su apellido, si necesita algún privilegio contacte a su supervisor"))
            self.page.dialog = dialog
            dialog.open = True
            self.rut_user.value = ""
            self.page.update()
            time.sleep(4)
            self.page.go("/")
        else:
            self.show_error_dialog("El rut ingresado no corresponde o ya existe un usuario, si se trata de un error, contacte a su supervisor o intente ingresarlo nuevamente")
    
    def go_login(self, e):
        self.page.go("/")
    
    def show_error_dialog(self, message):
        dialog = AlertDialog(title=Text(message))
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()
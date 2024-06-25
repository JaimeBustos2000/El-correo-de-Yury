import flet as ft
from flet import *
from bsdclass import bsdinteraction
from appstatus import AppState
from datetime import datetime
import sqlite3
import time



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
        conexion.duplicate()
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
            content=Text("Welcome to the Dashboard", size=24, color="WHITE")
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

class ProfilePage:
    def __init__(self, page: Page,app_state):
        self.page = page
        self.app_state = app_state
        self.build_profile_page()
        self.load_contactos_emergencia()
        self.load_cargas_familiares()

    def date(self):
        return datetime.now().strftime("%d-%m-%Y")

    def build_profile_page(self):
        self.nombre = TextField(value="", color="WHITE", height=40, read_only=True, bgcolor="BLACK", label="Nombre",label_style=TextStyle(color="WHITE"))
        self.apellido = TextField(value="", color="WHITE", height=40, read_only=True, bgcolor="BLACK", label="Apellido",label_style=TextStyle(color="WHITE"))
        self.rut = TextField(value="", color="WHITE", height=40, read_only=True, bgcolor="BLACK", label="Rut",label_style=TextStyle(color="WHITE"))
        self.genero = TextField(value="", color="WHITE", height=40, read_only=True, bgcolor="BLACK", label="Genero",label_style=TextStyle(color="WHITE"))

        self.select_genero = Dropdown(value = self.genero.value,options=[
            dropdown.Option("F"),
            dropdown.Option("M"),
        ],
            visible=False)

        self.direccion = TextField(value="", color="WHITE", height=60,width=450, read_only=True, bgcolor="BLACK", label="Direccion",label_style=TextStyle(color="WHITE"))
        self.telefono = TextField(value="", color="WHITE", height=40, read_only=True, bgcolor="BLACK", label="Telefono",label_style=TextStyle(color="WHITE"))
        self.cargo = TextField(value="", color="WHITE", height=40, read_only=True, bgcolor="BLACK", label="Cargo",label_style=TextStyle(color="WHITE"))
        self.fecha = TextField(value="", color="WHITE", height=40, read_only=True, bgcolor="BLACK", label="Fecha de ingreso",label_style=TextStyle(color="WHITE"))
        self.area = TextField(value="", color="WHITE", height=40, read_only=True, bgcolor="BLACK", label="Departamento",label_style=TextStyle(color="WHITE"))

        self.contactos_emergencia = []
        self.cargas_familiares = []


        self.cargas_familiares_actual, self.contactos_emergencia_actual = self.app_state.obtener_cargas_contactos(self.rut.value)

        self.contactos_emergencia_container = Column()
        self.cargas_familiares_container = Column()

        self.btn_edit = IconButton(icon="edit", on_click=self.enable_edit)
        self.btn_agregar_contacto = IconButton(icon="add", on_click=self.agregar_contacto_emergencia)
        self.btn_eliminar_contacto = IconButton(icon="remove", on_click=self.eliminar_contacto_emergencia)
        self.btn_agregar_carga = IconButton(icon="add", on_click=self.agregar_carga_familiar)
        self.btn_eliminar_carga = IconButton(icon="remove", on_click=self.eliminar_carga_familiar)
        self.save = TextButton(text="Guardar", on_click=self.save_data)


        self.eliminar_contacto_dialog = AlertDialog(
        title=Text("Eliminar Contacto de Emergencia"),
        content=Column([
            TextField(label="Nombre del Contacto", color="BLACK", height=40, bgcolor="WHITE"),
            TextButton(text="Eliminar", on_click=self.confirmar_eliminar_contacto_emergencia)]))

        self.eliminar_carga_dialog = AlertDialog(
        title=Text("Eliminar Carga Familiar"),
        content=Column([
            TextField(label="Nombre de la Carga", color="BLACK", height=40, bgcolor="WHITE"),
            TextButton(text="Eliminar", on_click=self.confirmar_eliminar_carga_familiar)]))

        self.btn_eliminar_contacto = IconButton(icon="remove", on_click=self.mostrar_eliminar_contacto_dialog)
        self.btn_eliminar_carga = IconButton(icon="remove", on_click=self.mostrar_eliminar_carga_dialog)

        # Cargas familiares
        self.carga_rut = TextField(value="", color="WHITE", height=40, bgcolor="BLACK", label="Rut")
        self.carga_nombre = TextField(value="", color="WHITE", height=40, bgcolor="BLACK", label="Nombre")
        self.genero_carga = Dropdown(label="Genero", label_style=TextStyle(color="BLACK"), width=200, color="BLACK", options=[
            dropdown.Option("F"),
            dropdown.Option("M")
        ])

        self.parentesco_carga = Dropdown(label="Relacion", label_style=TextStyle(color="BLACK"), width=200, color="BLACK", options=[
            dropdown.Option("1", text="Padre"),
            dropdown.Option("2", text="Madre"),
            dropdown.Option("3", text="Hijo/a"),
            dropdown.Option("4", text="Hermano/a"),
            dropdown.Option("5", text="Primo/a"),
            dropdown.Option("6", text="Conyuge")
        ])

        # Contactos de emergencia
        self.contacto_nombre = TextField(value="", color="WHITE", height=40, bgcolor="BLACK", label="Nombre")
        self.contacto_relacion = Dropdown(label="Relacion", label_style=TextStyle(color="BLACK"), width=200, color="WHITE", options=[
            dropdown.Option("1", text="Padre"),
            dropdown.Option("2", text="Madre"),
            dropdown.Option("3", text="Hijo/a"),
            dropdown.Option("4", text="Hermano/a"),
            dropdown.Option("5", text="Primo/a"),
            dropdown.Option("6", text="Conyuge")
        ])
        self.contacto_telefono = TextField(value="", color="WHITE", height=40, bgcolor="BLACK", label="Telefono")

        # Contenedor de la información del usuario
        user_info_container = Column(
            spacing=5,
            controls=[
                Column(controls=[
                    Text(value="Datos personales", font_family="Segoe UI", color="WHITE", size=30),
                    Row(width=1000, controls=[Row(vertical_alignment=CrossAxisAlignment.END, controls=[self.btn_edit])]),
                    Divider(height=5, color="transparent"),
                    Row(controls=[
                        self.nombre,
                        self.apellido,
                        self.rut
                    ]),
                    Row(controls=[
                        self.genero, self.select_genero,
                        self.telefono
                    ]),
                    Row(controls=[self.direccion]),
                    Row(controls=[
                        self.cargo,
                        self.fecha,
                        self.area
                    ])
                ]),
                Divider(height=20, color="transparent"),
                Column(controls=[
                    Text(value="Contactos de emergencia", font_family="Segoe UI", color="WHITE", size=30),

                    self.contactos_emergencia_container,
                    Row(controls=[self.btn_agregar_contacto, self.btn_eliminar_contacto])
                ]),
                Divider(height=20, color="transparent"),
                Column(controls=[
                    Text(value="Cargas familiares", font_family="Segoe UI", color="WHITE", size=30),
                    self.cargas_familiares_container,
                    Row(controls=[self.btn_agregar_carga, self.btn_eliminar_carga])
                ], ),
                Row(controls=[self.save])
            ],
            scroll=True, expand=1
        )

        self.cuenta = Card(
            width=1366,
            height=628,
            elevation=5,
            content=Container(
                border_radius=2,
                bgcolor="#162E2B",
                content=user_info_container
            )
        )
    # Funcion que carga los contactos que tiene el trabajador
    def load_contactos_emergencia(self):
        contactos=self.app_state.obtener_cargas_contactos(self.rut.value)[1]
        print(contactos)
        
        if contactos:
            self.contactos_emergencia_container.controls.clear()
            for row in contactos:
                contacto = Row(controls=[
                    TextField(value=row[0], color="WHITE", height=40, read_only=True, bgcolor="BLACK", label="Nombre",label_style=TextStyle(color="WHITE")),
                    TextField(value=row[1], color="WHITE", height=40, read_only=True, bgcolor="BLACK", label="Parentesco",label_style=TextStyle(color="WHITE")),
                    TextField(value=row[2], color="WHITE", height=40, read_only=True, bgcolor="BLACK", label="Teléfono",label_style=TextStyle(color="WHITE"))
                ])
                self.contactos_emergencia_container.controls.append(contacto)
            self.page.update()
        else:
            print("No hay contactos de emergencia")

    # Funcion que carga las cargas familiares que tiene el trabajador
    def load_cargas_familiares(self):
        cargas=self.app_state.obtener_cargas_contactos(self.rut.value)[0]
        print(cargas)
        self.cargas_familiares_container.controls.clear()
        if cargas:
            
            for row in cargas:
                carga = Row(controls=[
                    TextField(value=row[0], color="WHITE", height=40, read_only=True, bgcolor="BLACK", label="Nombre",label_style=TextStyle(color="WHITE")),
                    TextField(value=row[1], color="WHITE", height=40, read_only=True, bgcolor="BLACK", label="Parentesco",label_style=TextStyle(color="WHITE"))
                ])
                self.cargas_familiares_container.controls.append(carga)
            self.page.update()
        else:
            print("No hay cargas familiares")

    # Funcion que eliminar un contacto de emergencia
    def mostrar_eliminar_contacto_dialog(self, e):
        self.page.dialog = self.eliminar_contacto_dialog
        self.eliminar_contacto_dialog.open = True
        self.page.update()

    # Funcion que elimina una carga familiar
    def mostrar_eliminar_carga_dialog(self, e):
        self.page.dialog = self.eliminar_carga_dialog
        self.eliminar_carga_dialog.open = True
        self.page.update()
    
    # Funcion que confirma la eliminacion de un contacto de emergencia
    def confirmar_eliminar_contacto_emergencia(self, e):
        nombre_contacto = self.eliminar_contacto_dialog.content.controls[0].value
        trabajador_rut = self.rut.value
        self.eliminar_contacto_por_nombre(nombre_contacto, trabajador_rut)
        self.load_contactos_emergencia()
        self.eliminar_contacto_dialog.open = False
        self.page.update()

    # Funcion que confirma la eliminacion de una carga familiar
    def confirmar_eliminar_carga_familiar(self, e):
        nombre_carga = self.eliminar_carga_dialog.content.controls[0].value
        trabajador_rut = self.rut.value
        self.eliminar_carga_por_nombre(nombre_carga, trabajador_rut)
        self.load_cargas_familiares()
        self.eliminar_carga_dialog.open = False
        self.page.update()

    # Añade una interfaz para agregar contactos de emergencia
    def agregar_contacto_emergencia(self, e):
        nombre_contacto = TextField(value="", color="WHITE", height=40, bgcolor="BLACK", label="Nombre", label_style=TextStyle(color="WHITE"))
        relacion_contacto = Dropdown(width=200, color="BLACK", label="Relación", label_style=TextStyle(color="WHITE"), options=[
            dropdown.Option("1",text="Padre"),
            dropdown.Option("2",text="Madre"),
            dropdown.Option("3",text="Hijo/a"),
            dropdown.Option("4",text="Hermano/a"),
            dropdown.Option("5",text="Primo/a"),
            dropdown.Option("6",text="Conyuge")
        ])
        telefono_contacto = TextField(value="", color="WHITE", height=40, bgcolor="BLACK", label="Teléfono", label_style=TextStyle(color="WHITE"))

        nuevo_contacto = Row(controls=[nombre_contacto, relacion_contacto, telefono_contacto])

        self.contactos_emergencia_container.controls.append(nuevo_contacto)
        self.page.update()

        self.contactos_emergencia.append({
            'nombre': nombre_contacto,
            'relacion': relacion_contacto,
            'telefono': telefono_contacto
        })

    # Elimina el contacto de emergencia de la pantalla actual
    def eliminar_contacto_emergencia(self, e):
        if self.contactos_emergencia:
            contacto = self.contactos_emergencia.pop()
            nombre_contacto = contacto['nombre'].value
            trabajador_rut = self.rut.value
            self.eliminar_contacto_por_nombre(nombre_contacto, trabajador_rut)
            self.contactos_emergencia_container.controls.pop()
        self.page.update()
        
    # Elimina la carga familiar de la pantalla actual por nombre
    def eliminar_carga_por_nombre(self, nombre, trabajador_rut):
        conn = sqlite3.connect("correosyury.db")
        cur = conn.cursor()
        cur.execute("DELETE FROM CargaEmp WHERE nombre=? AND trabajador_rut=?", (nombre, trabajador_rut))
        conn.commit()
        conn.close()

    #   Elimina el contacto de emergencia de la pantalla actual por nombre
    def eliminar_contacto_por_nombre(self, nombre, trabajador_rut):
        conn = sqlite3.connect("correosyury.db")
        cur = conn.cursor()
        cur.execute("DELETE FROM ContactosEmp WHERE nombre=? AND trabajador_rut=?", (nombre, trabajador_rut))
        conn.commit()
        conn.close()

    # Añade la interfaz de carga familiar a la pantalla
    def agregar_carga_familiar(self, e):
        rut_carga = TextField(value="", color="BLACK", height=40, bgcolor="WHITE", label="Rut", label_style=TextStyle(color="BLACK"))
        nombre_carga = TextField(value="", color="BLACK", height=40, bgcolor="WHITE", label="Nombre", label_style=TextStyle(color="BLACK"))
        genero_carga = Dropdown(value="",width=200, color="WHITE", label="Género", label_style=TextStyle(color="BLACK"), options=[
            dropdown.Option("F"),
            dropdown.Option("M")
        ])
        parentesco_carga = Dropdown(width=200, color="WHITE", label="Parentesco", label_style=TextStyle(color="BLACK"), options=[
            dropdown.Option("1",text="Padre"),
            dropdown.Option("2",text="Madre"),
            dropdown.Option("3",text="Hijo/a"),
            dropdown.Option("4",text="Hermano/a"),
            dropdown.Option("5",text="Primo/a"),
            dropdown.Option("6",text="Conyuge")
        ])

        nueva_carga = Row(controls=[rut_carga, nombre_carga, genero_carga, parentesco_carga])

        self.cargas_familiares_container.controls.append(nueva_carga)
        self.page.update()

        self.cargas_familiares.append({
            'rut': rut_carga,
            'nombre': nombre_carga,
            'genero': genero_carga,
            'parentesco': parentesco_carga
        })

    # Funcion que eliminar una carga familiar de la pantalla
    def eliminar_carga_familiar(self, e):
        if self.cargas_familiares:
            carga = self.cargas_familiares.pop()
            nombre_carga = carga['nombre'].value
            trabajador_rut = self.rut.value
            self.eliminar_carga_por_nombre(nombre_carga, trabajador_rut)
            self.cargas_familiares_container.controls.pop()
        self.page.update()

    # funcion que obtiene los datos editables, para luego ser guardados
    def obtener_contactos_emergencia(self):
        contactos_data = []
        for contacto in self.contactos_emergencia:
            contactos_data.append({
                "nombre": contacto['nombre'].value,
                "relacion": contacto['relacion'].value,
                "telefono": contacto['telefono'].value,
            })
        return contactos_data

    # funcion que obtiene las cargas familiares, para luego ser guardadas
    def obtener_cargas_familiares(self):
        cargas_data = []
        for carga in self.cargas_familiares:
            cargas_data.append({
                "rut": carga['rut'].value,
                "nombre": carga['nombre'].value,
                "relacion": carga['genero'].value,
                "parentesco": carga['parentesco'].value,
            })
        return cargas_data

    # funcion que obtiene los datos editables del trabajador
    def obtener_datos_editables(self, e):
        self.nombre.on_change = self.obtener_datos_editables
        self.select_genero.on_change = self.obtener_datos_editables
        self.direccion.on_change = self.obtener_datos_editables
        self.telefono.on_change = self.obtener_datos_editables

        genero = self.select_genero.value
        nombre = self.nombre.value
        direccion = self.direccion.value
        telefono = self.telefono.value

        datap = [genero, nombre, direccion, telefono]

        return datap

    # funcion que guarda los datos editables del trabajador y comprueba si hay cambios y demas
    def save_data(self, e):
        if not self.hay_cambios():
            self.show_error_dialog("No se han realizado cambios.")
            return

        genero_actual = self.select_genero.value if self.select_genero.visible else self.genero.value
        nombre_actual = self.nombre.value
        direccion_actual = self.direccion.value
        telefono_actual = self.telefono.value
        trabajador_rut = self.rut.value  # Rut del trabajador que ha iniciado sesión

        # Actualizar datos principales del empleado en la base de datos
        if self.app_state.update_employee_data(trabajador_rut, genero_actual, nombre_actual, direccion_actual, telefono_actual):
            # Obtener datos de cargas familiares y contactos de emergencia
            cargas = self.obtener_cargas_familiares()
            contactos = self.obtener_contactos_emergencia()
            print(cargas)
            try:        
                # Guardar nuevas cargas familiares
                if cargas:
                    for carga in cargas:
                        rut = carga['rut']
                        nombre = carga['nombre']
                        genero = carga['relacion']
                        parentesco = carga['parentesco']
                        if rut and nombre and genero and parentesco:
                            self.app_state.add_carga_familiar(rut, nombre, genero, parentesco, trabajador_rut)

                if contactos:
                # Guardar nuevos contactos de emergencia
                    for contacto in contactos:
                        nombre = contacto['nombre']
                        relacion = contacto['relacion']
                        telefono = contacto['telefono']
                        if nombre and relacion and telefono:
                            self.app_state.add_contacto_emergencia(nombre, relacion, telefono, trabajador_rut)

                # Mostrar mensaje de éxito
                alt = AlertDialog(title=Text("Datos guardados"))
                self.page.dialog = alt
                alt.open = True
                self.page.update()
                time.sleep(2)
                self.select_genero.visible = False
                self.genero.visible = True
                self.page.go("/inicio")
            except Exception as ex:
                self.show_error_dialog(f"Error al guardar datos: {str(ex)}")
        else:
            self.show_error_dialog("Error al guardar datos en la base de datos.")


    def validar_rut(self, rut):
        # Verificar el formato del RUT
        if len(rut) >= 9 and len(rut) <= 10 and not rut.endswith("-"):
            return True
        else:
            return False

    def hay_cambios(self):
        # Obtener datos actuales del formulario
        genero_actual = self.select_genero.value
        nombre_actual = self.nombre.value
        direccion_actual = self.direccion.value
        telefono_actual = self.telefono.value

        # Comparar con los datos originales obtenidos al cargar la página
        return (genero_actual != self.genero.value or
                nombre_actual != self.nombre.value or
                direccion_actual != self.direccion.value or
                telefono_actual != self.telefono.value)

    def show_error_dialog(self, message):
        dialog = AlertDialog(title=Text(message))
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def show_data(self):
        data = self.app_state.get_data()
        if data:
            self.rut.value = data[0][0]
            self.nombre.value = data[0][1]
            self.apellido.value = data[0][2]
            self.genero.value = data[0][3]
            self.fecha.value = data[0][4]
            self.cargo.value = data[0][5]
            self.area.value = data[0][6]
            self.direccion.value = data[0][7]
            self.telefono.value = data[0][8]

            self.area.value = data[0][6]
            self.load_cargas_familiares()
            self.load_contactos_emergencia()
            self.page.update()
        else:
            alt = AlertDialog(title=Text("No se pudieron obtener los datos personales. Intente iniciar sesión nuevamente."))
            self.page.dialog = alt
            alt.open = True
            self.page.update()

    def enable_edit(self, e):
        alt = AlertDialog(title=(Text("Edición habilitada")))
        self.page.dialog = alt
        alt.open = True
        self.page.update()

        self.genero.visible = False
        self.select_genero.visible = True
        self.nombre.read_only = False
        self.direccion.read_only = False
        self.telefono.read_only = False

        # Asegurar que todos los contactos de emergencia y cargas familiares actuales sean editables
        for contacto in self.contactos_emergencia:

            for persona in contacto:
                persona['nombre'].read_only = False
                persona['relacion'].enabled = True
                persona['telefono'].read_only = False

        for carga in self.cargas_familiares:

            carga['rut'].read_only = False
            carga['nombre'].read_only = False
            carga['genero'].enabled = True
            carga['parentesco'].enabled = True

        self.page.update()


    def get_card(self):
        self.nombre.read_only = True
        self.genero.read_only = True
        self.direccion.read_only = True
        self.telefono.read_only = True
        return self.cuenta



# CLASE QUE CONTROLA EL FORMULARIO DE INGRESO DE DATOS
class FormPage:
    def __init__(self,page:Page,app_state):
        self.page=page
        self.app_state=app_state
        self.build_forms()
         
    def build_forms(self):
    #TEXTFIELDS PARA FORMULARIOS
        ##DATOS PERSONALES 
        self.rut=TextField(value="",color="BLACK",width=200, hint_text="Rut con guion")
        self.nombres=TextField(value="",color="BLACK",width=200)
        self.apellidos=TextField(value="",color="BLACK",width=200)
        self.sexo=Dropdown(label="Sexo",width=100,options=[dropdown.Option("M"),dropdown.Option("F")])
        self.calle=TextField(value="", width=200)
        self.complemento=TextField(value="", width=200)
        self.comuna=Dropdown(width=200,options=[
            dropdown.Option("Santiago"),
            dropdown.Option("Providencia"),
            dropdown.Option("Las Condes"),
            dropdown.Option("La Florida"),
            dropdown.Option("Puente Alto"),
            dropdown.Option("Ñuñoa"),
            dropdown.Option("Maipú"),
            dropdown.Option("La Reina"),
            dropdown.Option("Vitacura"),
            dropdown.Option("Peñalolén"),
            ])
        self.telefono=TextField(value="",color="BLACK",width=200)

        #DATOS LABORALES
        self.cargo=Dropdown(width=200,options=[
            dropdown.Option("Jefe de envios"),
            dropdown.Option("Gerente de RR.HH."),
            dropdown.Option("Personal de RR.HH."),
            dropdown.Option("Repartidor"),
            ])

        # Fecha ingreso
        fecha_actual=datetime.now()
        fecha_actual=fecha_actual.strftime("%d-%m-%Y")
        self.fecha=TextField(value=f"{fecha_actual}",color="BLACK",width=200, hint_text="Fecha de ingreso",text_size=15,text_align="CENTER")
        
        self.areaDepto=Dropdown(width=200,options=[
            dropdown.Option("envios"),
            dropdown.Option("recursos humanos"),
            ])

        #DATOS DE CONTACTO
        self.contacto1=TextField(value="",color="BLACK",width=200)
        self.contacto2=TextField(value="",color="BLACK",width=200)

        self.relacion1=Dropdown(width=200,color="WHITE",options=[
            dropdown.Option("Padre"),
            dropdown.Option("Madre"),
            dropdown.Option("Hijo/a"),
            dropdown.Option("Hermano/a"),
            dropdown.Option("Primo/a"),
            dropdown.Option("Conyuge")
            ])
        
        self.relacion2=Dropdown(width=200,color="WHITE",options=[
            dropdown.Option("Padre"),
            dropdown.Option("Madre"),
            dropdown.Option("Hijo/a"),
            dropdown.Option("Hermano/a"),
            dropdown.Option("Primo/a"),
            dropdown.Option("Conyuge")
            ])

        self.fonocon1=TextField(value="",color="BLACK",width=200)
        self.fonocon2=TextField(value="",color="BLACK",width=200)

        #DATOS DE CARGA FAMILIAR
        #carga 1
        self.rut_carga1=TextField(value="",color="BLACK",width=200)
        self.nombre_carga1=TextField(value="",color="BLACK",width=200)

        self.genero_carga1=Dropdown(width=200,options=[
            dropdown.Option("F"),
            dropdown.Option("M")])

        self.parentesco1=Dropdown(width=200,color="WHITE",options=[
            dropdown.Option("Padre"),
            dropdown.Option("Madre"),
            dropdown.Option("Hijo/a"),
            dropdown.Option("Hermano/a"),
            dropdown.Option("Primo/a"),
            dropdown.Option("Conyuge")
            ])

        #carga 2
        self.rut_carga2=TextField(value="",color="BLACK",width=200)
        self.nombre_carga2=TextField(value="",color="BLACK",width=200)

        self.genero_carga2=Dropdown(width=200,options=[
            dropdown.Option("F"),
            dropdown.Option("M")])

        self.parentesco2=Dropdown(width=200,color="WHITE",options=[
            dropdown.Option("Padre"),
            dropdown.Option("Madre"),
            dropdown.Option("Hijo/a"),
            dropdown.Option("Hermano/a"),
            dropdown.Option("Primo/a"),
            dropdown.Option("Conyuge")
            ])
        
        # FORMULARIO DATOS PERSONALES
        dataP=Container(
                width=1366,
                height=150,
                bgcolor="#476EAA",
                content=Column(
                    spacing=1,
                    horizontal_alignment=CrossAxisAlignment.START,
                    controls=[
                        Row(controls=[
                            
                            self.nombres,
                            
                            self.apellidos,
                            
                            self.rut,
                            
                            self.sexo
                        ]),
                        Row(width=100)
                        ,
                        Row(controls=[
                            self.calle,
                            self.complemento,
                            self.comuna, 
                            self.telefono  
                        ]    
                        )  
                    ]
                )
            )        
        # FORMULARIO DATOS LABORALES
        dataL=Container(
                width=1366,
                height=100,
                bgcolor="#476EAA",
                content=Column(
                    spacing=1,
                    horizontal_alignment=CrossAxisAlignment.START,
                    controls=[
                        Row(controls=[
                            Text(value="CARGO",size=20),
                            self.cargo,
                            Text(value="FECHA DE INGRESO",size=20),
                            self.fecha,
                            Text(value="AREA-DEPTO",size=20),
                            self.areaDepto
                        ])
                    ]
                )
            )
        # FORMULARIO CONTACTOS DE EMERGENCIA
        dataC=Container(
            width=1366,
            height=120,
            bgcolor="#476EAA",
            content=Column(
                spacing=4,
                horizontal_alignment=CrossAxisAlignment.START,
                controls=[
                    Row(controls=[
                        Text(value="Nombre contacto",size=20),
                        self.contacto1,
                        Text(value="RELACION",size=20),
                        self.relacion1,
                        Text(value="TELEFONO",size=20),
                        self.fonocon1
                    ]),
                    Row(controls=[
                        Text(value="Nombre contacto",size=20),
                        self.contacto2,
                        Text(value="RELACION",size=20),
                        self.relacion2,
                        Text(value="TELEFONO",size=20),
                        self.fonocon2 
                    ])
                ]
            )
        )
        # FORMULARIO CARGAS FAMILIARES
        dataF=Container(
            width=1366,
            height=120,
            bgcolor="#476EAA",
            content=Column(
                spacing=4,
                horizontal_alignment=CrossAxisAlignment.START,
                controls=[
                    Row(controls=[
                        Text(value="Rut",size=20),
                        self.rut_carga1,
                        Text(value="Nombre",size=20),
                        self.nombre_carga1,
                        Text(value="Genero",size=20),
                        self.genero_carga1,
                        Text(value="Parentesco",size=20),
                        self.parentesco1
                    ]),
                    Row(controls=[
                        Text(value="Rut",size=20),
                        self.rut_carga2,
                        Text(value="Nombre",size=20),
                        self.nombre_carga2,
                        Text(value="Genero",size=20),
                        self.genero_carga2,
                        Text(value="Parentesco",size=20),
                        self.parentesco2
                    ])
                ]
            )
        )        
        
        # FORMULARIO COMPLETO
        self.form_state=Column(
            spacing=5,
            horizontal_alignment=CrossAxisAlignment.CENTER,
            controls=[
                Divider(height=5,color="transparent"),
                Row(vertical_alignment=CrossAxisAlignment.START,
                    controls=[
                        Row(width=600),
                        Text(value="DATOS PERSONALES",color="BLACK",size=20),
                        Row(width=200,vertical_alignment=CrossAxisAlignment.END),
                        Row(vertical_alignment=CrossAxisAlignment.END,
                            controls=[                                    
                                TextButton(text="Enviar",style=ButtonStyle(bgcolor="GREEN",color="#ffffff"),on_click=self.validation_pass_form),
                                Text("Comprobar rut: ",color="BLACK"),
                                Checkbox(fill_color="WHITE",on_change=self.dni_comp)])]),
                dataP,
                Divider(height=5,color="transparent"),
                Text(value="DATOS LABORALES",color="BLACK",size=20),
                dataL,
                Divider(height=5,color="transparent"),
                Text(value="CONTACTOS DE EMERGENCIA",color="BLACK",size=20),
                dataC,
                Divider(height=5,color="transparent"),
                Text(value="CARGAS FAMILIARES",color="BLACK",size=20),
                dataF])
        # CARTA QUE CONTIENE EL FORMULARIO
        self.formulario=Card(
            width=1366,
            height=800,
            color="#FFFFFF",
            elevation=5,
            content=Container(
                border_radius=5,
                bgcolor="#B2DFF5",
                content=self.form_state))
    # RETORNA LA INTERFAZ COMPLETA
    def get_card(self):
        return self.formulario

    # CREA UN DICCIONARIO DE DATOS DE LOS FORMULARIOS
    def get_data(self):
        formulario = {
            "DataEmpleado": {
                "nombres": self.nombres.value,
                "apellidos": self.apellidos.value,
                "rut": self.rut.value,
                "sexo": self.sexo.value,
                "direccion": self.direccion.value,
                "telefono": self.telefono.value,
                "cargo": self.cargo.value,
                "fecha": self.fecha.value,
                "areaDepto": self.areaDepto.value
            },
            "ContactosEmp": [
                {
                    "nombre": self.contacto1.value,
                    "relacion": self.relacion1.value,
                    "telefono": self.fonocon1.value
                },
                {
                    "nombre": self.contacto2.value,
                    "relacion": self.relacion2.value,
                    "telefono": self.fonocon2.value
                    }
                ],
            "CargaEmp": [
                    {
                        "rut": self.rut_carga1.value,
                        "nombre": self.nombre_carga1.value,
                        "genero": self.genero_carga1.value,
                        "parentesco": self.parentesco1.value
                    },
                    {
                        "rut": self.rut_carga2.value,
                        "nombre": self.nombre_carga2.value,
                        "genero": self.genero_carga2.value,
                        "parentesco": self.parentesco2.value
                    }
                ]
        }
        return formulario
        
    # VALIDA QUE LOS CAMPOS NO ESTEN VACIOS Y QUE EL RUT SEA VALIDO CON EL BOTON
    def dni_comp(self,e):
        self.__bsd=bsdinteraction()
        rut=self.rut.value
        print(rut)
        print(len(rut))
        dni_exist=self.__bsd.check_user(rut)
        print(dni_exist)
        
        if 11>len(rut)<9 or rut=="":            
            alt = AlertDialog(title=Text("Ingrese un rut valido"))  # MENSAJE DE ALERTA
            self.page.dialog = alt
            alt.open = True
            self.page.update()
        else:
            if dni_exist:
                alt = AlertDialog(title=Text("Rut ya existe"))  
                self.page.dialog = alt
                alt.open = True
                self.page.update()
            else:
                alt = AlertDialog(title=Text("Rut disponible"))  
                self.page.dialog = alt
                alt.open = True
                self.page.update()
    
    # VALIDA QUE LOS CAMPOS NO ESTEN VACIOS Y QUE EL RUT SEA VALIDO AL INGRESAR COMO DATO NUEVO
    def campo_vacio(self):
        def validar_rut(rut):
            return 8 < len(rut) < 11 and not rut.endswith("-")

        # Validar que un campo no esté vacío
        def validar_campo(campo, clave=None):
            # Validar sexo/género para que solo sea "F" o "M"
            if clave in ["sexo", "genero"]:
                return campo in ["F", "M"]
            return len(campo) >= 3

        # Validar que todos los campos de un diccionario estén vacíos
        def todos_vacios(d):
            return all(not v for v in d.values())

        # Validar que al menos un campo de un diccionario esté lleno
        def validar_parcial(d):
            return any(d.values()) and not all(d.values())

        # Obtener los datos del formulario
        formulario = self.get_data()

        # Llamada a las funciones de validación
        for key, section in formulario.items():
            if isinstance(section, dict):
                for subkey, value in section.items():
                    if isinstance(value, dict):  # Si es un diccionario anidado, iterar sobre sus elementos
                        if subkey in ["contacto2", "Carga2"]:
                            if todos_vacios(value):
                                continue  # Si todos los campos están vacíos, saltar la validación
                            if validar_parcial(value):
                                return True, f"Error: todos los campos en {subkey} deben estar completos."
                        for subsubkey, subvalue in value.items():
                            if subsubkey == "rut":
                                if not validar_rut(subvalue):
                                    return True, f"Error: el RUT en {subkey} es inválido."
                            elif not validar_campo(subvalue, subsubkey):
                                return True, f"Error: el campo {subsubkey} en {subkey} debe tener al menos 5 caracteres o ser F/M para género."
                    else:
                        if subkey == "rut":
                            if not validar_rut(value):
                                return True, "Error: el RUT es inválido."
                        elif not validar_campo(value, subkey):
                            return True, f"Error: el campo {subkey} debe tener al menos 5 caracteres o ser F/M para género."

        # Validar ContactosEmp y CargaEmp pueden estar vacíos, pero no incompletos
        for section_key in ["ContactosEmp", "CargaEmp"]:
            if section_key in formulario:
                section = formulario[section_key]
                if isinstance(section, list):
                    for idx, item in enumerate(section):
                        if todos_vacios(item):
                            continue  # Si todos los campos están vacíos, saltar la validación
                        if validar_parcial(item):
                            return True, f"Error: todos los campos en {section_key} {idx + 1} deben estar completos."
                        for subkey, value in item.items():
                            if subkey == "rut":
                                if not validar_rut(value):
                                    return True, f"Error: el RUT en {section_key} {idx + 1} es inválido."
                            elif not validar_campo(value, subkey):
                                return True, f"Error: el campo {subkey} en {section_key} {idx + 1} debe tener al menos 5 caracteres o ser F/M para género."

        # Si pasa todas las validaciones
        # Crear una instancia de `bsdinteraction` y verificar si el RUT ya existe
        self.bsd=bsdinteraction()
        exist_dni=self.bsd.existe_rut(formulario["DataEmpleado"]["rut"])
        if exist_dni:
            return True, "Rut ya existe en la base de datos."
        else:
            self.app_state.formulary_to_db(formulario)
            self.bsd.duplicate()
            return False, "Formulario válido."


    # VALIDA QUE LOS CAMPOS NO ESTEN VACIOS Y QUE EL RUT SEA VALIDO AL INGRESAR COMO DATO NUEVO
    def validation_pass_form(self,e):  
        is_invalid, message = self.campo_vacio()

        if is_invalid:
            alt = AlertDialog(title=Text(message))  # Cambiar `message` por `Text(message)`
            self.page.dialog = alt
            alt.open = True
            self.page.update()
            print("Incorrecto")
        else:
            alt = AlertDialog(title=Text(message))  # Cambiar `message` por `Text(message)`
            self.page.dialog = alt
            alt.open = True
            self.page.update()
            time.sleep(3)
            print("Correcto")
            self.clean_start(self.page)
    
    # LIMPIA LOS CAMPOS DEL FORMULARIO y redirige a la pagina de inicio
    def clean_start(self,page):
        self.build_forms()
        page.go("/inicio")

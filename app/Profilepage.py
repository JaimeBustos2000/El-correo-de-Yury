import flet as ft
from flet import *
from cdyury.bsdclass import bsdinteraction
from cdyury.appstatus import AppState
from datetime import datetime
import sqlite3
import time
import re



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

        self.select_genero = Dropdown(value = self.genero.value,label=self.genero.value,options=[
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
        
        nombre_actual = self.nombre.value
        apellido = self.apellido.value
        trabajador_rut = self.rut.value  # Rut del trabajador que ha iniciado sesión

        gnero_actual = self.select_genero.value
        telefono_actual = self.telefono.value
        
        # Actualizar datos principales del empleado en la base de datos
        if self.app_state.update_employee_data(trabajador_rut, nombre_actual, apellido, gnero_actual, telefono_actual):
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
            self.rut.value = data[0]
            self.nombre.value = data[1]
            self.apellido.value = data[2]
            self.genero.value = data[3]
            self.fecha.value = data[4]
            self.cargo.value = data[5]
            self.area.value = data[6]
            self.direccion.value = data[7]
            self.telefono.value = data[8]

            self.area.value = data[6]
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
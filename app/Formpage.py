import flet as ft
from flet import *
from cdyury.bsdclass import bsdinteraction
from cdyury.appstatus import AppState
from datetime import datetime
import time

# CLASE QUE CONTROLA EL FORMULARIO DE INGRESO DE DATOS
class FormPage:
    def __init__(self,page:Page,app_state):
        self.page=page
        self.app_state=app_state
        self.build_forms()
         
    def build_forms(self):
    #TEXTFIELDS PARA FORMULARIOS
        ##DATOS PERSONALES
        
        self.rut=TextField(value="",color="BLACK",width=200, hint_text="Rut con guion",label="RUT",label_style=TextStyle(color="BLACK"))
        self.nombres=TextField(value="",color="BLACK",width=200,label="Nombres",label_style=TextStyle(color="BLACK"))
        self.apellidos=TextField(value="",color="BLACK",width=200,label="Apellidos",label_style=TextStyle(color="BLACK"))
        self.sexo=Dropdown(label="Sexo",label_style=TextStyle(color="BLACK"),width=100,options=[dropdown.Option("M"),dropdown.Option("F")])
        self.calle=TextField(value="", width=200,label="Calle(sin numero)",label_style=TextStyle(color="BLACK"))
        self.complemento=TextField(value="", width=200,label="Complemento/numero casa",label_style=TextStyle(color="BLACK"))
        self.comuna=Dropdown(label="Comuna",label_style=TextStyle(color="BLACK"),width=200,options=[
            dropdown.Option("1",text="Santiago"),
            dropdown.Option("2",text="Providencia"),
            dropdown.Option("3",text="Las Condes"),
            dropdown.Option("4",text="La Florida"),
            dropdown.Option("5",text="Puente Alto"),
            dropdown.Option("6",text="Ñuñoa"),
            dropdown.Option("7",text="Maipú"),
            dropdown.Option("8",text="La Reina"),
            dropdown.Option("9",text="Vitacura"),
            dropdown.Option("10",text="Peñalolén")
            ])
        self.telefono=TextField(value="",color="BLACK",width=200,label="Telefono",label_style=TextStyle(color="BLACK"))
        ########################################################################################
        #DATOS LABORALES
        
        self.cargo=Dropdown(label="Cargo", label_style=TextStyle(color="BLACK"),width=200,options=[
            dropdown.Option("1",text="Gerente de RR.HH."),
            dropdown.Option("2",text="Personal de RR.HH."),
            dropdown.Option("3",text="Jefe de envios"),
            dropdown.Option("4",text="Repartidor")
            ])

        # Fecha ingreso
        fecha_actual=datetime.now()
        fecha_actual=fecha_actual.strftime("%d-%m-%Y")
        self.fecha=TextField(value=f"{fecha_actual}",color="BLACK",width=200, hint_text="Fecha de ingreso",text_size=15,text_align="CENTER",label="Fecha de ingreso",label_style=TextStyle(color="BLACK"))
        
        self.areaDepto=Dropdown(label="Departamento",label_style=TextStyle(color="BLACK"),width=200,options=[
            dropdown.Option(1,text="envios"),
            dropdown.Option(2,text="recursos humanos")
            ])

        #DATOS DE CONTACTO
        self.contacto1=TextField(value="",color="BLACK",width=200,label="Nombre contacto",label_style=TextStyle(color="BLACK"))
        self.fonocon1=TextField(value="",color="BLACK",width=200,label="Telefono contacto",label_style=TextStyle(color="BLACK"))
        self.relacion1=Dropdown(label="Relacion",label_style=TextStyle(color="BLACK"),width=200,options=[
            dropdown.Option("1",text="Padre"),
            dropdown.Option("2",text="Madre"),
            dropdown.Option("3",text="Hermano/a"),
            dropdown.Option("4",text="Hijo"),
            dropdown.Option("5",text="Hija"),
            dropdown.Option("6",text="Primo/a"),
            dropdown.Option("7",text="Conyuge"),
            dropdown.Option("8",text="Tio"),
            dropdown.Option("9",text="Tia"),
            ])
        
        #contacto2
        self.contacto2=TextField(value="",color="BLACK",width=200,label="Nombre contacto",label_style=TextStyle(color="BLACK"))
        self.relacion2=Dropdown(label="Relacion",label_style=TextStyle(color="BLACK"),width=200,options=[
            dropdown.Option("1",text="Padre"),
            dropdown.Option("2",text="Madre"),
            dropdown.Option("3",text="Hermano/a"),
            dropdown.Option("4",text="Hijo"),
            dropdown.Option("5",text="Hija"),
            dropdown.Option("6",text="Primo/a"),
            dropdown.Option("7",text="Conyuge"),
            dropdown.Option("8",text="Tio"),
            dropdown.Option("9",text="Tia"),
            ])
        self.fonocon2=TextField(value="",color="BLACK",width=200,label="Telefono contacto",label_style=TextStyle(color="BLACK"))

        #DATOS DE CARGA FAMILIAR
        #carga 1
        self.rut_carga1=TextField(value="",color="BLACK",width=200,label="Rut carga",label_style=TextStyle(color="BLACK"))
        self.nombre_carga1=TextField(value="",color="BLACK",width=200,label="Nombre carga",label_style=TextStyle(color="BLACK"))

        self.parentesco1=Dropdown(label="Relacion",label_style=TextStyle(color="BLACK"),width=200,options=[
            dropdown.Option("1",text="Padre"),
            dropdown.Option("2",text="Madre"),
            dropdown.Option("3",text="Hermano/a"),
            dropdown.Option("4",text="Hijo"),
            dropdown.Option("5",text="Hija"),
            dropdown.Option("6",text="Primo/a"),
            dropdown.Option("7",text="Conyuge"),
            dropdown.Option("8",text="Tio"),
            dropdown.Option("9",text="Tia"),
            ])

        #carga 2
        self.rut_carga2=TextField(value="",color="BLACK",width=200,label="Rut carga",label_style=TextStyle(color="BLACK"))
        self.nombre_carga2=TextField(value="",color="BLACK",width=200,label="Nombre carga",label_style=TextStyle(color="BLACK"))
        self.parentesco2=Dropdown(label="Relacion",label_style=TextStyle(color="BLACK"),width=200,options=[
            dropdown.Option("1",text="Padre"),
            dropdown.Option("2",text="Madre"),
            dropdown.Option("3",text="Hermano/a"),
            dropdown.Option("4",text="Hijo"),
            dropdown.Option("5",text="Hija"),
            dropdown.Option("6",text="Primo/a"),
            dropdown.Option("7",text="Conyuge"),
            dropdown.Option("8",text="Tio"),
            dropdown.Option("9",text="Tia"),
            ])
        
        # FORMULARIO DATOS PERSONALES
        dataP=Container(
                width=1366,
                height=150,
                bgcolor="#5D8BD1",
                content=Column(
                    spacing=1,
                    horizontal_alignment=CrossAxisAlignment.START,
                    controls=[
                        Row(controls=[
                            self.nombres,
                            self.apellidos,
                            self.rut,
                            self.sexo
                        ])
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
                bgcolor="#5D8BD1",
                content=Column(
                    spacing=1,
                    horizontal_alignment=CrossAxisAlignment.START,
                    controls=[
                        Row(controls=[
                            self.cargo,
                            self.fecha,
                            self.areaDepto
                        ])
                    ]
                )
            )
        # FORMULARIO CONTACTOS DE EMERGENCIA
        dataC=Container(
            width=1366,
            height=120,
            bgcolor="#5D8BD1",
            content=Column(
                spacing=4,
                horizontal_alignment=CrossAxisAlignment.START,
                controls=[
                    Row(controls=[
                        self.contacto1,
                        self.relacion1,
                        self.fonocon1
                    ]),
                    Row(controls=[
                        self.contacto2,
                        self.relacion2,
                        self.fonocon2 
                    ])
                ]
            )
        )
        # FORMULARIO CARGAS FAMILIARES
        dataF=Container(
            width=1366,
            height=120,
            bgcolor="#5D8BD1",
            content=Column(
                spacing=4,
                horizontal_alignment=CrossAxisAlignment.START,
                controls=[
                    Row(controls=[
                        self.rut_carga1,
                        self.nombre_carga1,
                        self.parentesco1
                    ]),
                    Row(controls=[
                        self.rut_carga2,
                        self.nombre_carga2,
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
                "rut": self.rut.value,
                "nombres": self.nombres.value,
                "apellidos": self.apellidos.value,
                "sexo": self.sexo.value,
                "cargo": self.cargo.value,
                "calle": self.calle.value,
                "complemento": self.complemento.value,
                "comuna": self.comuna.value,
                "areaDepto": self.areaDepto.value,
                "telefono": self.telefono.value
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
                    "parentesco": self.parentesco1.value
                },
                {
                    "rut": self.rut_carga2.value,
                    "nombre": self.nombre_carga2.value,
                    "parentesco": self.parentesco2.value
                }
            ]
        }
        return formulario
        
    # VALIDA QUE LOS CAMPOS NO ESTEN VACIOS Y QUE EL RUT SEA VALIDO CON EL BOTON
    def dni_comp(self,e):
        self.__bsd=bsdinteraction()
        rut=self.rut.value
        print("rut: ",rut)
        print("Longitud rut:",len(rut))
        dni_exist=self.__bsd.existe_rut(rut)
        print("Existe rut:",dni_exist)
        
        if len(rut) < 9 or len(rut) > 10  or rut == "" or (not "-" in rut):
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

    def validar_datos(self):
        formulario=self.get_data()
        # Validación de DataEmpleado
        data_empleado = formulario.get("DataEmpleado", {})

        for campo, valor in data_empleado.items():
            if campo == "sexo":
                if valor not in ['F', 'M']:
                    return False, "El campo sexo del empleado debe ser 'F' o 'M'."
                
            elif campo=="cargo":
                if valor not in ['1', '2', '3', '4']:
                    return False, "El campo cargo no corresponde a un valor valido."
                
            elif campo=="areaDepto":
                if valor not in ['1', '2']:
                    return False, "El campo areaDepto no corresponde a un valor valido."
                
            elif campo=="telefono":
                if len(valor.strip()) == 0 or not valor.isdigit():
                    return False, "El campo telefono del empleado debe ser un número válido."
                elif len(valor.strip()) not in [9, 10]:
                    return False, "El campo telefono del empleado debe tener 9 o 10 dígitos."
                
            elif campo=="comuna":
                if valor not in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']:
                    return False, "El campo comuna del empleado no corresponde a un valor valido."
                
            elif campo=="complemento":
                if valor==None:
                    return False, f"El campo {campo} personal no debe estar vacío."
    
                if len(valor.strip()) == 0:
                    return False, f"El campo {campo} personal no debe estar vacío."
                
            elif campo=="nombres" or campo=="apellidos":
                if valor.isdigit():
                    return False, f"El campo {campo} personal no debe contener números."
                
            else:
                if valor==None or valor=="":
                    return False, f"El campo {campo} personal no debe estar vacío."
                
                if len(valor.strip()) == 0:
                    return False, f"El campo {campo} personal no debe estar vacío."
                
                if campo != "nombres" and len(valor.strip()) <= 3:
                    return False, f"El campo {campo} debe tener longitud mayor a 3 caracteres."

        # Validación de formato de Rut en DataEmpleado
        rut = data_empleado.get("rut", "")
        if not (len(rut) == 9 or len(rut) == 10) or not rut.replace("-", "").isdigit():
            return False, "El Rut en DataEmpleado debe tener formato válido (9 o 10 caracteres con guion)."

        # Validación de ContactosEmp
        contactos = formulario.get("ContactosEmp", [])
        for contacto in contactos:
            if any((valor is not None and len(valor.strip()) > 0) for valor in contacto.values()) and any((valor is None or len(valor.strip()) == 0) for valor in contacto.values()):
                return False, "Los campos en ContactosEmp deben estar completamente completados o completamente vacíos."
            
            if contacto["telefono"] != "":
                telefono = contacto["telefono"]
                if not isinstance(telefono, str) or not telefono.isdigit() or len(telefono) not in [9, 10]:
                    return False, "El campo telefono debe ser un número válido de 9 o 10 dígitos."
                
            if contacto["nombre"] != "":
                nombre = contacto["nombre"]
                if not isinstance(nombre, str) or nombre.isdigit():
                    return False, "El campo nombre en ContactosEmp no debe contener números."
            

        # Validación de CargaEmp
        cargas = formulario.get("CargaEmp", [])
        print("Cargas       as",cargas)

        for carga in cargas:
            # Verificar si todos los campos están vacíos o completos
            if any(valor and len(valor.strip()) > 0 for valor in carga.values()):
                if any(valor is None or len(valor.strip()) == 0 for valor in carga.values()):
                    return False, "Los campos en CargaEmp deben estar completamente completados o completamente vacíos."
        
                # Validar el campo rut
                rut = carga["rut"]
                if not (isinstance(rut, str) and 
                        rut.replace("-", "").isdigit() and 
                        len(rut) in [9, 10] and 
                        rut[-2] == "-"):
                    return False, "El campo rut en CargaEmp debe tener formato válido (9 o 10 caracteres con guion en el penúltimo carácter)."
        
                # Validar el campo nombre
                nombre = carga["nombre"]
                if any(char.isdigit() for char in nombre):
                    return False, "El campo nombre en CargaEmp no debe contener números."
            
        return True, "Todos los datos son válidos."


    # VALIDA QUE LOS CAMPOS NO ESTEN VACIOS Y QUE EL RUT SEA VALIDO AL INGRESAR COMO DATO NUEVO
    def validation_pass_form(self,e):  
        is_invalid, message = self.validar_datos()
        print(is_invalid, message)
        
        if not is_invalid:
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
            self.form=self.get_data()
            self.app_state.formulary_to_db(self.form)

            self.clean_start(self.page)
    
    # LIMPIA LOS CAMPOS DEL FORMULARIO y redirige a la pagina de inicio
    def clean_start(self,page):
        self.build_forms()
        page.go("/inicio")

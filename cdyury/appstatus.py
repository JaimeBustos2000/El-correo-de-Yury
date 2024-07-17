from cdyury.bsdclass import bsdinteraction
import sqlite3
from sqlite3 import Error


# Clase que guarda el estado de la aplicación y maneja datos obtenidos dentro de la app
class AppState:
    def __init__(self):
        self.username = ""
        self.data_array = ""
        self.rol = 0
        self.bsd = bsdinteraction()
        self.filters=False
        self.conex=self.bsd.connection()

    def set_username(self, username):
        self.username = username
    
    def get_username(self):
        return self.username

    def set_data(self, data):
        self.data_array = data
        
    def get_data(self):
        return self.data_array

    def formulary_to_db(self, form):
        self.form = form
        interact = self.bsd
        interact.data_to_db(form)
    
    def get_rol(self):
        self.rol = self.bsd.obtener_rol(self.get_username())
        return self.rol
    
    def set_rol(self, rol):
        self.rol = rol
    
    def retornar_rol(self):
        nombre_usuario=self.get_username()
        print("Nombre de usuario: ",nombre_usuario)
        self.rol = self.bsd.obtener_rol(nombre_usuario)
        print(self.rol)
        return self.rol
    
    def set_filters(self, filters):
        self.filters = filters
        
    def get_filters_on(self):
        print("filtro en appstate", self.filters)
        return self.filters
    
    # Función que obtiene las cargas familiares y contactos de un trabajador en específico y los carga en listas
    def obtener_cargas_contactos(self, rut_trabajador):
        data=self.bsd.obtener_cargas_contactos(rut_trabajador)
        cargas_familiares = data[0]
        contactos_emergencia = data[1]
        return cargas_familiares, contactos_emergencia
    
    
    # Aqui funciones no implementadas para ser tratadas en oracle pero con la logica necesaria para ser implementadas
    
    def eliminar_carga_familiar(self,nombre_carga, rut_trabajador):
        interact = self.bsd
        interact.eliminar_carga_familiar(nombre_carga, rut_trabajador)
        
    def eliminar_contacto_emergencia(self,nombre_contacto, rut_trabajador):
        interact = self.bsd
        interact.eliminar_contacto(nombre_contacto, rut_trabajador)
    
    # Función que obtiene los datos de un trabajador en específico y los actualiza
    def update_employee_data(self, rut, nombre, apellido):
        update=self.bsd.update_employee_data(rut,nombre, apellido)
        return update

    # Función que obtiene las cargas familiares nuevas de un trabajador en específico y los añade
    def add_carga_familiar(self, rut, nombre, genero, parentesco, trabajador_rut):
        try:
            conn = sqlite3.connect("correosyury.db")
            cur = conn.cursor()
            cur.execute("INSERT INTO CargaEmp (rut, nombre, genero, parentesco_id, trabajador_rut) VALUES (?, ?, ?, ?, ?)",
                        (rut, nombre, genero, parentesco, trabajador_rut))
            conn.commit()
            conn.close()
            print("Carga familiar agregada correctamente")
        except Exception as e:
            print(f"Error al agregar carga familiar: {str(e)}")

    # Función que obtiene los contactos de emergencia nuevos de un trabajador en específico y los añade
    """def add_contacto_emergencia(self, nombre, relacion, telefono, trabajador_rut):
        
        try:
            con=self.bsd.obtener_conexion()
            
            cur = con.cursor()
            cur.execute("INSERT INTO ContactosEmp (nombre, relacion_id, telefono, trabajador_rut) VALUES (?, ?, ?, ?)",
                        (nombre, relacion, telefono, trabajador_rut))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Error al agregar contacto de emergencia: {str(e)}")"""


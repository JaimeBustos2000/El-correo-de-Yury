from bsdclass import bsdinteraction
import sqlite3
from sqlite3 import Error

class AppState:
    def __init__(self):
        self.username = ""
        self.data_array = ""
        self.bsd = bsdinteraction()

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

    def update_employee_data(self, rut, genero, nombre, direccion, telefono):

        print(genero)
            
        try:
            conn = sqlite3.connect("correosyury.db")
            cur = conn.cursor()
            cur.execute("UPDATE Trabajadores SET sexo=?, nombre=?, direccion=?, telefono=? WHERE rut=?",
                        (genero, nombre, direccion, telefono, rut))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error al actualizar datos del trabajador: {str(e)}")
            return False

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

    def add_contacto_emergencia(self, nombre, relacion, telefono, trabajador_rut):
        
        try:
            conn = sqlite3.connect("correosyury.db")
            cur = conn.cursor()
            cur.execute("INSERT INTO ContactosEmp (nombre, relacion_id, telefono, trabajador_rut) VALUES (?, ?, ?, ?)",
                        (nombre, relacion, telefono, trabajador_rut))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Error al agregar contacto de emergencia: {str(e)}")

    def obtener_cargas_contactos(self, rut_trabajador):
        try:
            conn = sqlite3.connect("correosyury.db")
            cur = conn.cursor()
            cur.execute("SELECT rut, nombre, genero, parentesco_id FROM CargaEmp WHERE trabajador_rut=?", (rut_trabajador,))
            cargas_familiares = cur.fetchall()

            cur.execute("SELECT nombre, relacion_id, telefono FROM ContactosEmp WHERE trabajador_rut=?", (rut_trabajador,))
            contactos_emergencia = cur.fetchall()

            conn.close()

            return cargas_familiares, contactos_emergencia
        except Exception as e:
            print(f"Error al obtener cargas y contactos de emergencia: {str(e)}")
            return [], []
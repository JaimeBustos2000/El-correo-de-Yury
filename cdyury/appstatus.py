from cdyury.bsdclass import bsdinteraction
import sqlite3
from sqlite3 import Error


# Clase que guarda el estado de la aplicación y maneja datos obtenidos dentro de la app
class AppState:
    def __init__(self):
        self.username = ""
        self.data_array = ""
        self.bsd = bsdinteraction()
        self.conex=self.bsd.connection()

    def set_username(self, username):
        self.username = username
    
    def get_username(self):
        print(self.username)
        return self.username

    def set_data(self, data):
        self.data_array = data
        
    def get_data(self):
        return self.data_array

    def formulary_to_db(self, form):
        self.form = form
        interact = self.bsd
        interact.data_to_db(form)
        
    # Función que obtiene las cargas familiares y contactos de un trabajador en específico y los carga en listas
    def obtener_cargas_contactos(self, rut_trabajador):
        print(rut_trabajador)
        
        cur = self.conex.cursor()
        try:
            cur.execute("""
                SELECT cf.nombre_familiar, p.relacion
                FROM carga_familiar cf
                JOIN parentesco p ON cf.parentesco_id = p.id_parentesco
                JOIN empleado e ON cf.rut_emp = e.rut
                WHERE cf.rut_emp = :1
            """, (rut_trabajador,))
            cargas_familiares = cur.fetchall()
            
            cur.execute("""
                SELECT 
                    co.nombre_contacto,
                    pa.relacion,
                    t.num_telefono
                FROM contacto co
                JOIN telefono t ON co.telefono_id = t.id_telefono
                JOIN parentesco pa ON co.parentesco_id = pa.id_parentesco
                WHERE co.rut_emp = :1
            """, (rut_trabajador,))
            
            contactos_emergencia = cur.fetchall()
            
            print(cargas_familiares, contactos_emergencia)
            return cargas_familiares, contactos_emergencia
        except Exception as e:
            print(f"Error al obtener cargas y contactos de emergencia: {str(e)}")
            return [], []
        finally:
            cur.close()
    
    
    # Aqui funciones no implementadas para ser tratadas en oracle pero con la logica necesaria para ser implementadas
    
    # Función que obtiene los datos de un trabajador en específico y los actualiza
    def update_employee_data(self, rut, genero, nombre, direccion, telefono):
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


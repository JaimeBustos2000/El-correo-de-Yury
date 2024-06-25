from UserDatabase import UserDatabase #archivo y clase para verificar el login del usuario
from UserMana import PasswordManager #archivo y clase para hashear y descifrar contraseñas provenientes de la bsd
import sqlite3
import flet as ft
from flet import *
import random


#CLASE PRINCIPAL PARA INTERACTUAR CON LA BASE DE DATOS/PRELIMINAR PARA SEPARAR LOS REQUERIMIENTOS
class bsdinteraction():
    def __init__(self):
        self.name:str
        self.role:str #Despues a añadir el rol
        self.__database="correosyury.db" #definir la base de datos a usar
    
    #Verificacion de si el usuario es valido para crear una cuenta en el sistema
    def check_user(self, rut):

        #contraseña generica que sera hasheada como metodo privado
        self.__hashpass="53492840Aa"
        #Verificacion
        if rut==None or len(rut) < 9 or len(rut) > 11:
            print("Rut no coincide")
            return False
        else:
            # Conectar a la base de datos principal
            conn = sqlite3.connect(self.__database)
            cursor = conn.cursor()

            # Verificar si el rut está en la tabla trabajadores
            cursor.execute("SELECT * FROM trabajadores WHERE rut=?", (rut,))
            trabajadores_result = cursor.fetchone()

            # Verificar si el rut está en la tabla usuarios en la otra base de datos
            connect = sqlite3.connect("cdyusr.db")
            cursor_usr = connect.cursor()
            cursor_usr.execute("SELECT * FROM usuarios WHERE Trabajador_id=?", (rut,))
            usuarios_result = cursor_usr.fetchone()

            print(trabajadores_result,usuarios_result)

            # Verificar los resultados y devolver el resultado apropiado
            if  trabajadores_result is None or (trabajadores_result is None and usuarios_result is None):
                return False
            else:
                cursor_usr.execute("SELECT * FROM usuarios WHERE Trabajador_id=?",(rut,))
                resultado=cursor_usr.fetchone()
                
                if resultado:
                    print("Rut ya posee usuario")
                    return True
                else:
                    nombre_apellido = trabajadores_result[1]  # Suponiendo que el nombre completo está en la segunda columna
                    nombre, apellido = nombre_apellido.split(' ', 1)
                    username = str(nombre + apellido[:2]).lower()
                    
                    while True:
                        cursor_usr.execute("SELECT Trabajador_id FROM usuarios WHERE username=?",(username,))
                        result=cursor_usr.fetchone()
                        
                        if result:
                            random_usrtag=str(random.randint(1,99))
                            username = username + random_usrtag
                            break
                        else:
                            break

                    #creamos la contraseña hasheada
                    self.hash=PasswordManager().hash_password(self.__hashpass)
                    # Insertar el nuevo usuario en la base de datos usuarios
                    cursor_usr.execute(
                        "INSERT OR IGNORE INTO usuarios (Trabajador_id, username, password_hash) VALUES (?, ?, ?)",
                        (rut, username, PasswordManager().hash_password(self.__hashpass)) # Contraseña por defecto generica
                    )
                    connect.commit()
                    connect.close()

                    conn.close()
                    return True

    # Método para corroborar el inicio de sesion
    def login(self,user,password):
        self.__database="correosyury.db"
        self.__user=user
        self.__password=password
        
        self.permit=False
        self.validate=False
        
        user=UserDatabase()
   
        # Conectar a la base de datos de usuarios
        return user.authenticate_user(self.__user,self.__password)

    # Método para duplicar la base de datos de trabajadores a la base de datos de usuarios / test
    def duplicate(self):
        self.__database="correosyury.db"
        
        conexion_origen = sqlite3.connect(self.__database)

        conexion_destino = sqlite3.connect("cdyusr.db")
        
        cursor_origen = conexion_origen.cursor()
        cursor_destino = conexion_destino.cursor()
       
        query="DROP TABLE IF EXISTS trabajadores"
        cursor_destino.execute(query)
        query="CREATE TABLE IF NOT EXISTS trabajadores  (rut TEXT PRIMARY KEY, nombre TEXT NOT NULL, sexo TEXT NOT NULL, direccion TEXT NOT NULL, telefono TEXT, cargo TEXT NOT NULL, fecha_ingreso TEXT NOT NULL, area_y_departamento TEXT NOT NULL)"
        cursor_destino.execute(query)
     
        cursor_origen.execute("SELECT * FROM trabajadores")
        filas = cursor_origen.fetchall()
        
        for fila in filas:
            cursor_destino.execute("INSERT OR IGNORE INTO trabajadores VALUES (?,?,?,?,?,?,?,?)", fila)
            
        conexion_destino.commit()
        conexion_origen.close()
        conexion_destino.close()
        
    #Obtiene todos los datos del usuario para el perfil y creacion de usuarios
    def fetch_data(self,name):
        self.__database="cdyusr.db"
        self.__databaseprin="correosyury.db"
        con = sqlite3.connect(self.__database)
        cur = con.cursor()
        
        try:
            cur.execute("SELECT Trabajador_id FROM usuarios WHERE username=? ",(name,))
            rut=cur.fetchone()
            trabajador_id=rut[0]
            print(trabajador_id)
            con.close()    
        except Exception as e:
            print(f"ERROR BASE DE DATOS: {e}")
            return None
        
        
        try:
            connect=sqlite3.connect(self.__databaseprin)
            cursor=connect.cursor()
            cursor.execute("SELECT * FROM trabajadores WHERE rut=?",(trabajador_id,))
            datos=cursor.fetchall()
            print(datos)
            connect.close()
            return datos
            
        except Exception as e:
            print(f"ERROR BASE DE DATOS: {e}")
            return None            
        
    #Actualiza los datos del usuario
    def data_to_db(self, array):
        self.__database = "correosyury.db"
        
        conn = sqlite3.connect(self.__database)
        cursor = conn.cursor()

        # Crear las tablas si no existen /// OMITIR DADO QUE ESTAN CREADAS SOLO CONSULTAS
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Departamento (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT UNIQUE NOT NULL
        )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Cargos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT UNIQUE NOT NULL
        )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Parentescos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT UNIQUE NOT NULL
        )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS ContactosEmp (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            relacion_id INTEGER NOT NULL,
            telefono TEXT NOT NULL,
            trabajador_rut TEXT NOT NULL,
            FOREIGN KEY (relacion_id) REFERENCES Parentescos(id),
            FOREIGN KEY (trabajador_rut) REFERENCES Trabajadores(rut)
        )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS CargaEmp (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rut TEXT NOT NULL,
            nombre TEXT NOT NULL,
            genero TEXT NOT NULL,
            parentesco_id INTEGER NOT NULL,
            trabajador_rut TEXT NOT NULL,
            FOREIGN KEY (parentesco_id) REFERENCES Parentescos(id),
            FOREIGN KEY (trabajador_rut) REFERENCES Trabajadores(rut)
        )
        ''')


        # Insertar datos en las tablas Departamentos, Cargos y Parentescos
        departamentos = ['envios', 'recursos humanos']
        cargos = ["Jefe de envios", "Gerente de RR.HH.", "Personal de RR.HH", "Repartidor"]
        parentescos = ['Padre', 'Madre', 'Hijo/a', 'Hermano/a', 'Primo/a', 'Conyuge']
        
        # Insertar departamentos
        for depto in departamentos:
            try:
                cursor.execute('''
                INSERT OR IGNORE INTO Departamento (nombre)
                VALUES (?)
                ''', (depto,))
                print(f"Departamento '{depto}' insertado o ya existente.")
            except sqlite3.Error as e:
                print(f"Error al insertar departamento '{depto}': {e}")
        
        # Insertar cargos
        for cargo in cargos:
            try:
                cursor.execute('''
                INSERT OR IGNORE INTO Cargos (nombre)
                VALUES (?)
                ''', (cargo,))
                print(f"Cargo '{cargo}' insertado o ya existente.")
            except sqlite3.Error as e:
                print(f"Error al insertar cargo '{cargo}': {e}")
        
        # Insertar parentescos
        for parentesco in parentescos:
            try:
                cursor.execute('''
                INSERT OR IGNORE INTO Parentescos (nombre)
                VALUES (?)
                ''', (parentesco,))
                print(f"Parentesco '{parentesco}' insertado o ya existente.")
            except sqlite3.Error as e:
                print(f"Error al insertar parentesco '{parentesco}': {e}")
        
        # Commit the inserts for departamentos, cargos, and parentescos
        conn.commit()
        
        # Concatenar nombres y apellidos // OMITIR DADO QUE DEBEN ESTAR SEPARADO EL NOMBRE DEL APELLIDO
        data_empleado = array["DataEmpleado"]
        nombre_completo = f"{data_empleado['nombres']} {data_empleado['apellidos']}"
        
        
        # Insertar datos en las tablas Trabajadores, ContactosEmp y CargaEmp // SEGUN ORACLE
        """
        
        """
        try:
            # Insertar datos en la tabla Trabajadores
            cursor.execute('''
            INSERT INTO trabajadores (rut, nombre, sexo, direccion, telefono, cargo, fecha_ingreso, area_y_departamento)
            VALUES (?, ?, ?, ?, ?, (SELECT id FROM Cargos WHERE nombre = ?), ?, (SELECT id FROM Departamento WHERE nombre = ?))
            ''', (data_empleado['rut'], nombre_completo, data_empleado['sexo'], data_empleado['direccion'], data_empleado['telefono'], data_empleado['cargo'], data_empleado['fecha'], data_empleado['areaDepto']))

            # Insertar datos en la tabla ContactosEmp
            contactos_emp = array["ContactosEmp"]
            for contacto in contactos_emp:
                if contacto["nombre"]:  # Sólo insertar si el nombre no está vacío
                    relacion_id = None
                    if contacto["relacion"]:
                        cursor.execute('SELECT id FROM Parentescos WHERE nombre = ?', (contacto["relacion"],))
                        row = cursor.fetchone()
                        if row:
                            relacion_id = row[0]

                    cursor.execute('''
                    INSERT INTO ContactosEmp (nombre, relacion_id, telefono, trabajador_rut)
                    VALUES (?, ?, ?, ?)
                    ''', (contacto["nombre"], relacion_id, contacto["telefono"], data_empleado['rut']))

            # Insertar datos en la tabla CargaEmp
            cargas_emp = array["CargaEmp"]
            for carga in cargas_emp:
                if carga["rut"]:  # Sólo insertar si el rut no está vacío
                    parentesco_id = None
                    if carga["parentesco"]:
                        cursor.execute('SELECT id FROM Parentescos WHERE nombre = ?', (carga["parentesco"],))
                        row = cursor.fetchone()
                        if row:
                            parentesco_id = row[0]

                    cursor.execute('''
                    INSERT OR IGNORE INTO CargaEmp (rut, nombre, genero, parentesco_id, trabajador_rut)
                    VALUES (?, ?, ?, ?, ?)
                    ''', (carga["rut"], carga["nombre"], carga["genero"], parentesco_id, data_empleado['rut']))

            message = "Datos ingresados correctamente"
        except sqlite3.Error as e:
            print("Error:", e)
            message = str(e)
            return message

        self.duplicate()
        # Confirmar las operaciones
        conn.commit()

        # Cerrar la conexión
        conn.close()

        return message    
    
    
    def existe_rut(self,rut):
        print(rut)
        self.__database="correosyury.db"
        conn = sqlite3.connect(self.__database)
        cursor = conn.cursor()
        cursor.execute("SELECT rut FROM trabajadores WHERE rut = ?", (rut,))
        rut = cursor.fetchall()
        conn.close()
        
        if rut:
            return True
        else:
            return False
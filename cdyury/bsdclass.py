from Management.UserDatabase import UserDatabase #archivo y clase para verificar el login del usuario
from Management.UserMana import PasswordManager #archivo y clase para hashear y descifrar contraseñas provenientes de la bsd
import sqlite3
import flet as ft
from flet import *
import cx_Oracle
import random


#CLASE PRINCIPAL PARA INTERACTUAR CON LA BASE DE DATOS/PRELIMINAR PARA SEPARAR LOS REQUERIMIENTOS
class bsdinteraction():
    def __init__(self):
        self.name:str
        self.role:str #Despues a añadir el rol
        self.__database="correosyury.db"
        self.__hostname = 'localhost'  # Or the hostname/IP of your Oracle server
        self.__port = 1521             # Default port for Oracle XE
        self.__service_name = 'XE'     # Service name for Oracle XE
        self.__username = 'app_user'   # Oracle username
        self.__passw = '1234567Aa'     # Oracle user password
        self.conn = None
        self.connection()


    def connection(self):
        # Construct the DSN (Data Source Name)
        dsn = cx_Oracle.makedsn(self.__hostname, self.__port, service_name=self.__service_name)

        try:
            # Establish the connection
            self.conn = cx_Oracle.connect(user=self.__username, password=self.__passw, dsn=dsn)
            if self.conn:
                print("Conexion exitosa")
        except cx_Oracle.DatabaseError as e:
            print(f"Conexion fallida: {e}")
            self.conn = None
        return self.conn

    def disconnect(self):
        if self.conn:
            self.conn.close()
            print("Conexion cerrada")
        else:
            print("No hay conexion para cerrar")
    
    #Verificacion de si el usuario es valido para crear una cuenta en el sistema
    def check_user(self, rut):
        # Contraseña genérica que será hasheada
        self.__hashpass = "53492840Aa"

        # Verificación del RUT
        if rut is None or len(rut) < 9 or len(rut) > 11:
            print("Rut no coincide")
            return False
        
        # Crear cursor para ejecutar consultas
        cursor = self.conn.cursor()

        try:
            # Verificar si el rut está en la tabla trabajadores
            cursor.execute("SELECT * FROM ficha WHERE rut = :rut", {'rut': rut})
            trabajadores_result = cursor.fetchone()

            # Verificar si el rut está en la tabla usuarios
            cursor.execute("SELECT * FROM usuarios WHERE trabajador_rut = :rut", {'rut': rut})
            usuarios_result = cursor.fetchone()

            print(trabajadores_result)
            print(usuarios_result)

            # Si no se encuentra en trabajadores o en usuarios, retornar False
            if len(trabajadores_result) == 0 or (trabajadores_result is None and usuarios_result is None):
                return False

            # Si ya existe en usuarios, imprimir mensaje y retornar True
            if usuarios_result:
                print("Rut ya posee usuario")
                return False

            
            # Si no existe en usuarios, crear nuevo usuario
            nombre=trabajadores_result[2]
            apellido=trabajadores_result[3]
            username = str(nombre + apellido[:2]).lower()

            while True:
                cursor.execute("SELECT trabajador_rut FROM usuarios WHERE username = :username", {'username': username})
                result = cursor.fetchone()

                if result:
                    random_usrtag = str(random.randint(1, 99))
                    username = username + random_usrtag
                    break
                else:
                    break

            # Crear hash de la contraseña
            UserDatabase().create_user(rut, username, self.__hashpass)

            # Obtener el siguiente ID para el nuevo usuario
            cursor.execute("SELECT MAX(id) FROM usuarios")
            max_id = cursor.fetchone()[0]
            if max_id is None:
                max_id = 0
            new_id = max_id + 1

            # Insertar el nuevo usuario en la tabla usuarios


            self.conn.commit()
            print("Usuario creado exitosamente")
            return True
        finally:
            cursor.close()

    # Método para corroborar el inicio de sesion
    def login(self, user, password):
        is_valid=UserDatabase().authenticate_user(user, password)
        print(is_valid)
        if is_valid:
            return True
        else:
            return False

    """# Método para duplicar la tabla empleados a ficha (relacionada a usuarios) / test
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
        conexion_destino.close()"""
        
    #Obtiene todos los datos del usuario para el perfil y creacion de usuarios
    def fetch_data(self,name):

        cur=self.conn.cursor()

        try:
            sql = "SELECT trabajador_rut FROM usuarios WHERE username = :username"
            cur.execute(sql, {'username': name})
            rut=cur.fetchone()
            trabajador_id=rut[0]
            print(trabajador_id)   
        except Exception as e:
            print(f"ERROR BASE DE DATOS: {e}")
            return None
        
        
        cur=self.conn.cursor()

        try:
            # Ejecutar consulta SQL para obtener datos del empleado por su ID (trabajador_id)
            sql = """
                SELECT
                    e.rut,
                    e.nombres,
                    e.apellidos,
                    CASE e.sexo
                        WHEN 'M' THEN 'MASCULINO'
                        WHEN 'F' THEN 'FEMENINO'
                        ELSE 'OTRO'
                    END AS sexo,
                    TO_CHAR( e.fecha_ing, 'DD-MM-YYYY') AS fecha_formateada,
                    c.cargo_desc,
                    d.depto_desc,
                    dir.calle || ' ' || dir.complemento || ',' || com.nombre_co || ',' || reg.nombre_reg AS Direccion,
                    t.num_telefono
                FROM
                    empleado e
                JOIN
                    cargo c ON e.cargo_id = c.id_cargo
                JOIN
                    departamento d ON e.departamento_id = d.id_depto
                JOIN
                    direccion dir ON e.direccion_id = dir.id_direccion
                JOIN
                    comuna com ON dir.comuna_id = com.id_comuna
                JOIN
                    region reg ON com.region_id = reg.id_region
                JOIN
                    telefono t ON e.telefono_id = t.id_telefono
                WHERE
                    e.rut = :rut
            """
            cur.execute(sql, {'rut': trabajador_id})

            # Obtener todos los datos resultantes
            datos = cur.fetchall()
            print(datos)
            return datos
        finally:
            cur.close()      
        
    #Actualiza los datos del usuario
    def data_to_db(self, array):
        print("data to db:", array)
    
    #Obtiene los datos de los trabajadores para mostrar en la tabla
    def consultar_trabajadores(self, filtro):
        if filtro=="":
            filtro = "1=1"
        
        mydt = ft.DataTable(
            bgcolor="WHITE",
            heading_row_color=ft.colors.BLACK87,
            border=ft.border.all(2, "BLACK"),
            border_radius=10,
            vertical_lines=ft.border.BorderSide(1, "BLACK"),
            horizontal_lines=ft.border.BorderSide(2, ""),
            columns=[
                ft.DataColumn(ft.Text(value="#",color="WHITE")),
                ft.DataColumn(ft.Text(value="Rut",color="WHITE")),
                ft.DataColumn(ft.Text(value="Nombre",color="WHITE")),
                ft.DataColumn(ft.Text(value="Sexo",color="WHITE")),
                ft.DataColumn(ft.Text(value="Cargo",color="WHITE")),
                ft.DataColumn(ft.Text(value="Fecha-ingreso",color="WHITE")),
                ft.DataColumn(ft.Text(value="Area y depto.",color="WHITE"))
            ],
            rows=[]
        )

        try:
            cur=self.conn.cursor()
                # Consulta SQL para obtener trabajadores con filtro
            query = f"""
                    SELECT e.rut, 
                        e.nombres ||' '|| e.apellidos AS nombre_completo,
                    CASE e.sexo
                        WHEN 'M' THEN 'MASCULINO'
                        WHEN 'F' THEN 'FEMENINO'
                        ELSE 'OTRO'
                    END AS sexo,
                        e.direccion_id, 
                        t.num_telefono, 
                        c.cargo_desc,
                    TO_CHAR(e.fecha_ing, 'YYYY-MM-DD') AS fecha_ingreso,
                     d.depto_desc AS area_y_departamento
                    FROM empleado e
                    JOIN telefono t ON e.telefono_id = t.id_telefono
                    JOIN cargo c ON e.cargo_id = c.id_cargo
                    JOIN direccion di ON di.id_direccion = e.direccion_id
                    JOIN departamento d ON e.departamento_id = d.id_depto
                    WHERE {filtro}
                """
            print(query)
            cur.execute(query)
            
            consulta=cur.fetchall()
                # Procesar los resultados
            for i, row in enumerate(consulta,1):
                mydt.rows.append(
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(str(i), color="BLACK")),
                        ft.DataCell(ft.Text(value=row[0], color="BLACK")),  # Rut
                        ft.DataCell(ft.Text(value=row[1], color="BLACK")),  # Nombre completo
                        ft.DataCell(ft.Text(value=row[2], color="BLACK")),  # Sexo
                        ft.DataCell(ft.Text(value=row[5], color="BLACK")),  # Cargo
                        ft.DataCell(ft.Text(value=row[6], color="BLACK")),  # Fecha de ingreso
                        ft.DataCell(ft.Text(value=row[7], color="BLACK"))   # Área y departamento
                    ])
                )

        except cx_Oracle.Error as error:
            print(f"Error al ejecutar la consulta: {error}")

        return mydt
    
    def existe_rut(self,rut):
        cur=self.conn.cursor()
        try:
            sql = "SELECT * FROM empleado WHERE rut = :rut"
            cur.execute(sql, {'rut': rut})
            trabajadores = cur.fetchall()
            print(trabajadores)
            if trabajadores:
                return True
            else:
                return False
        finally:
            cur.close()

from Management.UserDatabase import UserDatabase #archivo y clase para verificar el login del usuario
from Management.UserMana import PasswordManager #archivo y clase para hashear y descifrar contraseñas provenientes de la bsd
from dotenv import load_dotenv
import flet as ft
from flet import *
import os
import cx_Oracle
import random


#CLASE PRINCIPAL PARA INTERACTUAR CON LA BASE DE DATOS/PRELIMINAR PARA SEPARAR LOS REQUERIMIENTOS
class bsdinteraction():
    def __init__(self):
        load_dotenv()
        self.conn = None
        self.connection()

    def connection(self):
        self.__hostname = str(os.getenv("Hostname"))
        self.__port = int(os.getenv("Port"))
        self.__service_name = str(os.getenv("Service"))
        self.__username = str(os.getenv("db_Username"))
        self.__passw= str(os.getenv("Password"))
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
            e_result= cursor.var(cx_Oracle.NUMBER)
            cursor.callproc("EXISTE_EMP", [rut, e_result])
            trabajadores_result  = int(e_result.getvalue())

            # Verificar si el rut está en la tabla usuarios
            v_result= cursor.var(cx_Oracle.NUMBER)
            cursor.callproc("USER_EXISTS", [rut, v_result])
            usuarios_result = int(v_result.getvalue())

            # 1 = Existe, 0 = No existe
            print(trabajadores_result)
            print(usuarios_result)

            # Si no se encuentra en empleado retornar False
            if trabajadores_result==0:
                return False

            # Si ya existe en usuarios, imprimir mensaje y retornar 
            if trabajadores_result==1 and usuarios_result==1:
                print("Rut ya posee usuario")
                return False

            # Si no existe en usuarios, crear nuevo usuario
            u_result= cursor.var(cx_Oracle.STRING)
            cursor.callproc("create_username", [rut, u_result])
            username = u_result.getvalue()
            print(username)
            
            cargo=cursor.var(cx_Oracle.NUMBER)
            cursor.callproc("get_cargo", [rut, cargo])
            cargo_id = int(cargo.getvalue())

            # Crear hash de la contraseña # Insertar el nuevo usuario en la tabla usuarios
            UserDatabase().create_user(cargo_id,rut, username, self.__hashpass)
            
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
        
    #Obtiene todos los datos del usuario para el perfil y creacion de usuarios
    def fetch_data(self,name):
        cur=self.conn.cursor()
        
        try:
            sql = "SELECT trabajador_rut FROM usuarios WHERE usuario = :username"
            cur.execute(sql, {'username': name})
            rut=cur.fetchone()
            trabajador_id=rut[0]
            print("rut trabajador",trabajador_id)   
        except Exception as e:
            print(f"ERROR BASE DE DATOS: {e}")
            return None
        
        
        cur=self.conn.cursor()

        try:
            # Ejecutar consulta SQL para obtener datos del empleado por su ID (trabajador_id)
            result = cur.var(cx_Oracle.CURSOR)
            cur.callproc("obtener_empleado", [trabajador_id,result])
            
            resultado = result.getvalue()
            print("El array es: ",resultado)
            # Obtener todos los datos resultantes

            return resultado
        finally:
            cur.close()      
        
    #Actualiza los datos del usuario
    def data_to_db(self, array):
        print("data to db:", array)
        data_empleado = array.get('DataEmpleado')
        
        if data_empleado:
            rut = data_empleado.get('rut')
            nombres = data_empleado.get('nombres')
            apellidos = data_empleado.get('apellidos')
            sexo = data_empleado.get('sexo')
            cargo = int(data_empleado.get('cargo'))
            calle = data_empleado.get('calle')
            complemento = data_empleado.get('complemento')
            comuna = int(data_empleado.get('comuna'))
            areaDepto = int(data_empleado.get('areaDepto'))
            telefono = data_empleado.get('telefono')
            fecha = data_empleado.get('fecha')
        
        try:
            con=self.connection()
            cursor=con.cursor()
            id_direccion = cursor.var(cx_Oracle.NUMBER)
            cursor.callproc("INSERTAR_DIRECCION", [id_direccion,calle,complemento,comuna])
            direccion_id = id_direccion.getvalue()

        finally:
            cursor.close()
        
        try:
            con=self.connection()
            cursor=con.cursor()
            id_tel=cursor.var(cx_Oracle.NUMBER)
            cursor.callproc("INSERTAR_TELEFONO", [id_tel,telefono])
            telefono_id = id_tel.getvalue()
        finally:
            cursor.close()


        try:
            con=self.connection()
            cursor = con.cursor()
            cursor.callproc("INSERTAR_EMPLEADO", [rut, nombres, apellidos, sexo, cargo, direccion_id, telefono_id, fecha, areaDepto])
            
            
            print("Datos insertados correctamente en la tabla Empleados.")
        except cx_Oracle.Error as error:
            print("Error al insertar datos en la tabla Empleados:", error)
        finally:
            cursor.close()
            

        #Extraer datos de ContactosEmp
        contactos = array.get('ContactosEmp', [])
        if contactos:
               for contacto in contactos:
                   nombre = contacto.get('nombre')
                       # Omitir contacto si el nombre está vacío o es None
                   if not nombre or nombre.strip() == '':
                       print("dato vacio")
                       continue
                   
                   # Validar que todos los campos están llenos o vacíos
                   if all(valor is None or len(str(valor).strip()) == 0 for valor in contacto.values()):
                       continue  # Contacto completamente vacío, omitir
                   if any((valor is not None and len(str(valor).strip()) > 0) for valor in contacto.values()) and \
                      any((valor is None or len(str(valor).strip()) == 0) for valor in contacto.values()):
                       print("Los campos en ContactosEmp deben estar completamente completados o completamente vacíos.")
                   relacion = int(contacto.get('relacion'))
                   telefono = contacto.get('telefono')
                       # Insertar el contacto en la base de datos
                   
                   try:
                        con=self.connection()
                        cursor=con.cursor()
                        cursor.execute("SELECT MAX(id_telefono) FROM telefono")
                        max_id_tel = cursor.fetchone()[0]
                        if max_id_tel:
                            max_id_tel += 1
            
                        sql_insert="INSERT INTO telefono (id_telefono,num_telefono) VALUES (:1,:2)"
                        cursor.execute(sql_insert,(max_id_tel,telefono))
                        con.commit()
                   finally:
                        cursor.close()
                   try:
                        con=self.connection()
                        cursor=con.cursor()
                        cursor.execute("SELECT MAX(id_contacto) FROM contacto")
                        max_id_con = cursor.fetchone()[0]
                        if max_id_con:
                            max_id_con += 1
            
                        sql_insert="INSERT INTO contacto (id_contacto, nombre_contacto, parentesco_id, telefono_id, rut_emp) VALUES (:1,:2,:3,:4,:5)"
                        cursor.execute(sql_insert,(max_id_con,nombre, relacion, max_id_tel, rut))
                        con.commit()
                   finally:
                        cursor.close()
                    
        cargas = array.get('CargaEmp', [])
        for carga in cargas:
            
            rut_fam = carga.get('rut')
            if not rut_fam or rut_fam.strip() == '':
                continue
            
            if all(valor is None or len(str(valor).strip()) == 0 for valor in carga.values()):
                continue

            nombre = carga.get('nombre')
            parentesco = int(carga.get('parentesco'))

            # Insertar la carga familiar en la base de datos
            try:
                con=self.connection()
                cursor = con.cursor()
                sql_insert = """
                INSERT INTO carga_familiar (rut_familiar, rut_emp, nombre_familiar, parentesco_id)
                VALUES (:1, :2, :3, :4)
                """
                cursor.execute(sql_insert, (rut_fam, rut, nombre, parentesco))
                con.commit()
                print("Datos insertados correctamente en la tabla CargaEmp.")
            except cx_Oracle.Error as error:
                print("Error al insertar datos en la tabla CargaEmp:", error)
            finally:
                cursor.close()
   
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
            result=cur.var(cx_Oracle.NUMBER)
            cur.callproc("EXISTE_EMP", [rut, result])
            if int(result.getvalue())==1:
                return True
            else:
                return False
        except cx_Oracle.Error as error:
            print(f"Error al ejecutar la consulta: {error}")
        finally:
            cur.close()

    def eliminar_carga_familiar(self,nombre_carga, rut_trabajador):
        cur = self.conn.cursor()
        try:
            cur.execute("""
                DELETE FROM carga_familiar
                WHERE rut_emp = :rut_emp
                AND nombre_familiar = :nombre_familiar
            """, {'rut_emp': rut_trabajador, 'nombre_familiar': nombre_carga})
            self.conn.commit()
            print("Carga familiar eliminada correctamente.")
        except cx_Oracle.Error as error:
            print("Error al eliminar carga familiar:", error)
        finally:
            cur.close()
            
    def eliminar_contacto(self,nombre_contacto, rut_trabajador):
        
        cur = self.conn.cursor()
        try:
            cur.execute("""
                DELETE FROM contacto
                WHERE rut_emp = :rut_emp
                AND nombre_contacto = :nombre_contacto
            """, {'rut_emp': rut_trabajador, 'nombre_contacto': nombre_contacto})
            self.conn.commit()
            print("Contacto eliminado correctamente.")
        except cx_Oracle.Error as error:
            print("Error al eliminar contacto:", error)
        finally:
            cur.close()
            
    def update_employee_data(self,rut, nombre, apellidos):
        print(rut)
        cur = self.conn.cursor()
        try:
            cur.execute("""
                UPDATE empleado
                SET 
                    nombres = :nombres,
                    apellidos = :apellidos
                WHERE rut = :rut
            """, {'rut': rut,'nombres': nombre, 'apellidos': apellidos})
            self.conn.commit()
            print("Datos de empleado actualizados correctamente.")
            return True
        except cx_Oracle.Error as error:
            print("Error al actualizar datos de empleado:", error)
            return False
        finally:
            cur.close()
            
import cx_Oracle
from Management.UserMana import PasswordManager
import os
from dotenv import load_dotenv

class UserDatabase:
    def __init__(self):
        load_dotenv()
        self.hostname = str(os.getenv("Hostname"))
        self.port = int(os.getenv("Port"))
        self.service_name = str(os.getenv("Service"))
        self.username = str(os.getenv("db_Username"))
        self.passw= str(os.getenv("Password"))
        # Configura la conexión a Oracle
        dsn_tns = cx_Oracle.makedsn(self.hostname, self.port, service_name=self.service_name)
        self.conn = cx_Oracle.connect(self.username ,self.passw, dsn=dsn_tns)
        # Inicializa la estructura de la base de datos si no existe
        self.__initialize_database()

    def __initialize_database(self):
        # Método privado para crear la tabla si no existe
        cursor = self.conn.cursor()
        cursor.close()

    def create_user(self,cargo_id, rut,username, password):
        manager = PasswordManager()
        hashed_password = manager.hash_credencials(password)
        cursor = self.conn.cursor()
        try:
            id=cursor.var(cx_Oracle.NUMBER)
            cursor.callproc('insertar_usuario', [id, cargo_id, rut, username, hashed_password])
            
        except cx_Oracle.Error as e:
            if e.args[0].code == 1:
                print(f"El usuario '{username}' ya existe en la base de datos")
            else:
                print("Error al insertar usuario:", e)
        finally:
            cursor.close()

    def authenticate_user(self, username, password):
        manager = PasswordManager()
        cursor = self.conn.cursor()
        try:
            cursor.execute('SELECT hash_pass FROM usuarios WHERE usuario = :username', {'username': username})
            
            result = cursor.fetchone()
            if result is None:
                print("User not found")
                return False
            
            hashed_password = result[0]
            is_valid = manager.check_password(password, hashed_password)
            return is_valid
        
        except cx_Oracle.Error as e:
            print("Error authenticating user:", e)
        finally:
            cursor.close()

import cx_Oracle
from UserMana import PasswordManager 

class UserDatabase:
    def __init__(self):
        self.hostname = 'localhost'  # Or the hostname/IP of your Oracle server
        self.port = 1521             # Default port for Oracle XE
        self.service_name = 'XE'     # Service name for Oracle XE
        self.username = 'app_user'   # Oracle username
        self.passw = '1234567Aa'     # Oracle user password
        # Configura la conexión a Oracle
        dsn_tns = cx_Oracle.makedsn(self.hostname, self.port, self.service_name)
        self.conn = cx_Oracle.connect(self.username ,self.passw, dsn=dsn_tns)

        # Inicializa la estructura de la base de datos si no existe
        self.__initialize_database()

    def __initialize_database(self):
        # Método privado para crear la tabla si no existe
        cursor = self.conn.cursor()

        cursor.close()

    def create_user(self, rut,username, password):
        manager = PasswordManager()
        hashed_password = manager.hash_password(password)

        cursor = self.conn.cursor()

        cursor.execute("SELECT MAX(id) FROM usuarios")
        max_id = cursor.fetchone()[0]
        if max_id is None:
            max_id = 0
        new_id = max_id + 1
        
        try:
            cursor.execute('INSERT INTO usuarios (id, trabajador_rut, username, hashed_password) VALUES (:id , :rut,:username, :hashed_password)',
                           {'id':new_id,'rut':rut,'username': username, 'hashed_password': hashed_password})
            self.conn.commit()
            print("Usuario creado exitosamente")
        except cx_Oracle.IntegrityError as e:
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
            cursor.execute('SELECT hashed_password FROM usuarios WHERE username = :username', {'username': username})
            result = cursor.fetchone()

            if result is None:
                return False

            hashed_password = result[0]

            # Verificar la contraseña utilizando PasswordManager
            is_valid = manager.check_password(password, hashed_password)

            return is_valid
        finally:
            cursor.close()

    def __del__(self):
        self.conn.close()
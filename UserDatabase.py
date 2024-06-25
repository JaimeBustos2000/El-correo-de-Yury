from UserMana import PasswordManager
import sqlite3

# Clase que maneja la base de datos de usuarios
class UserDatabase:
    def __init__(self):
        self.__db_name = "cdyusr.db"  # Atributo privado
        self.__initialize_database()  # Método privado

    def __initialize_database(self):
        # Método privado
        conn = sqlite3.connect(self.__db_name)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                Trabajador_id TEXT UNIQUE NOT NULL,
                username TEXT NOT NULL UNIQUE,
                hashed_password TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

    def create_user(self, username, password):
        manager = PasswordManager()
        hashed_password = manager.hash_password(password)
        conn = sqlite3.connect(self.__db_name)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO usuarios (username, hashed_password) VALUES (?, ?)', (username, hashed_password))
        conn.commit()
        conn.close()

    def authenticate_user(self, username, password):
        manager = PasswordManager()
        conn = sqlite3.connect(self.__db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT password_hash FROM usuarios WHERE username = ?', (username,))
        result = cursor.fetchone()
        conn.close()
        if result is None:
            return False
        hashed_password = result[0]
        return manager.check_password(password, hashed_password)

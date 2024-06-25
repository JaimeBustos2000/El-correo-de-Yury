import bcrypt

# Clase para manejar contraseñas y hashing seguro
class PasswordManager:
    def __init__(self):
        self.__salt_rounds = 12  # Atributo privado

    def hash_password(self, password):
        # Método público
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(self.__salt_rounds))
        return hashed_password

    def check_password(self, password, hashed_password):
        # Método público
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password)


import bcrypt

# Clase para manejar contraseñas y hashing seguro
class PasswordManager:
    def __init__(self):
        self.__salt_rounds = 12  # Atributo privado
        
    def hash_credencials(self, password):
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(self.__salt_rounds))
        return hashed_password

    def check_password(self, password, hashed_password):
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
    
    def check_username(self, user, hashed_username):
        return bcrypt.checkpw(user.encode('utf-8'), hashed_username)


import hashlib
from db import get_db_connection

# Función para obtener el hash de una contraseña
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Función para autenticar al usuario
def authenticate(username, password):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()



    if user and user["password"] == hash_password(password):
        return user["role"]
    return None

# Función para crear un nuevo usuario
def crear_usuario(nombre_usuario, contraseña, direccion_wallet, role):
    conn = get_db_connection()
    cursor = conn.cursor()
    hashed_password = hash_password(contraseña)
    cursor.execute("INSERT INTO users (username, password, direccion_wallet, role) VALUES (%s, %s, %s, %s)",
                   (nombre_usuario, hashed_password, direccion_wallet, role))
    conn.commit()
    cursor.close()
    conn.close()
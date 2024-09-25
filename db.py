import mysql.connector
import pandas as pd

# Configuración de la base de datos
db_config = {
    'user': 'admin',  
    'password': '#3eLcDbd2024*',  
    'host': 'permisos.chqagagiyz8f.us-east-1.rds.amazonaws.com',  
    'database': 'permisos',  
}

# Conexión a la base de datos
def get_db_connection():
    return mysql.connector.connect(**db_config)

# Función para agregar permisos a la base de datos
def agregar_permiso(usuario_solicitante, tipo, tiempo, fecha_inicio, fecha_fin=None, hora_inicio=None, hora_fin=None):
    estado = 'pendiente'
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO permisos (usuario_solicitante, tipo, tiempo, hora_inicio, hora_fin, fecha_inicio, fecha_fin, estado) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
        (usuario_solicitante, tipo, tiempo, hora_inicio, hora_fin, fecha_inicio, fecha_fin, estado)
    )
    conn.commit()
    cursor.close()
    conn.close()

# Función para obtener permisos de la base de datos
def obtener_permisos():
    conn = get_db_connection()
    df = pd.read_sql("SELECT * FROM permisos", conn)
    conn.close()
    return df

# Función para autorizar permisos
def autorizar_permiso(permiso_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE permisos SET estado = 'aprobado' WHERE id = %s", (permiso_id,))
    conn.commit()
    cursor.close()
    conn.close()

# Función para obtener el historial de permisos de un usuario
def obtener_historial_permisos(username):
    conn = get_db_connection()
    query = """
    SELECT *
    FROM permisos
    WHERE usuario_solicitante = %s
    ORDER BY fecha_inicio DESC
    """
    df = pd.read_sql(query, conn, params=(username,))
    conn.close()
    return df

# Función para actualizar el estado de los permisos automáticamente
def actualizar_estado_permisos():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Actualiza permisos diarios que han pasado la fecha de fin
    cursor.execute("UPDATE permisos SET estado = 'terminado' WHERE fecha_fin < CURDATE() AND estado = 'aprobado'")

    # Actualiza permisos por horas que han pasado la hora de fin
    cursor.execute("""
        UPDATE permisos
        SET estado = 'terminado'
        WHERE tiempo = 'horas' AND CONCAT(fecha_inicio, ' ', hora_fin) < NOW() AND estado = 'aprobado'
    """)

    conn.commit()
    cursor.close()
    conn.close()

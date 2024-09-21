import streamlit as st
import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt
import seaborn as sns

# Configuración de la base de datos
db_config = {
    'user': 'tu_usuario',
    'password': 'tu_contraseña',
    'host': 'localhost',
    'database': 'gestion_permisos'
}

# Conexión a la base de datos
def get_db_connection():
    return mysql.connector.connect(**db_config)

"""
# Función para obtener el hash de una contraseña
def hash_password(password):
    return sha256(password.encode()).hexdigest()

# Función para autenticar al usuario
def authenticate(username, password):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios WHERE nombre_usuario = %s", (username,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if user and user["contraseña"] == hash_password(password):
        return user["rol"]
    return None
"""


# Función para agregar permisos a la base de datos
def agregar_permiso(nombre, tipo, fecha_inicio, fecha_fin):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO permisos (nombre, tipo, fecha_inicio, fecha_fin) VALUES (%s, %s, %s, %s)",
                   (nombre, tipo, fecha_inicio, fecha_fin))
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
    cursor.execute("UPDATE permisos SET aprobado = TRUE WHERE id = %s", (permiso_id,))
    conn.commit()
    cursor.close()
    conn.close()

# Función para visualizar datos
def visualizar_datos(df):
    st.subheader("Gráficos de Análisis")
    fig, ax = plt.subplots()
    sns.countplot(x='tipo', data=df, ax=ax)
    st.pyplot(fig)

# Título de la aplicación
st.title("Gestión de Permisos de Trabajo")

# Autenticación
st.sidebar.header("Iniciar Sesión")
username = st.sidebar.text_input("Nombre de usuario")
password = st.sidebar.text_input("Contraseña", type="password")



# Simulación de usuarios para pruebas
users = {
    "supervisor": "supervisor123",
    "trabajador": "trabajador123"
}

def authenticate(username, password):
    return users.get(username) == password

# Variable de sesión para controlar el estado de inicio de sesión
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Manejo de inicio de sesión
if st.sidebar.button("Iniciar Sesión"):
    if authenticate(username, password):
        st.session_state.logged_in = True
        st.session_state.username = username
        st.sidebar.success("Inicio de sesión exitoso")
    else:
        st.sidebar.error("Nombre de usuario o contraseña incorrectos.")

# Lógica de la aplicación
if st.session_state.logged_in:
    # Menú de opciones
    st.sidebar.header("Menú")
    if st.session_state.username == "supervisor":
        option = st.sidebar.selectbox("Selecciona una opción:", ["Crear Permiso", "Autorizar Permisos", "Monitoreo", "Informes"])
    else:
        option = st.sidebar.selectbox("Selecciona una opción:", ["Solicitar Permiso"])

    # Supervisor: Crear Permiso
    if option == "Crear Permiso":
        st.subheader("Formulario de Creación de Permisos")
        nombre_trabajador = st.text_input("Nombre del Trabajador")
        tipo_permiso = st.selectbox("Tipo de Permiso", ["Horas Extra", "Día Libre", "Permiso Médico"])
        fecha_inicio = st.date_input("Fecha de Inicio")
        fecha_fin = st.date_input("Fecha de Fin")
        
        if st.button("Enviar"):
            agregar_permiso(nombre_trabajador, tipo_permiso, fecha_inicio, fecha_fin)
            st.success("Permiso creado con éxito")

    # Supervisor: Autorizar Permisos
    elif option == "Autorizar Permisos":
        st.subheader("Autorizar Permisos")
        df = obtener_permisos()
        st.write(df)
        
        permiso_id = st.number_input("ID del Permiso a Autorizar", min_value=1)
        if st.button("Autorizar"):
            autorizar_permiso(permiso_id)
            st.success(f"Permiso con ID {permiso_id} autorizado.")

    # Trabajador: Solicitar Permiso
    elif option == "Solicitar Permiso":
        st.subheader("Formulario de Solicitud de Permiso")
        tipo_permiso = st.selectbox("Tipo de Permiso", ["Horas Extra", "Día Libre", "Permiso Médico"])
        fecha_inicio = st.date_input("Fecha de Inicio")
        fecha_fin = st.date_input("Fecha de Fin")
        
        if st.button("Solicitar"):
            agregar_permiso(st.session_state.username, tipo_permiso, fecha_inicio, fecha_fin)
            st.success("Solicitud de permiso enviada")

    # Monitoreo
    elif option == "Monitoreo":
        st.subheader("Monitoreo de Permisos")
        df = obtener_permisos()
        st.write(df)

    # Informes
    elif option == "Informes":
        st.subheader("Informes de Productividad")
        df = obtener_permisos()
        visualizar_datos(df)

    # Opción de cerrar sesión
    if st.sidebar.button("Cerrar Sesión"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        # Limpiar datos de sesión
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.session_state.logged_in = False  # Asegurarse de que esté en estado de no autenticado
        st.write("Cierre de sesión exitoso. Vuelve a iniciar sesión.")
        st.stop()  # Detiene la ejecución y muestra el mensaje de cierre de sesión

else:
    st.sidebar.info("Por favor, inicie sesión para continuar.")

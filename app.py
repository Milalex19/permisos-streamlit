import streamlit as st
import pandas as pd
from db import agregar_permiso, obtener_permisos, autorizar_permiso, obtener_historial_permisos, actualizar_estado_permisos
from auth import authenticate, crear_usuario
import plotly.express as px

# Inicializar el estado de la sesión
if "new_user" not in st.session_state:
    st.session_state["new_user"] = ""
if "new_password" not in st.session_state:
    st.session_state["new_password"] = ""
if "login_username" not in st.session_state:
    st.session_state["login_username"] = ""
if "login_password" not in st.session_state:
    st.session_state["login_password"] = ""

# Título de la aplicación
st.title("Gestión de Permisos de Trabajo")

# Autenticación
st.sidebar.header("Iniciar Sesión / Registro")
choice = st.sidebar.selectbox("Selecciona una opción:", ["Iniciar Sesión", "Registrarse"])

if choice == "Registrarse":
    st.subheader("Crear Nuevo Usuario")
    new_user = st.text_input("Nombre de Usuario", key="new_user")
    new_password = st.text_input("Contraseña", type='password', key="new_password")
    new_direccion_wallet = st.text_input("Dirección Wallet", key="new_direccion_wallet")
    role = st.selectbox("Selecciona el rol del usuario", ["trabajador", "supervisor"], key="role")
    
    if st.button("Registrar"):
        if new_user and new_password and new_direccion_wallet:
            crear_usuario(new_user, new_password, new_direccion_wallet, role)
            st.success("Usuario creado exitosamente. Por favor, inicia sesión.")
            
        else:
            st.error("Por favor, completa todos los campos.")

elif choice == "Iniciar Sesión":
    st.subheader("Iniciar Sesión")
    username = st.sidebar.text_input("Nombre de usuario", key="login_username")
    password = st.sidebar.text_input("Contraseña", type="password", key="login_password")

    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if st.sidebar.button("Iniciar Sesión"):
        user_role = authenticate(username, password)
        if user_role:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.user_role = user_role
            st.sidebar.success("Inicio de sesión exitoso")
            actualizar_estado_permisos()  # Actualiza los permisos al iniciar sesión
        else:
            st.sidebar.error("Nombre de usuario o contraseña incorrectos.")

# Lógica de la aplicación
if st.session_state.get('logged_in', False):
    # Menú de opciones
    st.sidebar.header("Menú")
    if st.session_state.user_role == "supervisor":
        option = st.sidebar.selectbox("Selecciona una opción:", ["Crear Permiso", "Autorizar Permisos", "Monitoreo", "Informes"])
    else:
        option = st.sidebar.selectbox("Selecciona una opción:", ["Solicitar Permiso", "Ver Historial de Permisos"])

    # match
    # Supervisor: Crear Permiso
    if option == "Crear Permiso":
        st.subheader("Formulario de Creación de Permisos")
        nombre_trabajador = st.text_input("Nombre del Trabajador", key="nombre_trabajador") if st.session_state.user_role == "supervisor" else st.session_state.username

        tipo_permiso = st.selectbox("Tipo de Permiso", ["Día Libre", "Vacaciones", "Cita Médica", "Permiso Personal", "Calamidad Doméstica"], key="tipo_permiso")
        duracion_permiso = st.radio("Duración del Permiso", ["Día", "Horas"], key="duracion_permiso")

        if duracion_permiso == "Día":
            fecha_inicio = st.date_input("Fecha de Inicio", key="fecha_inicio")
            fecha_fin = st.date_input("Fecha de Fin", key="fecha_fin")
            hora_inicio = None
            hora_fin = None
        else:
            fecha_inicio = st.date_input("Fecha del Permiso", key="fecha_hora_inicio")
            hora_inicio = st.time_input("Hora de Inicio", key="hora_inicio")
            hora_fin = st.time_input("Hora de Fin", key="hora_fin")

        if st.button("Enviar"):
            if duracion_permiso == "Día":
                agregar_permiso(nombre_trabajador, tipo_permiso, "día", fecha_inicio, fecha_fin)
            else:
                agregar_permiso(nombre_trabajador, tipo_permiso, "horas", fecha_inicio, hora_inicio=hora_inicio, hora_fin=hora_fin)
            st.success("Permiso creado con éxito")

    # Supervisor: Autorizar Permisos
    elif option == "Autorizar Permisos":
        st.subheader("Autorizar Permisos")
        df = obtener_permisos()
        st.write(df)
        
        permiso_id = st.number_input("ID del Permiso a Autorizar", min_value=1, key="permiso_id")
        if st.button("Autorizar"):
            autorizar_permiso(permiso_id)
            st.success(f"Permiso con ID {permiso_id} autorizado.")

    # Trabajador: Solicitar Permiso
    elif option == "Solicitar Permiso":
        st.subheader("Formulario de Solicitud de Permiso")
        tipo_permiso = st.selectbox("Tipo de Permiso", ["Día Libre", "Vacaciones", "Cita Médica", "Permiso Personal", "Calamidad Doméstica"], key="solicitud_tipo_permiso")
        duracion_permiso = st.radio("Duración del Permiso", ["Día", "Horas"], key="solicitud_duracion_permiso")

        if duracion_permiso == "Día":
            fecha_inicio = st.date_input("Fecha de Inicio", key="solicitud_fecha_inicio")
            fecha_fin = st.date_input("Fecha de Fin", key="solicitud_fecha_fin")
            hora_inicio = None
            hora_fin = None
        else:
            fecha_inicio = st.date_input("Fecha del Permiso", key="solicitud_fecha_hora_inicio")
            hora_inicio = st.time_input("Hora de Inicio", key="solicitud_hora_inicio")
            hora_fin = st.time_input("Hora de Fin", key="solicitud_hora_fin")
        
        if st.button("Solicitar"):
            if duracion_permiso == "Día":
                agregar_permiso(st.session_state.username, tipo_permiso, "día", fecha_inicio, fecha_fin)
            else:
                agregar_permiso(st.session_state.username, tipo_permiso, "horas", fecha_inicio, hora_inicio=hora_inicio, hora_fin=hora_fin)
            st.success("Solicitud de permiso enviada")

    # Trabajador: Ver Historial de Permisos
    elif option == "Ver Historial de Permisos":
        st.subheader("Historial de Permisos")
        df = obtener_historial_permisos(st.session_state.username)
        st.write(df)

    # Monitoreo
    elif option == "Monitoreo":
        st.subheader("Monitoreo de Permisos")
        df = obtener_permisos()
        st.write(df)

    # Informes
    elif option == "Informes":
        st.subheader("Informes de Productividad")
        df = obtener_permisos()
        fig = px.bar(df, x='tipo', title="Permisos por Tipo")
        st.plotly_chart(fig)

    # Opción de cerrar sesión
    if st.sidebar.button("Cerrar Sesión"):
        st.session_state.clear()
        st.write("Cierre de sesión exitoso. Vuelve a iniciar sesión.")

else:
    st.sidebar.info("Por favor, inicia sesión o regístrate para continuar.")


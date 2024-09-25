# Plataforma-Permisos

# Gestión de Permisos de Trabajo

Este proyecto es una aplicación web desarrollada con **Streamlit**, **Python**, y **MySQL** para gestionar permisos de trabajo en entornos de producción. Permite a los trabajadores solicitar permisos, a los supervisores autorizarlos y realizar un seguimiento de los permisos a través de gráficos e informes. Además, ofrece funcionalidades de autenticación y registro de usuarios.

## Características

- **Autenticación y Registro**: Permite a los usuarios registrarse e iniciar sesión en la aplicación.
- **Roles de Usuario**: Existen dos tipos de roles: **Trabajador** y **Supervisor**. Cada uno tiene diferentes permisos y accesos en la aplicación.
- **Solicitud de Permisos**: Los trabajadores pueden solicitar permisos indicando el tipo de permiso, la duración (día u horas), y las fechas o tiempos específicos.
- **Autorización de Permisos**: Los supervisores pueden revisar y autorizar los permisos solicitados por los trabajadores.
- **Historial de Permisos**: Los trabajadores pueden ver el historial de sus permisos solicitados junto con su estado actual.
- **Monitoreo y Informes**: Los supervisores pueden monitorear todos los permisos en el sistema y generar informes visuales sobre los permisos solicitados.

## Estructura del Proyecto

- **`app.py`**: Archivo principal de la aplicación Streamlit que maneja la interfaz de usuario y las interacciones.
- **`bd.py`**: Módulo que contiene funciones para interactuar con la base de datos MySQL (agregar permisos, obtener permisos, autorizar permisos, etc.).
- **`auth.py`**: Módulo que maneja la autenticación y creación de usuarios en la base de datos.
- **Script SQL**: Contiene las instrucciones para crear la base de datos y las tablas necesarias para la aplicación.

## Requisitos

- Python 3.8 o superior
- MySQL
- Librerías de Python:
  - `streamlit`
  - `mysql-connector-python`
  - `pandas`
  - `plotly`

## Instalación

1. **Clonar el repositorio**:
    ```bash
    git clone https://github.com/matonn1/gestion-permisos-trabajo.git
    cd gestion-permisos-trabajo
    ```

2. **Instalar las dependencias**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Configurar la base de datos**:
    - Crear la base de datos y las tablas ejecutando el script SQL proporcionado en MySQL.
    - Asegúrate de que los datos de conexión a la base de datos en `bd.py` coincidan con tu configuración local.

4. **Ejecutar la aplicación**:
    ```bash
    streamlit run app.py
    ```

## Uso

### Iniciar Sesión / Registrarse

1. **Registro**: Los nuevos usuarios pueden registrarse proporcionando un nombre de usuario, una contraseña y seleccionando un rol (trabajador o supervisor).
2. **Inicio de Sesión**: Los usuarios registrados pueden iniciar sesión ingresando su nombre de usuario y contraseña.

### Funcionalidades

- **Trabajador**:
  - Solicitar permisos (días u horas).
  - Ver el historial de permisos.
  
- **Supervisor**:
  - Crear permisos para trabajadores.
  - Autorizar permisos.
  - Monitorear los permisos en el sistema.
  - Generar informes visuales sobre los permisos.

### Ejemplo de uso

1. Un trabajador inicia sesión, selecciona la opción de "Solicitar Permiso" y completa el formulario con la información necesaria.
2. Un supervisor inicia sesión, revisa los permisos pendientes, y autoriza aquellos que considera apropiados.
3. El trabajador puede revisar su historial de permisos para ver el estado de sus solicitudes.

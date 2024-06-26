# Aplicación Base para Pruebas de Frameworks

Esta es una aplicación base básica que permite a los usuarios registrarse, crear publicaciones y comentarlas. El objetivo es comparar este framework con otros según diferentes criterios.

## 📋 Requisitos

- Python 3.8 o superior

## 🚀 Instalación

1. Instala las dependencias del proyecto:
    ```bash
    pip install -r requirements.txt
    ```

## ⚙️ Configuración

1. Crea un archivo `.env` con los siguientes valores:
    a. Url base
        - `BASE_URL`: Esta es la url usada para generar url absolutas, por ejemplo se puede usar el valor "http://localhost:8000".
    b. Para enviar correos de recuperación de contraseña:
        - `EMAIL_HOST_USER`: El correo de Gmail desde el cual deseas enviar los correos.
        - `EMAIL_HOST_PASSWORD`: La contraseña de aplicación utilizada para autenticarse con la API de Gmail.

⚠️ Asegúrate de que el usuario y la contraseña proporcionados para la base de datos tengan los permisos necesarios.

## 🗄️ Ejecución de las migraciones de la Base de Datos

1. Crea una nueva migración:
    ```bash
    python manage.py makemigrations
    ```
2. Aplica las migraciones a la base de datos:
    ```bash
    python manage.py migrate
    ```

## 🎮 Ejecución del proyecto

1. Recopilar los archivos estáticos:
    ```bash
    python manage.py collectstatic
    ```
2. Ejecuta el proyecto:
    ```bash
    python manage.py runserver
    ```

##  🔨 Desarrollo
Para ejecutar el proyecto en un entorno de desarrollo, utiliza el comando:
  ```bash
  python manage.py runserver
  ```

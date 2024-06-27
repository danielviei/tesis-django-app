# Aplicación Base para Pruebas de Frameworks

Esta es una aplicación base básica que permite a los usuarios registrarse, crear publicaciones y comentarlas. El objetivo es comparar este framework con otros según diferentes criterios.

## 📋 Requisitos

- Python 3.8 o superior

## 🚀 Instalación

1. Crear el entorno virtual
   ```bash
   python -m venv venv
   ```

2. Activar el entorno virtual
   ```bash
   source ./venv/bin/activate
   ```

4. Instala las dependencias del proyecto:
    ```bash
    pip install -r requeriments.txt 
    ```
5. Crear la carpeta de archivos estáticos
   ```
   mkdir project/static
   ```
   
   
## ⚙️ Configuración

1. Crea un archivo `.env` con los siguientes valores dentro de la carpeta project/project:

    a. Url base
    - `BASE_URL`: Esta es la url usada para generar url absolutas, por ejemplo se puede usar el valor "http://localhost:8000".

    b. Para enviar correos de recuperación de contraseña:
    - `EMAIL_HOST_USER`: El correo de Gmail desde el cual deseas enviar los correos.
    - `EMAIL_HOST_PASSWORD`: La contraseña de aplicación utilizada para autenticarse con la API de Gmail.

2. Para crear un Usuario administrador debes ejecutar el siguiente comando y rellenar los campos que solicita:
   ```bash
   python ./project/manage.py createsuperuser
   ```

## 🗄️ Ejecución de las migraciones de la Base de Datos

1. Crea una nueva migración:
    ```bash
    python ./project/manage.py makemigrations
    ```
2. Aplica las migraciones a la base de datos:
    ```bash
    python ./project/manage.py migrate
    ```

## 🎮 Ejecución del proyecto

1. Recopilar los archivos estáticos:
    ```bash
    python ./project/manage.py collectstatic
    ```
2. Ejecuta el proyecto:
    ```bash
    python ./project/manage.py runserver
    ```

##  🔨 Desarrollo
Para ejecutar el proyecto en un entorno de desarrollo, utiliza el comando:
  ```bash
  python ./project/manage.py runserver
  ```

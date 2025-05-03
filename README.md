# 🏨 APP RESERVATION HOTEL WEB

[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Framework-green.svg)](https://fastapi.tiangolo.com/)
[![MySQL](https://img.shields.io/badge/MySQL-8%2B-blue.svg)](https://www.mysql.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-red.svg)](https://www.sqlalchemy.org/)
[![Pydantic](https://img.shields.io/badge/Pydantic-DataValidation-lightgrey.svg)](https://pydantic-docs.helpmanual.io/)
[![Uvicorn](https://img.shields.io/badge/Uvicorn-ASGI-blueviolet.svg)](https://www.uvicorn.org/)
[![Swagger UI](https://img.shields.io/badge/Swagger-UI-green.svg)](https://swagger.io/tools/swagger-ui/)
[![Postman](https://img.shields.io/badge/Postman-API%20Client-orange.svg)](https://www.postman.com/)
[![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-IDE-blue.svg)](https://code.visualstudio.com/)
[![Warp](https://img.shields.io/badge/Warp-Terminal-black.svg)](https://warp.dev/)

---

API RESTful desarrollada con FastAPI para la gestión de reservas hoteleras. Este proyecto permite administrar habitaciones, clientes, reservas, tipos de habitación y más, a través de endpoints consumibles desde cualquier frontend o cliente HTTP.

## API RESTful - Gestión de Reservas Hoteleras

La API de "APP RESERVATION HOTEL WEB" está diseñada para manejar las operaciones principales de un sistema de reservas hoteleras. Proporciona endpoints seguros y estructurados que permiten a los desarrolladores integrar funcionalidades de backend a cualquier frontend web, móvil o cliente HTTP. 

## Funciones clave:
- Gestión de habitaciones y sus tipos (individual, doble, suite, etc.).
- Registro y administración de clientes.
- Creación, consulta y cancelación de reservas.
- Control de estados de reserva (pendiente, confirmada, cancelada).
- Administración de usuarios y roles para el sistema.

La documentación interactiva (Swagger UI y ReDoc) facilita la comprensión y prueba de todos los endpoints disponibles.

## Esta API es ideal para proyectos hoteleros que necesitan una base robusta, escalable y fácil de extender.

## 🚀TECNOLOGÍAS UTILIZADAS

- Python 3.10+
- FastAPI
- MySQL 8+
- SQLAlchemy
- Pydantic
- Python-dotenv
- PyMySQL
- Uvicorn (ASGI server)
- Swagger UI (Documentación automática)

## 📦 REQUISITOS PREVIOS

Antes de comenzar, asegúrate de tener instalado lo siguiente:

1. **Python 3.10 o superior**: https://www.python.org/downloads/
2. **MySQL Server 8 o superior**: https://dev.mysql.com/downloads/mysql/
3. **MySQL Workbench** (para ejecutar scripts SQL): https://dev.mysql.com/downloads/workbench/
4. **Git**: https://git-scm.com/
5. **GitHub Desktop** (opcional para clonar repos desde interfaz gráfica): https://desktop.github.com/
6. **Warp** (opcional, terminal moderna para macOS): https://www.warp.dev/


## 🛠️ CONFIGURACIÓN DEL PROYECTO (PASO A PASO)

🔹 Paso 1: Clonar el repositorio

Abre tu terminal, y ejecuta:

    git clone https://github.com/Blazkull/APP-RESERVATION-HOTEL-WEB.git
    cd APP-RESERVATION-HOTEL-WEB

🔹 Paso 2: Crear y activar entorno virtual

Windows:

    python -m venv .\local
    .\local\Scripts\activate

macOS/Linux:

    python3 -m venv ./local
    source ./local/bin/activate

🔹 Paso 3: Instalar dependencias del proyecto

    pip install -r requirements.txt

🔹 Paso 4: Crear el archivo `.env` para las variables de entorno

En la raíz del proyecto, crea un archivo llamado `.env` con el siguiente contenido:

    DATABASE_URL=mysql+pymysql://root:1234@localhost:3306/db_reservation_hotel

⚠️ IMPORTANTE: Cambia `root`, `1234`, `localhost` y `3306` por tus credenciales reales de MySQL si son diferentes.

🔹 Paso 5: Crear la base de datos

Abre **MySQL Workbench**, crea una nueva conexión y:

1. Abre el archivo `script_create_db_reservation_hotel_and_insert_data.sql` que se encuentra en el repositorio.
2. Ejecuta **solo** la sección que crea la base de datos `db_reservation_hotel`. **No insertes los datos todavía**.

🔹 Paso 6: Ejecutar el proyecto para generar automáticamente las tablas

Una vez que la base de datos ha sido creada, ejecuta el proyecto con:

    uvicorn main:app --reload

Esto generará automáticamente las tablas necesarias mediante los modelos definidos en SQLAlchemy.

Abre **MySQL Workbench**, crea una nueva conexión y:

1. Abre el archivo `script_create_db_reservation_hotel_and_insert_data.sql` que se encuentra en el repositorio.
2. Ejecuta todo el script (`Ctrl + Shift + Enter` o botón "Run").

Este script:
- Solo crea la base de datos `db_reservation_hotel`

🔹 Paso 6: Ejecutar el proyecto para que se generen automáticamente las tablas desde los modelos SQLAlchemy

🔹 Paso 7: Levantar el servidor FastAPI

Ejecuta el siguiente comando desde la raíz del proyecto:

    uvicorn main:app --reload

Esto iniciará el servidor en modo desarrollo, escuchando por defecto en:  
📍 `http://127.0.0.1:8000/`


## 📘 DOCUMENTACIÓN INTERACTIVA

Después de levantar el servidor, puedes insertar los datos de prueba desde MySQL Workbench ejecutando la segunda parte del archivo `script_create_db_reservation_hotel_and_insert_data.sql` (la parte que contiene los INSERTs).

Una vez hecho esto, accede a la documentación generada automáticamente:

- Swagger UI: http://127.0.0.1:8000/docs
- Redoc: http://127.0.0.1:8000/redoc


## 📤 ENDPOINTS DESTACADOS

- GET /rooms/ → Listar habitaciones
- GET /clients/ → Listar clientes
- POST /clients/ → Registrar nuevo cliente
- POST /reservations/ → Crear una nueva reserva
- GET /room_types/ → Listar tipos de habitaciones
- DELETE /reservations/{id} → Eliminar reserva por ID

Consulta toda la documentación en `/docs` para explorar todos los recursos disponibles.


## 📂 Estructura del Proyecto

├── app/
│   ├── pycache/
│   └── main.py        # Archivo principal de la aplicación FastAPI. Punto de entrada.
│
├── core/
│   ├── pycache/
│   ├── config.py      # Configuración de la aplicación (base de datos, entorno, etc.).
│   └── database.py    # Conexión y configuración de la base de datos (SQLAlchemy).
│
├── local/             # Posible directorio para archivos locales/temporales (ubicación inusual).
│
├── models/
│   ├── pycache/
│   ├── client.py      # Modelo para la tabla de clientes.
│   ├── reservation_status.py # Modelo para la tabla de estados de reserva.
│   ├── reservation.py # Modelo para la tabla de reservas.
│   ├── room_status.py # Modelo para la tabla de estados de habitación.
│   ├── room_type.py   # Modelo para la tabla de tipos de habitación.
│   ├── room.py        # Modelo para la tabla de habitaciones.
│   ├── user_type.py   # Modelo para la tabla de tipos de usuario.
│   └── user.py        # Modelo para la tabla de usuarios.
│
├── routers/
│   ├── pycache/
│   ├── init.py
│   ├── clients.py     # Rutas para operaciones de clientes.
│   ├── dashboard.py   # Rutas para la funcionalidad del dashboard.
│   ├── login.py       # Ruta para la autenticación de usuarios.
│   ├── reservation_statues.py # Rutas para estados de reserva.
│   ├── reservations.py# Rutas para operaciones de reservas.
│   ├── room.py        # Rutas para operaciones de habitaciones.
│   ├── roomstatus.py  # Rutas para estados de habitación.
│   ├── roomtypes.py   # Rutas para tipos de habitación.
│   ├── users.py       # Rutas para operaciones de usuarios.
│   └── usertypes.py   # Rutas para tipos de usuario.
│
├── static/            # Directorio para archivos estáticos (CSS, JS, imágenes).
│
├── env/               # Posible directorio para configuración de entorno (ubicación inusual).
├── .gitattributes
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt
└── script_create_db_r...

## 👥 COLABORADORES

| Nombre     | Rol               | GitHub                                 |
|------------|------------------ |----------------------------------------|
| Jhoan Acosta| Backend Developer| https://github.com/Blazkull            |
| Kevin Perez| Frontend Developer| https://github.com/kevinperezroa       |
| Rafael Jimenez| Database Administrator | https://github.com/Tstark601        |


## 📌 NOTAS FINALES

- Es fundamental mantener el archivo `.env` fuera del repositorio público.
- Se recomienda usar herramientas como http://127.0.0.1:8000/docs para pruebas manuales.
- El proyecto está preparado para ser consumido desde cualquier frontend o cliente HTTP.
- Puedes expandir esta API para incluir autenticación, dashboards de administración, y lógica de negocio avanzada.

¡Listo! Ya puedes comenzar a trabajar con tu API REST de reservas hoteleras. 😎

from fastapi import FastAPI
from core.database import create_db_and_tables
from routers import usertypes,users,clients,roomtypes,roomstatus,room
from fastapi.middleware.cors import CORSMiddleware # habilitar CROS (conexion con frontend)

app = FastAPI()

@app.on_event("startup")
def startup():
    create_db_and_tables()

app.include_router(users.router)
app.include_router(usertypes.router)
app.include_router(clients.router)
app.include_router(roomtypes.router)
app.include_router(roomstatus.router)
app.include_router(room.router)
#app.include_router(reservations.router)




origins = [
    "http://localhost",
    "http://localhost:8080",
    "https://mi-dominio.com",
    "https://otro-dominio.net",
    "*",  # Permite todos los orígenes (solo para desarrollo, ¡no recomendado para producción!)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos HTTP (GET, POST, PUT, DELETE, OPTIONS, etc.)
    allow_headers=["*"],  # Permite todos los encabezados
)


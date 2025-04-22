import os
import uvicorn
from fastapi import FastAPI
from core.database import create_db_and_tables
from routers import usertypes, users, clients, roomtypes, roomstatus, room, reservations
from fastapi.middleware.cors import CORSMiddleware  # habilitar CORS

app = FastAPI()

@app.on_event("startup")
def startup():
    create_db_and_tables()

@app.get("/")
def read_root():
    return {"message": "API en línea en Render"}

# Inclusión de rutas
app.include_router(users.router)
app.include_router(usertypes.router)
app.include_router(clients.router)
app.include_router(roomtypes.router)
app.include_router(roomstatus.router)
app.include_router(room.router)
app.include_router(reservations.router)

# Configuración de CORS
origins = [
    "http://localhost",
    "http://localhost:8080",
    "https://mi-dominio.com",
    "https://otro-dominio.net",
    "*",  # Solo para desarrollo
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)

from fastapi import FastAPI
from core.database import create_db_and_tables
from routers import users, categories, reservations

app = FastAPI()

@app.on_event("startup")
def startup():
    create_db_and_tables()

app.include_router(users.router)
app.include_router(categories.router)
app.include_router(reservations.router)

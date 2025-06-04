# D:\APP-RESERVATION-HOTEL-WEB\core\config.py

from dotenv import load_dotenv
import os

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dotenv_path = os.path.join(project_root, '.env')

print(f"DEBUG: Intentando cargar .env desde: {dotenv_path}")

# --- INICIO DE LA MODIFICACIÓN ---
# Añade override=True para forzar la sobrescritura
load_dotenv(dotenv_path=dotenv_path, override=True)
# --- FIN DE LA MODIFICACIÓN ---

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

settings = Settings()

print(f"DEBUG: DATABASE_URL cargada en config.py: {settings.DATABASE_URL}")
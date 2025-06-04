# D:\APP-RESERVATION-HOTEL-WEB\test_env.py
import os
from dotenv import load_dotenv, dotenv_values

# Ruta al archivo .env
dotenv_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')

print(f"DEBUG_TEST: Ruta al .env: {dotenv_file_path}")

loaded_status = load_dotenv(dotenv_path=dotenv_file_path, override=True)
print(f"DEBUG_TEST: load_dotenv status: {loaded_status}")

values = dotenv_values(dotenv_path=dotenv_file_path)
print(f"DEBUG_TEST: Contenido del .env leído: {values}")

db_url_from_env = os.getenv("DATABASE_URL")
print(f"DEBUG_TEST: DATABASE_URL desde os.getenv(): {db_url_from_env}")
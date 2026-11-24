"""Configuración de la aplicación. Los datos de conexión se leen del archivo .env"""
import os

from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NOMBRE = os.getenv("DB_NAME", "turnos_medicos")

BCRYPT_ROUNDS = 12          # costo del hash de contraseñas
MAX_INTENTOS_LOGIN = 3      # intentos de inicio de sesión antes de volver al menú de acceso

import os
from dotenv import load_dotenv

load_dotenv()

# Configuración para Railway
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Si no hay DATABASE_URL, usar configuración por defecto
if not DATABASE_URL:
    DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/birads_db"

print(f"🔗 Conectando a: {DATABASE_URL[:30]}...")

# Configuración de la aplicación
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
SECRET_KEY = os.getenv("SECRET_KEY", "tu_clave_secreta_muy_segura")
PORT = int(os.getenv("PORT", 8080))

# URLs permitidas para CORS
ALLOWED_ORIGINS = [
    "http://localhost:4200",
    "http://localhost:3000", 
    "https://*.railway.app",
    "https://*.vercel.app",
    "*"  # Para desarrollo - quitar en producción
]
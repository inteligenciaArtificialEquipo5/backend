import os
from dotenv import load_dotenv

# Obtener la ruta de la raíz del proyecto (donde está run.py)
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))


# Cargar el archivo .env desde la raíz del proyecto
dotenv_path = os.path.join(base_dir, '.env')

load_dotenv(dotenv_path)


class Config:
    MONGO_URL = os.getenv("MONGO_URL")

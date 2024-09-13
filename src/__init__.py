# Importación de Flask para crear la aplicación web
from flask import Flask
# Importación de MongoClient de pymongo para conectarse a MongoDB
from pymongo import MongoClient
# Importación de la configuración de la aplicación desde el archivo de configuración
from .config.config import Config

# Inicialización de las variables para la conexión a MongoDB
mongo_client = None
db = None

# Función para crear la instancia de la aplicación Flask
def create_app():
    # Declaración global de las variables para asegurar acceso a nivel global
    global mongo_client, db

    # Creación de la instancia de la aplicación Flask
    app = Flask(__name__)
    
    # Cargar la configuración de la aplicación desde el archivo de configuración
    app.config.from_object(Config)
    
    # Inicializar la conexión a MongoDB usando pymongo con la URL proporcionada en la configuración
    mongo_client = MongoClient(app.config["MONGO_URL"])
    db = mongo_client['bloque1AI']  # Conectar a la base de datos 'bloque1AI'

    # Importar y registrar los blueprints de las rutas
    from .routes.predictionRoutes import prediction_bp
    from .routes.modelRoutes import model_bp

    # Registrar los blueprints para las rutas de predicciones y el modelo
    app.register_blueprint(prediction_bp)
    app.register_blueprint(model_bp)

    # Retornar la instancia de la aplicación Flask creada
    return app

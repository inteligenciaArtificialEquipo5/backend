from flask import Flask
from pymongo import MongoClient
from .config.config import Config

# Crear instancia de MongoClient
mongo_client = None
db = None


def create_app():
    global mongo_client, db

    app = Flask(__name__)
    app.config.from_object(Config)
    print((app.config["MONGO_URL"]))
    # Inicializar la conexión a MongoDB con pymongo
    mongo_client = MongoClient(app.config["MONGO_URL"])
    db = mongo_client['bloque1AI']

    # Importar y registrar blueprints
    from .routes.predictionRoutes import prediction_bp

    app.register_blueprint(prediction_bp)

    return app

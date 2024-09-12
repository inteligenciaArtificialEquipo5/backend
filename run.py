from src import create_app
from flask_cors import CORS

app = create_app()

# Habilitar CORS para todas las rutas
CORS(app)

if __name__ == "__main__":
    app.run(debug=True, port=8080, host='0.0.0.0')
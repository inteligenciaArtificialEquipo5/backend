# Importar la función create_app para crear la aplicación Flask
from src import create_app
# Importar CORS para habilitar el uso compartido de recursos entre orígenes
from flask_cors import CORS

# Crear la aplicación Flask utilizando la función create_app
app = create_app()

# Habilitar CORS para todas las rutas de la aplicación
CORS(app)

# Punto de entrada principal del script, se ejecuta solo si el archivo es ejecutado directamente
if __name__ == "__main__":
    # Ejecutar la aplicación Flask en modo depuración en el puerto 8080 y escuchando en todas las interfaces de red
    app.run(ssl_context=('server.cert', 'server.key'),
            debug=True, port=843, host='0.0.0.0')

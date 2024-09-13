# Importación de Flask Blueprint para crear rutas y métodos para la API
from flask import Blueprint, request, jsonify
# Importación de las funciones para realizar predicciones y cargar el modelo
from ..controllers.modelController import predict, load_model

# Creación del Blueprint para las rutas relacionadas con el modelo
model_bp = Blueprint('model_bp', __name__)

# Definición de la ruta para realizar predicciones, usando el método POST
@model_bp.route('/predict', methods=['POST'])
def predict_route():
    try:
        # Cargar el modelo desde el archivo
        model = load_model()

        # Obtener los datos de entrada de la solicitud POST en formato JSON
        input_data = request.json

        # Lista de campos requeridos que deben estar presentes en los datos de entrada
        required_fields = ['Age', 'RoomService', 'FoodCourt', 'ShoppingMall', 'Spa', 'VRDeck', 
                           'HomePlanet', 'Destination', 'CryoSleep', 'VIP', 'CabinDeck', 'CabinSide']

        # Validación de que todos los campos requeridos estén presentes en los datos de entrada
        for field in required_fields:
            if field not in input_data:
                # Si falta un campo, retorna un error 400 con un mensaje específico
                return jsonify({'error': f'Missing field: {field}'}), 400

        # Realizar la predicción utilizando los datos de entrada y el modelo cargado
        prediction_result = predict(input_data, model)

        # Retornar el resultado de la predicción en formato JSON con un código de estado 200 (éxito)
        return jsonify({'prediction': prediction_result}), 200

    # Manejo de errores específicos relacionados con los valores proporcionados
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    # Manejo de errores generales durante el proceso de predicción
    except Exception as e:
        return jsonify({'error': str(e)}), 500

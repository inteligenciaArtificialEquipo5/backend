from flask import Blueprint, request, jsonify
from ..controllers.modelController import predict, load_model

model_bp = Blueprint('model_bp', __name__)

@model_bp.route('/predict', methods=['POST'])
def predict_route():
    try:
        # Cargar el modelo
        model = load_model()

        # Obtener los datos de la solicitud POST
        input_data = request.json

        # Campos requeridos
        required_fields = ['Age', 'RoomService', 'FoodCourt', 'ShoppingMall', 'Spa', 'VRDeck', 
                            'HomePlanet', 'Destination', 'CryoSleep', 'VIP', 'CabinDeck', 'CabinSide']

        # Validar que todos los campos estén presentes
        for field in required_fields:
            if field not in input_data:
                return jsonify({'error': f'Missing field: {field}'}), 400

        # Hacer la predicción usando el modelo cargado
        prediction_result = predict(input_data, model)

        # Retornar la predicción como respuesta
        return jsonify({'prediction': prediction_result}), 200

    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

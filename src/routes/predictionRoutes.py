from flask import Blueprint, request, jsonify
from ..controllers.predictionController import *

prediction_bp = Blueprint('prediction_bp', __name__)


@prediction_bp.route('/predictions/test', methods=['GET'])
def test_prediction():
    return jsonify({"message": "Predictions working"}), 200


@prediction_bp.route('/predictions', methods=['POST'])
def save_prediction_route():
    data = request.json
    if 'datosParaPrueba' not in data or 'resultadoPrediccion' not in data:
        return jsonify({"message": "Datos incompletos"}), 400
    prediction_id = save_prediction(
        data['datosParaPrueba'], data['resultadoPrediccion'])
    return jsonify({"message": "Predicción guardada con éxito!", "id": str(prediction_id.inserted_id)}), 201


@prediction_bp.route('/predictions', methods=['GET'])
def get_all_predictions_route():
    predictions = get_all_predictions()
    predictions_list = []
    for prediction in predictions:
        prediction['_id'] = str(prediction['_id'])
        predictions_list.append(prediction)
    return jsonify(predictions_list), 200


@prediction_bp.route('/predictions/<prediction_id>', methods=['GET'])
def get_prediction_by_id_route(prediction_id):
    prediction = get_prediction_by_id(prediction_id)
    if prediction:
        prediction['_id'] = str(prediction['_id'])
        return jsonify(prediction), 200
    else:
        return jsonify({"message": "Predicción no encontrada"}), 404
    

@prediction_bp.route('/predictions/cryosleep-vip-transported', methods=['GET'])
def cryosleep_vip_transported():
    try:
        # Llamar al controlador para obtener los datos procesados
        data = get_cryosleep_vip_data()

        # Verificar si los datos existen
        if not data:
            return jsonify({"error": "No data found"}), 404

        # Retornar la respuesta en formato JSON
        return jsonify(data), 200

    except Exception as e:
        # Manejar cualquier error inesperado
        return jsonify({"error": "An error occurred", "message": str(e)}), 404

@prediction_bp.route('/predictions/age-transportation', methods=['GET'])
def age_transportation():
    try:
        # Obtener los datos del controlador
        data = get_age_data()
        return jsonify(data), 200  # Retornar la respuesta en formato JSON
    except Exception as e:
        return jsonify({"error": str(e)}), 404

@prediction_bp.route('/predictions/planet-destination', methods=['GET'])
def planet_destination():
    try:
        # Llamar al controlador para obtener los datos procesados
        data = get_planet_destination_data()

        # Retornar los datos en formato JSON
        return jsonify(data), 200
    except Exception as e:
        # Manejo de errores
        return jsonify({"error": str(e)}), 404
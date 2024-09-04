from flask import Blueprint, request, jsonify
from ..controllers.predictionController import save_prediction, get_all_predictions, get_prediction_by_id

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

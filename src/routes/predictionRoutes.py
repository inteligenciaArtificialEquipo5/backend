from flask import Blueprint, request, jsonify
from ..controllers.predictionController import *

# Crear un Blueprint para agrupar todas las rutas relacionadas con predicciones
prediction_bp = Blueprint('prediction_bp', __name__)

# Ruta para probar si el servicio de predicciones está funcionando correctamente
@prediction_bp.route('/predictions/test', methods=['GET'])
def test_prediction():
    # Devuelve un mensaje de confirmación junto con un código HTTP 200
    return jsonify({"message": "Predictions working"}), 200


# Ruta para guardar una nueva predicción en la base de datos
@prediction_bp.route('/predictions', methods=['POST'])
def save_prediction_route():
    # Obtener los datos del cuerpo de la solicitud en formato JSON
    data = request.json
    
    # Verificar si las claves necesarias ('datosParaPrueba' y 'resultadoPrediccion') están presentes
    if 'datosParaPrueba' not in data or 'resultadoPrediccion' not in data:
        # Si faltan datos, devolver un mensaje de error con un código HTTP 400
        return jsonify({"message": "Datos incompletos"}), 400
    
    # Llamar al controlador para guardar la predicción en la base de datos
    prediction_id = save_prediction(
        data['datosParaPrueba'], data['resultadoPrediccion'])
    
    # Responder con un mensaje de éxito y devolver el ID de la predicción guardada
    return jsonify({"message": "Predicción guardada con éxito!", "id": str(prediction_id.inserted_id)}), 201


# Ruta para obtener todas las predicciones guardadas
@prediction_bp.route('/predictions', methods=['GET'])
def get_all_predictions_route():
    # Llamar al controlador para obtener todas las predicciones almacenadas
    predictions = get_all_predictions()
    
    # Convertir cada predicción en un formato adecuado para JSON
    predictions_list = []
    for prediction in predictions:
        prediction['_id'] = str(prediction['_id'])  # Convertir el ID a cadena
        predictions_list.append(prediction)
    
    # Retornar la lista de predicciones en formato JSON con código HTTP 200
    return jsonify(predictions_list), 200


# Ruta para obtener una predicción específica por su ID
@prediction_bp.route('/predictions/<prediction_id>', methods=['GET'])
def get_prediction_by_id_route(prediction_id):
    # Llamar al controlador para obtener la predicción por su ID
    prediction = get_prediction_by_id(prediction_id)
    
    # Si la predicción existe, devolverla en formato JSON
    if prediction:
        prediction['_id'] = str(prediction['_id'])  # Convertir el ID a cadena
        return jsonify(prediction), 200
    else:
        # Si la predicción no se encuentra, devolver un mensaje de error con código 404
        return jsonify({"message": "Predicción no encontrada"}), 404


# Ruta para obtener datos relacionados con 'cryosleep', 'VIP' y 'transported' (personalización)
@prediction_bp.route('/predictions/cryosleep-vip-transported', methods=['GET'])
def cryosleep_vip_transported():
    try:
        # Llamar al controlador para obtener los datos procesados
        data = get_cryosleep_vip_data()

        # Verificar si se encontraron datos
        if not data:
            return jsonify({"error": "No data found"}), 404  # Si no hay datos, devolver un error 404

        # Devolver los datos en formato JSON con un código HTTP 200
        return jsonify(data), 200

    except Exception as e:
        # Manejar cualquier excepción inesperada y devolver un mensaje de error
        return jsonify({"error": "An error occurred", "message": str(e)}), 404


# Ruta para obtener datos relacionados con la edad y el transporte
@prediction_bp.route('/predictions/age-transportation', methods=['GET'])
def age_transportation():
    try:
        # Llamar al controlador para obtener los datos procesados relacionados con la edad y el transporte
        data = get_age_data()
        
        # Devolver los datos en formato JSON con un código HTTP 200
        return jsonify(data), 200  
    except Exception as e:
        # Manejar cualquier error y devolver un mensaje de error con código 404
        return jsonify({"error": str(e)}), 404


# Ruta para obtener datos sobre los destinos de los planetas (personalización)
@prediction_bp.route('/predictions/planet-destination', methods=['GET'])
def planet_destination():
    try:
        # Llamar al controlador para obtener los datos procesados sobre el destino de los planetas
        data = get_planet_destination_data()

        # Devolver los datos en formato JSON con un código HTTP 200
        return jsonify(data), 200
    except Exception as e:
        # Manejar cualquier error y devolver un mensaje de error con código 404
        return jsonify({"error": str(e)}), 404

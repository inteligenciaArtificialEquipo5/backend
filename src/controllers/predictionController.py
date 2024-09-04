from ..models.predictionModel import Prediction

def save_prediction(datos_para_prueba, resultado_prediccion):
    return Prediction.save_prediction(datos_para_prueba, resultado_prediccion)

def get_all_predictions():
    return Prediction.get_all_predictions()

def get_prediction_by_id(prediction_id):
    return Prediction.get_prediction_by_id(prediction_id)
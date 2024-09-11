# Importamos el modelo
from ..models.predictionModel import Prediction


def save_prediction(datos_para_prueba, resultado_prediccion):
    # Convertir el DataFrame a un diccionario
    datos_para_prueba_dict = datos_para_prueba.to_dict(orient='records')[0]  # Convertir la primera fila a un diccionario

    # Imprimir para ver cómo se están guardando los datos (para depuración)
    resultadoPrediccion = True if resultado_prediccion == 1 else False

    # Guardar la predicción en MongoDB
    return Prediction.save_prediction(datos_para_prueba_dict, resultadoPrediccion)

def get_all_predictions():
    return Prediction.get_all_predictions()

def get_prediction_by_id(prediction_id):
    return Prediction.get_prediction_by_id(prediction_id)
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

def get_cryosleep_vip_data():
    # Obtener todas las predicciones desde la base de datos
    predictions = get_all_predictions()

    # Inicializar variables para las cuatro combinaciones de CryoSleep y Transported
    cryosleep_transported = {
        "CryoSleep_True_Transported_True": 0,
        "CryoSleep_True_Transported_False": 0,
        "CryoSleep_False_Transported_True": 0,
        "CryoSleep_False_Transported_False": 0
    }

    # Inicializar variables para las cuatro combinaciones de VIP y Transported
    vip_transported = {
        "VIP_True_Transported_True": 0,
        "VIP_True_Transported_False": 0,
        "VIP_False_Transported_True": 0,
        "VIP_False_Transported_False": 0
    }

    # Procesar los datos de las predicciones
    for pred in predictions:
        predData = pred['datosParaPrueba']
        
        # Obtener los valores de CryoSleep, VIP y Transported
        cryo_sleep = predData.get("CryoSleep_True", False)
        vip = predData.get("VIP_True", False)
        transported = pred.get("resultadoPrediccion", False)

        # Guardar las combinaciones posibles para CryoSleep
        if cryo_sleep and transported:
            cryosleep_transported["CryoSleep_True_Transported_True"] += 1
        elif cryo_sleep and not transported:
            cryosleep_transported["CryoSleep_True_Transported_False"] += 1
        elif not cryo_sleep and transported:
            cryosleep_transported["CryoSleep_False_Transported_True"] += 1
        elif not cryo_sleep and not transported:
            cryosleep_transported["CryoSleep_False_Transported_False"] += 1

        # Guardar las combinaciones posibles para VIP
        if vip and transported:
            vip_transported["VIP_True_Transported_True"] += 1
        elif vip and not transported:
            vip_transported["VIP_True_Transported_False"] += 1
        elif not vip and transported:
            vip_transported["VIP_False_Transported_True"] += 1
        elif not vip and not transported:
            vip_transported["VIP_False_Transported_False"] += 1

    # Devolver los datos procesados para CryoSleep y VIP
    return {
        "CryoSleep": cryosleep_transported,
        "VIP": vip_transported
    }
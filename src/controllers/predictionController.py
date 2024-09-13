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

def get_age_data():
    # Obtener todas las predicciones desde la base de datos
    predictions = get_all_predictions()

    # Inicializar diccionarios para los rangos de edad
    age_bins_transported = {
        '0-10': 0, '11-20': 0, '21-30': 0, '31-40': 0, '41-50': 0,
        '51-60': 0, '61-70': 0, '71-80': 0, '81-90': 0, '91-100': 0
    }
    age_bins_not_transported = {
        '0-10': 0, '11-20': 0, '21-30': 0, '31-40': 0, '41-50': 0,
        '51-60': 0, '61-70': 0, '71-80': 0, '81-90': 0, '91-100': 0
    }

    # Procesar las predicciones
    for pred in predictions:
        predData = pred['datosParaPrueba']
        age = predData.get("Age", None)
        transported = pred.get("resultadoPrediccion", False)

        if age is not None:
            # Determinar el rango de edad
            if age <= 10:
                bin_key = '0-10'
            elif age <= 20:
                bin_key = '11-20'
            elif age <= 30:
                bin_key = '21-30'
            elif age <= 40:
                bin_key = '31-40'
            elif age <= 50:
                bin_key = '41-50'
            elif age <= 60:
                bin_key = '51-60'
            elif age <= 70:
                bin_key = '61-70'
            elif age <= 80:
                bin_key = '71-80'
            elif age <= 90:
                bin_key = '81-90'
            else:
                bin_key = '91-100'

            # Incrementar el contador correspondiente
            if transported:
                age_bins_transported[bin_key] += 1
            else:
                age_bins_not_transported[bin_key] += 1

    return {
        "age_bins_transported": age_bins_transported,
        "age_bins_not_transported": age_bins_not_transported
    }

def get_planet_destination_data():
    # Obtener todas las predicciones desde la base de datos
    predictions = get_all_predictions()

    # Inicializar diccionarios para los planetas y destinos
    planet_dest_transported = {}
    planet_dest_not_transported = {}

    # Definir mapeos para los planetas y destinos (ajusta estos nombres según tu formato de datos)
    planet_map = { "HomePlanet_0.0": "Europa", "HomePlanet_1.0": "Earth", "HomePlanet_2.0": "Mars" }
    destination_map = { "Destination_0.0": "TRAPPIST-1e", "Destination_1.0": "PSO J318.5-22", "Destination_2.0": "55 Cancri e" }

    # Procesar los datos de las predicciones
    for pred in predictions:
        predData = pred['datosParaPrueba']
        transported = pred.get("resultadoPrediccion", False)

        # Verificar planeta y destino en los datos
        planet = None
        destination = None

        # Encontrar el planeta
        for planet_key in planet_map:
            if predData.get(planet_key, 0) == 1:
                planet = planet_map[planet_key]
                break

        # Encontrar el destino
        for destination_key in destination_map:
            if predData.get(destination_key, 0) == 1:
                destination = destination_map[destination_key]
                break

        if planet and destination:
            if transported:
                # Incrementar contador para transportados
                if planet not in planet_dest_transported:
                    planet_dest_transported[planet] = {destination: 1}
                else:
                    planet_dest_transported[planet][destination] = planet_dest_transported[planet].get(destination, 0) + 1
            else:
                # Incrementar contador para no transportados
                if planet not in planet_dest_not_transported:
                    planet_dest_not_transported[planet] = {destination: 1}
                else:
                    planet_dest_not_transported[planet][destination] = planet_dest_not_transported[planet].get(destination, 0) + 1

    return {
        "planet_dest_transported": planet_dest_transported,
        "planet_dest_not_transported": planet_dest_not_transported
    }
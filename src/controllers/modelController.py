# Importación de librerías necesarias para la manipulación de datos y el uso del modelo
import os
import pandas as pd
import joblib
import numpy as np

# Importación de funciones específicas del controlador de predicción
from .predictionController import save_prediction

# Función para cargar el modelo previamente entrenado desde un archivo .pkl


def load_model():
    # Construye la ruta completa del archivo del modelo
    model_path = os.path.join(os.path.dirname(
        __file__), '..', 'model', 'model.pkl')

    # Verifica si el archivo del modelo existe
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"El archivo {model_path} no existe.")

    # Abre y carga el modelo usando joblib
    with open(model_path, 'rb') as model_file:
        model = joblib.load(model_file)

    # Retorna el modelo cargado
    return model

# Función para realizar la predicción utilizando datos de entrada y el modelo cargado


def predict(input_data, model):
    try:
        # Convierte los datos de entrada numéricos en un array de NumPy para el procesamiento
        input_array = np.array([float(input_data[col]) for col in [
            'Age', 'RoomService', 'FoodCourt', 'ShoppingMall', 'Spa', 'VRDeck'
        ]])

        # Crea un DataFrame con las columnas numéricas para usarlo en la predicción
        df_predict = pd.DataFrame([input_array], columns=[
            'Age', 'RoomService', 'FoodCourt', 'ShoppingMall', 'Spa', 'VRDeck'
        ])

        # Añadir columnas categóricas utilizando One-Hot Encoding manual para cada categoría
        # Codificación de HomePlanet
        df_predict['HomePlanet_0.0'] = 1 if input_data['HomePlanet'] == '0' else 0
        df_predict['HomePlanet_1.0'] = 1 if input_data['HomePlanet'] == '1' else 0
        df_predict['HomePlanet_2.0'] = 1 if input_data['HomePlanet'] == '2' else 0

        # Codificación de Destination
        df_predict['Destination_0.0'] = 1 if input_data['Destination'] == '0' else 0
        df_predict['Destination_1.0'] = 1 if input_data['Destination'] == '1' else 0
        df_predict['Destination_2.0'] = 1 if input_data['Destination'] == '2' else 0

        # Codificación de CryoSleep
        df_predict['CryoSleep_True'] = 1 if input_data['CryoSleep'] == True else 0

        # Codificación de VIP
        df_predict['VIP_True'] = 1 if input_data['VIP'] == True else 0

        # Codificación de CabinDeck
        df_predict['CabinDeck_B'] = 1 if input_data['CabinDeck'] == 'B' else 0
        df_predict['CabinDeck_C'] = 1 if input_data['CabinDeck'] == 'C' else 0
        df_predict['CabinDeck_D'] = 1 if input_data['CabinDeck'] == 'D' else 0
        df_predict['CabinDeck_E'] = 1 if input_data['CabinDeck'] == 'E' else 0
        df_predict['CabinDeck_F'] = 1 if input_data['CabinDeck'] == 'F' else 0
        df_predict['CabinDeck_G'] = 1 if input_data['CabinDeck'] == 'G' else 0
        df_predict['CabinDeck_T'] = 1 if input_data['CabinDeck'] == 'T' else 0

        # Codificación de CabinSide
        df_predict['CabinSide_S'] = 1 if input_data['CabinSide'] == 'S' else 0

        # Llenar valores faltantes con 0 para evitar problemas durante la predicción
        df_predict = df_predict.fillna(0)

        # Realizar la predicción usando el modelo cargado
        df_predict['Transported'] = model.predict(df_predict)

        # Guardar la predicción realizada en la base de datos
        save_prediction(df_predict, df_predict['Transported'].iloc[0])

        # Retornar el resultado de la predicción en formato booleano
        if df_predict['Transported'].iloc[0] == 1:
            return True
        else:
            return False

    # Manejo de errores en caso de que falten datos en el input
    except KeyError as e:
        raise ValueError(f"Falta un campo requerido: {str(e)}")
    # Manejo de cualquier otro error que ocurra durante la predicción
    except Exception as e:
        raise ValueError(f"Error al realizar la predicción: {str(e)}")

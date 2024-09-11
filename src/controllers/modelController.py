# Importación de librerías
import os
import pandas as pd
import joblib
import numpy as np

# Importación de funciones
from .predictionController import save_prediction

# Cargar el modelo
def load_model():
    model_path = os.path.join(os.path.dirname(__file__), '..', 'model', 'model.pkl')
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"El archivo {model_path} no existe.")
    with open(model_path, 'rb') as model_file:
        model = joblib.load(model_file)
    return model

# Realizar predicción
def predict(input_data, model):
    try:
        # Convertir los datos de entrada numéricos en un array de NumPy
        input_array = np.array([float(input_data[col]) for col in [
            'Age', 'RoomService', 'FoodCourt', 'ShoppingMall', 'Spa', 'VRDeck'
        ]])

        # Crear un DataFrame con las columnas numéricas
        df_predict = pd.DataFrame([input_array], columns=[
            'Age', 'RoomService', 'FoodCourt', 'ShoppingMall', 'Spa', 'VRDeck'
        ])

        # Añadir columnas categóricas usando One-Hot Encoding manual
        # HomePlanet
        df_predict['HomePlanet_0.0'] = 1 if input_data['HomePlanet'] == '0' else 0
        df_predict['HomePlanet_1.0'] = 1 if input_data['HomePlanet'] == '1' else 0
        df_predict['HomePlanet_2.0'] = 1 if input_data['HomePlanet'] == '2' else 0

        # Destination
        df_predict['Destination_0.0'] = 1 if input_data['Destination'] == '0' else 0
        df_predict['Destination_1.0'] = 1 if input_data['Destination'] == '1' else 0
        df_predict['Destination_2.0'] = 1 if input_data['Destination'] == '2' else 0

        # CryoSleep
        df_predict['CryoSleep_True'] = 1 if input_data['CryoSleep'] == 'True' else 0

        # VIP
        df_predict['VIP_True'] = 1 if input_data['VIP'] == 'True' else 0

        # CabinDeck
        df_predict['CabinDeck_B'] = 1 if input_data['CabinDeck'] == 'B' else 0
        df_predict['CabinDeck_C'] = 1 if input_data['CabinDeck'] == 'C' else 0
        df_predict['CabinDeck_D'] = 1 if input_data['CabinDeck'] == 'D' else 0
        df_predict['CabinDeck_E'] = 1 if input_data['CabinDeck'] == 'E' else 0
        df_predict['CabinDeck_F'] = 1 if input_data['CabinDeck'] == 'F' else 0
        df_predict['CabinDeck_G'] = 1 if input_data['CabinDeck'] == 'G' else 0
        df_predict['CabinDeck_T'] = 1 if input_data['CabinDeck'] == 'T' else 0

        # CabinSide
        df_predict['CabinSide_S'] = 1 if input_data['CabinSide'] == 'S' else 0

        # Llenar valores faltantes con 0
        df_predict = df_predict.fillna(0)

        # Realizar la predicción usando el modelo
        df_predict['Transported'] = model.predict(df_predict)

                # Guardando la predicción en la base de datos
        save_prediction(df_predict, df_predict['Transported'].iloc[0])

        # Retornar el resultado de la predicción
        if df_predict['Transported'].iloc[0] == 1:
            return True
        else:
            return False

    except KeyError as e:
        raise ValueError(f"Falta un campo requerido: {str(e)}")
    except Exception as e:
        raise ValueError(f"Error al realizar la predicción: {str(e)}")

# Importación de ObjectId para manejar los identificadores únicos de MongoDB
from bson import ObjectId
# Importación de la conexión a la base de datos desde el módulo correspondiente
from .. import db


# Clase Prediction para manejar las predicciones y su persistencia
class Prediction:
    # Método constructor de la clase Prediction
    def _init_(self, datos_para_prueba, resultado_prediccion):
        # Inicialización de los atributos con los datos de prueba y el resultado de la predicción
        self.datos_para_prueba = datos_para_prueba
        self.resultado_prediccion = resultado_prediccion

    # Método estático para guardar la predicción en la base de datos
    @staticmethod
    def save_prediction(datos_para_prueba, resultado_prediccion):
        # Estructura de los datos a guardar en la base de datos
        data = {
            "datosParaPrueba": datos_para_prueba,
            "resultadoPrediccion": resultado_prediccion
        }
        # Inserta la predicción en la colección 'Datos' y retorna el resultado de la operación
        return db['Datos'].insert_one(data)

    # Método estático para obtener todas las predicciones guardadas en la base de datos
    @staticmethod
    def get_all_predictions():
        # Retorna todas las entradas de la colección 'Datos'
        return db['Datos'].find()

    # Método estático para obtener una predicción por su identificador único
    @staticmethod
    def get_prediction_by_id(prediction_id):
        # Busca y retorna una predicción específica usando su ObjectId
        return db['Datos'].find_one({"_id": ObjectId(prediction_id)})

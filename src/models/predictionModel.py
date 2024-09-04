from bson import ObjectId
from .. import db


class Prediction:
    def _init_(self, datos_para_prueba, resultado_prediccion):
        self.datos_para_prueba = datos_para_prueba
        self.resultado_prediccion = resultado_prediccion

    @staticmethod
    def save_prediction(datos_para_prueba, resultado_prediccion):
        data = {
            "datosParaPrueba": datos_para_prueba,
            "resultadoPrediccion": resultado_prediccion
        }
        return db['Datos'].insert_one(data)

    @staticmethod
    def get_all_predictions():
        return db['Datos'].find()

    @staticmethod
    def get_prediction_by_id(prediction_id):
        return db['Datos'].find_one({"_id": ObjectId(prediction_id)})

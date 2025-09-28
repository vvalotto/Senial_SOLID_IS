"""
Define las clases procesadoras de señales
Demostración de OCP "técnico" con problemas de dependencias
"""
from dominio_senial.senial import *


class Procesador(object):
    """
    Clase ORIGINAL - Procesador de amplificación

    ✅ CUMPLE OCP: Esta clase NO fue modificada para agregar nueva funcionalidad
    Mantiene su responsabilidad original: amplificar señales por factor 2x
    """
    def __init__(self):
        """
        Constructor: Inicializa la clase procesadora original
        """
        self._senial_procesada = Senial()
        return

    def procesar_senial(self, senial):
        """
        Método ORIGINAL que realiza amplificación de la señal

        ✅ SIN MODIFICACIONES: Mantiene funcionalidad original intacta
        Siempre aplica factor de amplificación 2x (comportamiento original)

        :param senial: Señal a procesar (amplificar por 2x)
        :return: None (modifica estado interno)
        """
        print("Procesando amplificación (factor 2x)...")
        self._amplificacion = 2.0  # Factor fijo original
        self._senial_procesada._valores = list(map(self.funcion_doble, senial._valores))
        return

    def obtener_senial_procesada(self):
        """
        Devuelve la señal procesada
        :return: Objeto Senial con valores amplificados
        """
        return self._senial_procesada

    def funcion_doble(self, valor):
        """
        Función ORIGINAL que retorna el doble del valor de entrada
        :param valor: Valor a amplificar
        :return: Valor amplificado por el factor
        """
        return valor * self._amplificacion


class ProcesadorUmbral(object):
    """
    Clase NUEVA - Procesador por umbral

    ✅ EXTENSIÓN SIN MODIFICACIÓN: Nueva clase que agrega funcionalidad
    sin tocar el código original del Procesador

    ⚠️ PROBLEMA: Crea inconsistencias de interfaz y dependencias problemáticas
    """
    def __init__(self, umbral):
        """
        Constructor: Inicializa procesador con valor de umbral

        ⚠️ INTERFAZ INCONSISTENTE: Constructor diferente al Procesador original

        :param umbral: Valor del umbral para filtrado
        """
        self._senial_procesada = Senial()
        self._umbral = umbral
        return

    def procesar_senial(self, senial):
        """
        Método que realiza filtrado por umbral

        ⚠️ PROBLEMA DE DISEÑO: Misma interfaz externa pero semántica diferente
        - Procesador: amplifica siempre por 2x
        - ProcesadorUmbral: filtra por umbral configurado en constructor

        :param senial: Señal a procesar (filtrar por umbral)
        :return: None (modifica estado interno)
        """
        print(f"Procesando filtro por umbral ({self._umbral})...")
        self._senial_procesada._valores = list(map(self.funcion_umbral, senial._valores))
        return

    def obtener_senial_procesada(self):
        """
        Devuelve la señal procesada
        :return: Objeto Senial con valores filtrados
        """
        return self._senial_procesada

    def funcion_umbral(self, valor):
        """
        Función que filtra valores según el umbral establecido
        :param valor: Valor a evaluar
        :return: Valor original si < umbral, 0 en caso contrario
        """
        return valor if valor < self._umbral else 0

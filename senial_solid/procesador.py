"""
Módulo que define la clase Procesador de señales.

Aplicación del SRP: Esta clase tiene una única responsabilidad:
procesar señales digitales aplicando amplificación x2.
"""
from senial_solid.senial import Senial


class Procesador:
    """
    Procesador de señales digitales.

    Responsabilidad única: Aplicar amplificación x2 a señales digitales.
    Esta clase se encarga exclusivamente del procesamiento de datos,
    separando esta responsabilidad de la adquisición y visualización.
    """

    def __init__(self):
        """
        Inicializa el procesador de señales.
        """
        self._senial_procesada = Senial()

    def procesar_senial(self, senial):
        """
        Procesa una señal aplicando amplificación x2.

        :param senial: Señal de entrada a procesar
        """
        print("Procesando...")
        for i in range(senial.obtener_tamanio()):
            self._senial_procesada.poner_valor(senial.obtener_valor(i) * 2)

    def obtener_senial_procesada(self):
        """
        Retorna la señal procesada.

        :return: Señal con los valores procesados
        """
        return self._senial_procesada
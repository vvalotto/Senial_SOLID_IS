"""
Configurador - Factory Centralizado para la Aplicación

Aplicación del SRP: Esta clase tiene una única responsabilidad:
crear y configurar todas las instancias de clases que la aplicación necesita.

Versión: Configuración programática (sin DIP aún)
"""
from adquisicion_senial import Adquisidor
from procesamiento_senial import ProcesadorAmplificador, ProcesadorConUmbral
from presentacion_senial import Visualizador


class Configurador:
    """
    Factory Centralizado que aplica SRP para la creación de objetos.

    Responsabilidad única: Crear y configurar todas las instancias de clases
    que participan en la solución de procesamiento de señales.

    Configuración programática: Los valores están definidos en código
    (se migrará a configuración externa cuando apliquemos DIP).
    """

    @staticmethod
    def crear_adquisidor():
        """
        Crea el adquisidor de señales configurado para la aplicación.

        Configuración actual: 5 muestras por señal
        :return: Instancia configurada de Adquisidor
        """
        numero_muestras = 5
        return Adquisidor(numero_muestras)

    @staticmethod
    def crear_procesador_amplificador():
        """
        Crea un procesador amplificador con configuración específica.

        Configuración actual: Factor de amplificación 4.0
        :return: Instancia configurada de ProcesadorAmplificador
        """
        factor_amplificacion = 4.0
        return ProcesadorAmplificador(factor_amplificacion)

    @staticmethod
    def crear_procesador_umbral():
        """
        Crea un procesador con umbral con configuración específica.

        Configuración actual: Umbral de 8.0
        :return: Instancia configurada de ProcesadorConUmbral
        """
        umbral = 8.0
        return ProcesadorConUmbral(umbral)

    @staticmethod
    def crear_procesador():
        """
        Crea el procesador configurado de fábrica para la aplicación.

        Decisión centralizada: El Configurador decide qué procesador usar
        sin requerir input del usuario. Esta es la configuración "de fábrica"
        para la demostración didáctica.

        Configuración actual: ProcesadorAmplificador con factor 4.0
        :return: Instancia de BaseProcesador configurada de fábrica
        """
        return Configurador.crear_procesador_amplificador()

    @staticmethod
    def crear_visualizador():
        """
        Crea el visualizador de señales configurado para la aplicación.

        :return: Instancia configurada de Visualizador
        """
        return Visualizador()

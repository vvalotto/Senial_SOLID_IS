"""
Para OCP
Se refactoriza la clase de manera de extender otros tipos de
funciones de procesmiento de datos sin que impacte en los anteriores programas
o que cambiando solo las clases de alto nivel que pueda "armar" la solucion
"""
from abc import ABCMeta, abstractmethod
from dominio_senial.senial import Senial


class BaseProcesador(metaclass=ABCMeta):
    """
    Clase Abstracta Procesador
    """
    def __init__(self):
        """
        Se inicializa con la senial que se va a procesar
        """
        self._senial_procesada = Senial()

    @abstractmethod
    def procesar(self, senial):
        """
        Metodo abstracto que se implementara para cada tipo de procesamiento
        """

    def obtener_senial_procesada(self):
        """
        Devuelve la señal procesada
        """
        return self._senial_procesada


class ProcesadorAmplificador(BaseProcesador):
    """
    Clase Procesador Amplificador
    """
    def __init__(self, amplificacion):
        """
        Sobreescribe el constructor de la clase abstracta para inicializar el valor de amplificacion
        :param amplificacion: Factor de amplificación a aplicar
        """
        super().__init__()
        self._amplificacion = amplificacion

    def procesar(self, senial):
        """
        Implementa el procesamiento de amplificar cada valor de senial
        :param senial: Señal a procesar
        """
        print(f"Procesando amplificación (factor {self._amplificacion}x)...")
        self._senial_procesada._valores = list(map(self._amplificar, senial._valores))

    def _amplificar(self, valor):
        """
        Función que amplifica un valor por el factor establecido
        :param valor: Valor a amplificar
        :return: Valor amplificado
        """
        return valor * self._amplificacion

class ProcesadorConUmbral(BaseProcesador):
    """
    Clase Procesador con Umbral
    """
    def __init__(self, umbral):
        """
        Sobreescribe el constructor de la clase abstracta para inicializar el umbral
        :param umbral: Valor del umbral para filtrado
        """
        super().__init__()
        self._umbral = umbral

    def procesar(self, senial):
        """
        Implementa el procesamiento de la señal con filtrado por umbral
        :param senial: Señal a procesar
        """
        print(f"Procesando filtro por umbral ({self._umbral})...")
        self._senial_procesada._valores = list(map(self._funcion_umbral, senial._valores))

    def _funcion_umbral(self, valor):
        """
        Función que filtra valores según el umbral establecido
        :param valor: Valor a evaluar
        :return: Valor original si es menor al umbral, 0 en caso contrario
        """
        return valor if valor < self._umbral else 0

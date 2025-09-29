"""
Módulo que define la clase Visualizador de señales.

Aplicación del SRP: Esta clase tiene una única responsabilidad:
mostrar los datos de una señal digital.
"""
from dominio_senial import Senial


class Visualizador:
    """
    Visualizador de señales digitales.

    Responsabilidad única: Mostrar los datos de una señal digital en consola.
    Esta clase se encarga exclusivamente de presentar los valores de la señal,
    separando esta responsabilidad de la adquisición y procesamiento.
    """

    def __init__(self):
        """
        Inicializa el visualizador de señales.
        """

    def mostrar_datos(self, senial: Senial) -> None:
        """
        Muestra los datos de una señal en formato simple.

        :param senial: Señal a visualizar
        :raises TypeError: Si la señal no es del tipo correcto
        :raises ValueError: Si la señal está vacía
        """
        if not isinstance(senial, Senial):
            raise TypeError("El parámetro debe ser una instancia de la clase Senial")

        if senial.esta_vacia():
            raise ValueError("No se puede visualizar una señal vacía")

        print("=== VISUALIZACIÓN DE SEÑAL ===")
        print(f"Número de muestras: {senial.obtener_tamanio()}")
        print("Valores de la señal:")

        for i in range(senial.obtener_tamanio()):
            valor = senial.obtener_valor(i)
            print(f"  Muestra {i}: {valor}")

        print("=" * 31)

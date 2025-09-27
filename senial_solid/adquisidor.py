"""
Módulo que define la clase Adquisidor de señales.

Aplicación del SRP: Esta clase tiene una única responsabilidad:
adquirir datos de entrada para formar una señal digital.
"""
from senial_solid.senial import Senial


class Adquisidor:
    """
    Adquisidor de datos para señales digitales.

    Responsabilidad única: Capturar datos de entrada desde consola
    y construir una señal digital.
    """

    def __init__(self, numero_muestras):
        """
        Inicializa el adquisidor de señales.

        :param numero_muestras: Cantidad de muestras a adquirir
        """
        self._senial = Senial()
        self._nro_muestra = numero_muestras

    def _leer_dato_entrada(self):
        """
        Solicita un valor numérico por consola con validación.

        :return: Valor numérico ingresado por el usuario
        """
        while True:
            try:
                return float(input('Ingresar Valor: '))
            except ValueError:
                print('Dato mal ingresado, <enter>')

    def obtener_senial_adquirida(self):
        """
        Retorna la señal con los valores adquiridos.

        :return: Objeto Señal con los datos capturados
        """
        return self._senial

    def leer_senial(self):
        """
        Proceso principal de adquisición de datos.

        Lee la cantidad especificada de muestras desde consola y las almacena
        en la señal interna.
        """
        print("Lectura de la señal")
        for i in range(self._nro_muestra):
            print(f"Dato nro: {i}")
            self._senial.poner_valor(self._leer_dato_entrada())
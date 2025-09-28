"""
Módulo que define la entidad Señal.
Representa una señal digital como entidad del dominio.

Aplicación del SRP: Esta clase tiene una única responsabilidad:
gestionar los datos de una señal digital.
"""


class Senial:
    """
    Entidad que representa una señal digital.

    Responsabilidad única: Almacenar y gestionar los valores de una señal digital,
    proporcionando operaciones básicas de acceso y modificación.
    """

    def __init__(self):
        """
        Inicializa una nueva señal digital vacía.
        """
        self._valores = []

    def poner_valor(self, valor):
        """
        Agrega un nuevo valor al final de la señal.

        :param valor: Valor numérico a agregar a la señal
        """
        self._valores.append(valor)

    def obtener_valor(self, indice):
        """
        Recupera un valor específico de la señal por su índice.

        :param indice: Índice del valor a recuperar (base 0)
        :return: Valor en la posición especificada
        """
        try:
            return self._valores[indice]
        except IndexError:
            print(f"Error: Índice {indice} fuera de rango")
            return None

    def obtener_tamanio(self):
        """
        Retorna el número de muestras en la señal.

        :return: Cantidad de valores almacenados en la señal
        """
        return len(self._valores)

    def esta_vacia(self):
        """
        Verifica si la señal no contiene valores.

        :return: True si la señal está vacía, False en caso contrario
        """
        return len(self._valores) == 0
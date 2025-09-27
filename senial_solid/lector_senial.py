"""
Ejemplo de violación del principio de SRP
Aquí la clase LectorSenial tiene todas las responsabilidades del
procesamiento de una señal
"""


class LectorSenial:
    """
    Clase que posee todas las fases del procesamiento de una señal
    1. Lectura de la señal
    2. Procesamiento
    3. Visualización de la señal procesada

    VIOLACIÓN SRP: Esta clase tiene múltiples responsabilidades que deberían
    estar separadas en diferentes clases.
    """

    def __init__(self, tamanio: int):
        """
        Inicializa la instancia del lector

        :param tamanio: número de valores de la señal a procesar
        :raises ValueError: si tamanio es menor o igual a 0
        """
        if tamanio <= 0:
            raise ValueError("El tamaño debe ser mayor a 0")

        self._nro_muestra = tamanio
        self._valores = []
        self._valores_procesados = []

    def __leer_dato_entrada(self) -> float:
        """
        Metodo privado que se usa para ingresar un solo valor.
        En este caso se ingresa por consola.

        :return: valor numérico ingresado por el usuario
        """
        while True:
            try:
                return float(input('Valor: '))
            except ValueError:
                print('Dato mal ingresado, presione <enter> para continuar')
    
    def leer_senial(self) -> None:
        """
        Obtiene la señal de entrada y la guarda en la lista interna
        """
        print("Lectura de la señal")
        for i in range(self._nro_muestra):
            print(f"Dato nro: {i + 1}")
            self._valores.append(self.__leer_dato_entrada())

    def procesar_senial(self) -> None:
        """
        Procesa la señal de manera que para cada valor adquirido se obtenga el doble del mismo
        """
        if not self._valores:
            raise ValueError("No hay valores para procesar. Ejecute leer_senial() primero.")

        print("Procesando Señal")
        self._valores_procesados = [valor * 2 for valor in self._valores]

    def mostrar_senial(self) -> None:
        """
        Muestra la señal procesada en salida de consola
        """
        if not self._valores_procesados:
            raise ValueError("No hay señal procesada. Ejecute procesar_senial() primero.")

        print("Mostrar la señal")
        print("Señal original:", self._valores)
        print("Señal amplificada (x2):", self._valores_procesados)

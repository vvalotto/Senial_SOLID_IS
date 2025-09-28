#!/usr/bin/env python3
"""
Lanzador principal del sistema que demuestra la aplicación de principios SOLID,
donde las responsabilidades se dividen entre diferentes clases y paquetes.
"""
import platform
import os
from adquisicion_senial import Adquisidor
from procesamiento_senial import Procesador
from presentacion_senial import Visualizador


class Lanzador:
    """
    Programa Lanzador que demuestra la aplicación de principios SOLID
    """

    @staticmethod
    def limpiar_pantalla():
        """
        Limpia la pantalla de manera compatible con diferentes sistemas operativos
        """
        if platform.system() == "Windows":
            os.system("cls")
        else:
            os.system("clear")

    @staticmethod
    def tecla():
        """
        Función que solicita una tecla para continuar
        """
        while True:
            respuesta = input('Presione C para continuar> ').upper().strip()
            if respuesta == "C":
                break
            print("Por favor, presione 'C' para continuar")

    @staticmethod
    def ejecutar():
        """
        Ejecuta el procesamiento de señal usando las clases que implementan principios SOLID.
        Se instancian las clases que participan del procesamiento.
        """
        try:
            # Instanciar las clases que implementan SRP
            adquisidor = Adquisidor(5)
            procesador = Procesador()
            visualizador = Visualizador()

            Lanzador.limpiar_pantalla()
            print("=== DEMOSTRACIÓN PRINCIPIOS SOLID - PROCESAMIENTO DE SEÑALES ===")
            print()

            # Paso 1 - Adquisición de la señal
            print("Inicio - Paso 1 - Adquisición de la señal")
            adquisidor.leer_senial()
            senial_adquirida = adquisidor.obtener_senial_adquirida()
            Lanzador.tecla()

            # Paso 2 - Procesamiento de la señal adquirida
            print("\nInicio - Paso 2 - Procesamiento")
            procesador.procesar_senial(senial_adquirida)
            senial_procesada = procesador.obtener_senial_procesada()
            Lanzador.tecla()

            # Paso 3 - Visualización de la señal procesada
            print("\nInicio - Paso 3 - Mostrar Señal")
            visualizador.mostrar_datos(senial_procesada)

            print("\n=== FIN PROGRAMA - PRINCIPIOS SOLID APLICADOS CORRECTAMENTE ===")

        except KeyboardInterrupt:
            print("\n\nProceso interrumpido por el usuario")
        except Exception as e:
            print(f"\nError durante la ejecución: {e}")


def ejecutar():
    """
    Función de entrada para el comando de consola
    """
    Lanzador.ejecutar()


if __name__ == "__main__":
    ejecutar()
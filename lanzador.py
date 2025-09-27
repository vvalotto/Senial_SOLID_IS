#!/usr/bin/env python3
"""
Programa lanzador del ejemplo - Demostración de violación SRP
"""

from senial_solid.lector_senial import LectorSenial


class Lanzador:
    """
    Programa Principal que demuestra el uso de la clase LectorSenial
    que viola el principio de responsabilidad única (SRP)
    """

    @staticmethod
    def ejecutar() -> None:
        """
        Ejecución del programa lanzador que procesa una señal de 10 muestras

        :return: None
        """
        try:
            senial = LectorSenial(10)

            print("=== PROCESAMIENTO DE SEÑAL - VIOLACIÓN SRP ===")
            print("Paso 1 - Adquiere la señal")
            senial.leer_senial()

            print("\nPaso 2 - Procesa la señal")
            senial.procesar_senial()

            print("\nPaso 3 - Muestra la señal")
            senial.mostrar_senial()

            print("\n=== PROCESAMIENTO COMPLETADO ===")

        except ValueError as e:
            print(f"Error: {e}")
        except KeyboardInterrupt:
            print("\nProceso interrumpido por el usuario")
        except Exception as e:
            print(f"Error inesperado: {e}")


def ejecutar():
    """
    Función de entrada para el comando de consola
    """
    Lanzador.ejecutar()


if __name__ == "__main__":
    ejecutar()

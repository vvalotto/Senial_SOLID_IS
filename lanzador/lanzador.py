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
    def seleccionar_tipo_procesamiento():
        """
        Permite al usuario seleccionar el tipo de procesamiento y sus parámetros.

        Returns:
            tuple: (tipo_procesamiento, parametro, descripcion)
        """
        print("\n" + "="*60)
        print("SELECCIÓN DE TIPO DE PROCESAMIENTO")
        print("="*60)
        print("Opciones disponibles:")
        print("1. Amplificación (multiplica cada valor por un factor)")
        print("2. Filtro por umbral (mantiene valores menores al umbral)")
        print()

        while True:
            try:
                opcion = int(input("Seleccione una opción (1 o 2): "))
                if opcion in [1, 2]:
                    break
                print("❌ Opción inválida. Por favor ingrese 1 o 2.")
            except ValueError:
                print("❌ Por favor ingrese un número válido.")

        if opcion == 1:
            # Procesamiento por amplificación
            print("\n--- Configuración de Amplificación ---")
            while True:
                try:
                    factor = float(input("Ingrese el factor de amplificación (ej: 2.0): "))
                    if factor > 0:
                        break
                    print("❌ El factor debe ser mayor que 0.")
                except ValueError:
                    print("❌ Por favor ingrese un número válido.")

            tipo_procesamiento = "amplificar"
            parametro = factor
            descripcion = f"Amplificación con factor {factor}x"

        else:
            # Procesamiento por umbral
            print("\n--- Configuración de Filtro por Umbral ---")
            print("Nota: Se mantendrán valores menores al umbral, los demás se pondrán en 0")
            while True:
                try:
                    umbral = float(input("Ingrese el valor del umbral: "))
                    break
                except ValueError:
                    print("❌ Por favor ingrese un número válido.")

            tipo_procesamiento = "umbral"
            parametro = umbral
            descripcion = f"Filtro por umbral = {umbral}"

        print(f"✅ Configuración seleccionada: {descripcion}")
        return tipo_procesamiento, parametro, descripcion

    @staticmethod
    def ejecutar():
        """
        Ejecuta el procesamiento de señal usando las clases que implementan principios SOLID.
        Se instancian las clases que participan del procesamiento.
        Permite seleccionar el tipo de procesamiento de manera interactiva.
        """
        try:
            # Instanciar las clases que implementan SRP
            adquisidor = Adquisidor(5)
            procesador = Procesador()
            visualizador = Visualizador()

            Lanzador.limpiar_pantalla()
            print("=== DEMOSTRACIÓN PRINCIPIOS SOLID - PROCESAMIENTO DE SEÑALES v3.0 ===")
            print("Sistema con soporte para múltiples tipos de procesamiento")
            print()

            # Paso 1 - Adquisición de la señal
            print("📡 PASO 1 - ADQUISICIÓN DE LA SEÑAL")
            print("-" * 40)
            adquisidor.leer_senial()
            senial_adquirida = adquisidor.obtener_senial_adquirida()

            print(f"\n✅ Señal adquirida con {senial_adquirida.obtener_tamanio()} muestras")
            Lanzador.tecla()

            # Selección de tipo de procesamiento
            tipo_procesamiento, parametro, descripcion = Lanzador.seleccionar_tipo_procesamiento()
            Lanzador.tecla()

            # Paso 2 - Procesamiento de la señal adquirida
            print(f"\n⚙️  PASO 2 - PROCESAMIENTO: {descripcion.upper()}")
            print("-" * 40)
            print(f"Aplicando procesamiento tipo '{tipo_procesamiento}' con parámetro {parametro}")

            procesador.procesar_senial(senial_adquirida, tipo_procesamiento, parametro)
            senial_procesada = procesador.obtener_senial_procesada()

            print("✅ Procesamiento completado")
            Lanzador.tecla()

            # Paso 3 - Visualización de la señal procesada
            print("\n📊 PASO 3 - VISUALIZACIÓN DE RESULTADOS")
            print("-" * 40)
            print("Comparación entre señal original y procesada:")
            print()

            # Mostrar señal original
            print("🔹 SEÑAL ORIGINAL:")
            visualizador.mostrar_datos(senial_adquirida)
            print()

            # Mostrar señal procesada
            print(f"🔸 SEÑAL PROCESADA ({descripcion}):")
            visualizador.mostrar_datos(senial_procesada)

            print(f"\n🎉 PROCESAMIENTO COMPLETADO EXITOSAMENTE")
            print("="*60)
            print("✅ Principios SOLID aplicados:")
            print("   • SRP: Cada clase tiene una responsabilidad única")
            print(f"   • OCP: Procesador extensible con nuevos tipos (actual: {tipo_procesamiento})")
            print("   • Sistema modular y mantenible")
            print("="*60)

        except KeyboardInterrupt:
            print("\n\n⚠️  Proceso interrumpido por el usuario")
        except Exception as e:
            print(f"\n❌ Error durante la ejecución: {e}")
            print("   Verifique que todos los componentes estén correctamente instalados")


def ejecutar():
    """
    Función de entrada para el comando de consola
    """
    Lanzador.ejecutar()


if __name__ == "__main__":
    ejecutar()
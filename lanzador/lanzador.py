#!/usr/bin/env python3
"""
Lanzador principal del sistema que demuestra la aplicación de principios SOLID,
donde las responsabilidades se dividen entre diferentes clases y paquetes.
"""
import platform
import os
from adquisicion_senial import Adquisidor
from procesamiento_senial import Procesador, ProcesadorUmbral  # ⚠️ DEPENDENCIAS MÚLTIPLES
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
            # Instanciar componentes base
            adquisidor = Adquisidor(5)
            visualizador = Visualizador()

            Lanzador.limpiar_pantalla()
            print("=== DEMOSTRACIÓN OCP 'TÉCNICO' - PROCESAMIENTO DE SEÑALES v3.0 ===")
            print("Sistema que cumple OCP localmente pero crea problemas de dependencias")
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

            # ⚠️ PROBLEMA DE DEPENDENCIAS: Lanzador debe conocer clases concretas
            print(f"\n⚙️  PASO 2 - PROCESAMIENTO: {descripcion.upper()}")
            print("-" * 40)
            print("⚠️  NOTA: Observe cómo el Lanzador debe elegir entre clases concretas...")

            # ❌ LÓGICA CONDICIONAL EN LANZADOR (problema de dependencias)
            if tipo_procesamiento == "amplificar":
                print("Usando clase Procesador original (sin modificar - cumple OCP)")
                procesador = Procesador()  # Clase original, constructor sin parámetros
                procesador.procesar_senial(senial_adquirida)  # Interfaz original

            elif tipo_procesamiento == "umbral":
                print(f"Usando nueva clase ProcesadorUmbral (extensión - cumple OCP)")
                procesador = ProcesadorUmbral(parametro)  # ⚠️ Interfaz inconsistente
                procesador.procesar_senial(senial_adquirida)  # Misma interfaz externa

            else:
                raise ValueError(f"Tipo '{tipo_procesamiento}' no soportado")

            senial_procesada = procesador.obtener_senial_procesada()
            print("✅ Procesamiento completado")
            print("⚠️  PROBLEMA: Lanzador acoplado a clases concretas")
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

            print(f"\n🎉 DEMOSTRACIÓN COMPLETADA")
            print("="*70)
            print("✅ OCP 'TÉCNICAMENTE' CUMPLIDO:")
            print("   • Procesador original NO modificado")
            print("   • Nueva funcionalidad agregada via ProcesadorUmbral")
            print("   • Código existente preservado")
            print()
            print("⚠️  PERO PROBLEMAS CREADOS:")
            print("   ❌ Lanzador acoplado a clases concretas")
            print("   ❌ Interfaces inconsistentes (constructores diferentes)")
            print("   ❌ Lógica condicional movida a capa superior")
            print("   ❌ Violación de DIP (dependencias hacia concreciones)")
            print("   ❌ Escalabilidad comprometida")
            print()
            print("📚 LECCIÓN: Cumplir OCP localmente puede crear problemas globales")
            print("🎯 PRÓXIMO PASO: Aplicar OCP correctamente con abstracciones")
            print("="*70)

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
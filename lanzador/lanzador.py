#!/usr/bin/env python3
"""
Lanzador principal del sistema que demuestra la aplicación de principios SOLID,
donde las responsabilidades se dividen entre diferentes clases y paquetes.
"""
import platform
import os
from adquisicion_senial import Adquisidor
from procesamiento_senial import BaseProcesador, ProcesadorAmplificador, ProcesadorConUmbral
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
    def crear_procesador(tipo_procesamiento, parametro) -> BaseProcesador:
        """
        Factory method para crear procesadores usando polimorfismo.

        ✅ CUMPLE OCP: Nuevos tipos se agregan aquí sin modificar código existente
        ✅ CUMPLE DIP: Retorna abstracción BaseProcesador, no concreción específica

        :param tipo_procesamiento: Tipo de procesador a crear
        :param parametro: Parámetro específico del procesador
        :return: Instancia de BaseProcesador (polimorfismo)
        """
        if tipo_procesamiento == "amplificar":
            return ProcesadorAmplificador(parametro)
        elif tipo_procesamiento == "umbral":
            return ProcesadorConUmbral(parametro)
        else:
            raise ValueError(f"Tipo de procesamiento '{tipo_procesamiento}' no soportado")

    @staticmethod
    def procesar_con_polimorfismo(procesador: BaseProcesador, senial):
        """
        Método que demuestra polimorfismo - funciona con cualquier implementación
        de BaseProcesador sin conocer el tipo específico.

        ✅ CUMPLE OCP: Extensible para nuevos tipos sin modificación
        ✅ CUMPLE LSP: Cualquier implementación de BaseProcesador es intercambiable

        :param procesador: Cualquier implementación de BaseProcesador
        :param senial: Señal a procesar
        :return: Señal procesada
        """
        procesador.procesar(senial)
        return procesador.obtener_senial_procesada()

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
            print("=== DEMOSTRACIÓN OCP CORRECTO - PROCESAMIENTO DE SEÑALES v3.0 ===")
            print("Sistema que cumple OCP usando abstracciones y polimorfismo")
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

            # ✅ SOLUCIÓN OCP: Uso de Factory Pattern + Polimorfismo
            print(f"\n⚙️  PASO 2 - PROCESAMIENTO: {descripcion.upper()}")
            print("-" * 40)
            print("✅ NOTA: Lanzador usa abstracción - no conoce implementaciones específicas")

            # ✅ FACTORY PATTERN: Crea procesador usando abstracción
            print(f"Creando procesador tipo '{tipo_procesamiento}' con parámetro {parametro}")
            procesador = Lanzador.crear_procesador(tipo_procesamiento, parametro)
            print(f"✅ Procesador creado: {type(procesador).__name__}")

            # ✅ POLIMORFISMO: Funciona con cualquier implementación de BaseProcesador
            print("Aplicando procesamiento usando polimorfismo...")
            senial_procesada = Lanzador.procesar_con_polimorfismo(procesador, senial_adquirida)

            print("✅ Procesamiento completado usando abstracción")
            print("✅ BENEFICIO: Lanzador NO acoplado a implementaciones específicas")
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

            print(f"\n🎉 DEMOSTRACIÓN OCP CORRECTA COMPLETADA")
            print("="*75)
            print("✅ PRINCIPIOS SOLID APLICADOS CORRECTAMENTE:")
            print("   • SRP: Cada clase tiene responsabilidad única")
            print("   • OCP: Sistema extensible sin modificar código existente")
            print("   • LSP: Implementaciones intercambiables polimórficamente")
            print("   • DIP: Dependencias hacia abstracciones (BaseProcesador)")
            print()
            print("🏗️  PATRONES ARQUITECTÓNICOS APLICADOS:")
            print("   ✅ Abstract Factory: BaseProcesador como contrato")
            print("   ✅ Strategy Pattern: Diferentes algoritmos intercambiables")
            print("   ✅ Factory Method: crear_procesador() centraliza creación")
            print("   ✅ Polimorfismo: procesar_con_polimorfismo() genérico")
            print()
            print("🚀 EXTENSIBILIDAD DEMOSTRADA:")
            print("   • Agregar nuevos tipos: Solo implementar BaseProcesador")
            print("   • Sin modificar código existente: Factory absorbe cambios")
            print("   • Interfaces consistentes: Todas heredan de BaseProcesador")
            print("   • Testabilidad mejorada: Fácil mock de BaseProcesador")
            print()
            print("📚 LECCIÓN: OCP correctamente aplicado con abstracciones")
            print("🎯 RESULTADO: Arquitectura escalable y mantenible")
            print("="*75)

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
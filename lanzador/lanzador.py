#!/usr/bin/env python3
"""
Lanzador principal del sistema que demuestra SRP PURO aplicado.

Este módulo implementa el patrón COORDINADOR que aplica SRP estrictamente,
separando ORQUESTACIÓN de CONFIGURACIÓN completamente.

📚 DOCUMENTACIÓN TÉCNICA:
- SRP aplicado: docs/IMPLEMETACION DE SRP EN PAQUETES.md
- OCP mantenido: docs/IMPLEMENTACION DE OCP CON ABSTRACCIONES.md

🎯 RESPONSABILIDAD ÚNICA: ORQUESTACIÓN
- SOLO coordina la ejecución entre componentes ya configurados
- NO toma decisiones de configuración (delegadas al Configurador)
- NO interactúa con usuario para configuración
- NO contiene lógica de negocio

🏗️ PATRÓN IMPLEMENTADO:
Coordinador/Orquestador que usa Factory Centralizado para obtener
componentes pre-configurados y ejecuta el flujo de procesamiento.

Versión: 5.0 - SRP Puro con responsabilidades cristalinas
Autor: Victor Valotto
"""
import platform
import os
from configurador import Configurador


class Lanzador:
    """
    Lanzador que aplica SRP PURO - Responsabilidad única: ORQUESTACIÓN

    📖 PATRÓN COORDINADOR:
    El Lanzador coordina la ejecución del flujo de procesamiento aplicando
    separación estricta de responsabilidades.

    📚 REFERENCIAS TEÓRICAS:
    - docs/IMPLEMETACION DE SRP EN PAQUETES.md: Evolución de responsabilidades
    - docs/IMPLEMENTACION DE OCP CON ABSTRACCIONES.md: Uso de polimorfismo

    ✅ LO QUE SÍ HACE (SRP):
    - Orquestar flujo: Adquisición → Procesamiento → Visualización
    - Coordinar interacción entre componentes
    - Mostrar progreso y resultados del procesamiento

    ❌ LO QUE NO HACE (SRP):
    - Decidir QUÉ adquisidor usar (→ Configurador)
    - Decidir QUÉ procesador usar (→ Configurador)
    - Contener lógica de negocio (→ Componentes específicos)
    - Interactuar con usuario para configuración (→ Configurador)

    🔄 BENEFICIO SRP:
    Cambios en configuración NO afectan al Lanzador.
    Cambios en lógica de procesamiento NO afectan al Lanzador.
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
        🚀 MÉTODO PRINCIPAL - Orquesta el flujo completo aplicando SRP puro.

        📖 RESPONSABILIDAD ÚNICA:
        Coordinar la interacción entre componentes sin tomar decisiones
        de configuración (delegadas al Configurador).

        📚 REFERENCIA ARQUITECTÓNICA:
        docs/IMPLEMETACION DE SRP EN PAQUETES.md - Sección "Factory Centralizado"
        Demuestra separación total entre orquestación y configuración.

        🔄 FLUJO ORQUESTADO:
        1. Obtener componentes configurados (SIN decidir cuáles)
        2. Ejecutar adquisición de datos
        3. Ejecutar procesamiento de señal
        4. Ejecutar visualización de resultados
        5. Mostrar resumen de principios aplicados

        ✅ SRP DEMOSTRADO:
        Este método NO cambia cuando:
        - Se agrega nuevo tipo de adquisidor
        - Se agrega nuevo tipo de procesador
        - Se cambia configuración de componentes
        """
        try:
            # ✅ SRP PURO: Solo obtener componentes configurados (sin decidir cuáles)
            # 📚 Ver docs/IMPLEMETACION DE SRP EN PAQUETES.md - Delegación al Configurador
            adquisidor = Configurador.crear_adquisidor()    # Decisión "de fábrica"
            procesador = Configurador.crear_procesador()    # Sin consultar usuario
            visualizador = Configurador.crear_visualizador()  # Configuración centralizada

            Lanzador.limpiar_pantalla()
            print("=== DEMOSTRACIÓN SRP PURO - PROCESAMIENTO DE SEÑALES v5.0 ===")
            print("Lanzador con responsabilidad única: ORQUESTACIÓN")
            print("Configurador con responsabilidad única: CREACIÓN")
            print()

            # ✅ ORQUESTACIÓN: Paso 1 - Adquisición
            print("📡 PASO 1 - ADQUISICIÓN DE LA SEÑAL")
            print("-" * 40)
            adquisidor.leer_senial()
            senial_original = adquisidor.obtener_senial_adquirida()
            print(f"✅ Señal adquirida con {senial_original.obtener_tamanio()} muestras")
            Lanzador.tecla()

            # ✅ ORQUESTACIÓN: Paso 2 - Procesamiento
            print(f"\n⚙️  PASO 2 - PROCESAMIENTO")
            print("-" * 40)
            print(f"✅ Procesador configurado: {type(procesador).__name__}")
            print("✅ Configuración decidida por el Configurador (SRP)")

            # ✅ USO DIRECTO: Sin wrapper innecesario - Polimorfismo puro
            # 📚 Ver docs/IMPLEMENTACION DE OCP CON ABSTRACCIONES.md - Polimorfismo
            procesador.procesar(senial_original)  # Funciona con cualquier procesador
            senial_procesada = procesador.obtener_senial_procesada()

            print("✅ Procesamiento completado")
            Lanzador.tecla()

            # ✅ ORQUESTACIÓN: Paso 3 - Visualización
            print("\n📊 PASO 3 - VISUALIZACIÓN DE RESULTADOS")
            print("-" * 40)
            print("Comparación entre señal original y procesada:")
            print()

            print("🔹 SEÑAL ORIGINAL:")
            visualizador.mostrar_datos(senial_original)
            print()

            print("🔸 SEÑAL PROCESADA:")
            visualizador.mostrar_datos(senial_procesada)

            # ✅ RESULTADO: SRP aplicado correctamente
            print(f"\n🎉 DEMOSTRACIÓN SRP PURO COMPLETADA")
            print("="*60)
            print("✅ RESPONSABILIDADES PERFECTAMENTE SEPARADAS:")
            print("   • Lanzador: SOLO orquestar el flujo de procesamiento")
            print("   • Configurador: SOLO crear y configurar objetos")
            print("   • Adquisidor: SOLO capturar datos de entrada")
            print("   • Procesador: SOLO transformar señales")
            print("   • Visualizador: SOLO mostrar resultados")
            print()
            print("🏗️  PRINCIPIOS SOLID DEMOSTRADOS:")
            print("   ✅ SRP: Una responsabilidad por clase/paquete")
            print("   ✅ OCP: Procesadores extensibles sin modificar lanzador")
            print("   ✅ LSP: Cualquier procesador funciona polimórficamente")
            print("   ✅ Preparado para DIP: Configurador listo para inyección")
            print()
            print("📚 LECCIÓN APRENDIDA:")
            print("   🎯 SEPARACIÓN TOTAL de responsabilidades")
            print("   🎯 CONFIGURACIÓN CENTRALIZADA sin input del usuario")
            print("   🎯 ORQUESTACIÓN PURA sin lógica de negocio")
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

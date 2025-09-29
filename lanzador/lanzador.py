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
        🚀 METODO PRINCIPAL - Orquesta el flujo completo aplicando SRP puro.

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
        Este metodo NO cambia cuando:
        - Se agrega nuevo tipo de adquisidor
        - Se agrega nuevo tipo de procesador
        - Se cambia configuración de componentes
        """
        try:
            # ✅ SRP PURO: Solo obtener componentes configurados (sin decidir cuáles)
            # 📚 Ver docs/IMPLEMETACION DE SRP EN PAQUETES.md - Delegación al Configurador
            adquisidor = Configurador.crear_adquisidor()    # Con señal inyectada
            procesador = Configurador.crear_procesador()    # Con señal inyectada
            visualizador = Configurador.crear_visualizador()  # Configuración centralizada

            # 🔄 INFORMACIÓN DIAGNÓSTICA: Verificar tipo de señal inyectado
            # Usamos métodos de acceso para respetar encapsulación
            senial_adquisidor = adquisidor.obtener_senial_adquirida()
            senial_procesador = procesador.obtener_senial_procesada()
            tipo_senial_adquisidor = type(senial_adquisidor).__name__
            tipo_senial_procesador = type(senial_procesador).__name__

            Lanzador.limpiar_pantalla()
            print("=== DEMOSTRACIÓN SRP PURO - PROCESAMIENTO DE SEÑALES v5.0 ===")
            print("Lanzador con responsabilidad única: ORQUESTACIÓN")
            print("Configurador con responsabilidad única: CREACIÓN + INYECCIÓN")
            print()
            print("🔄 INYECCIÓN DE DEPENDENCIAS INDEPENDIENTE:")
            print(f"   • Adquisidor configurado con señal: {tipo_senial_adquisidor}")
            print(f"   • Procesador configurado con señal: {tipo_senial_procesador}")

            # 🧪 ANÁLISIS DE CONFIGURACIÓN (experimentos LSP)
            if tipo_senial_adquisidor != tipo_senial_procesador:
                print("   🧪 CONFIGURACIÓN MIXTA detectada:")
                print(f"      - Adquisición: {tipo_senial_adquisidor}")
                print(f"      - Procesamiento: {tipo_senial_procesador}")
                print("   🎓 Experimento LSP avanzado: Tipos diferentes por fase")
            else:
                print(f"   ✅ Configuración homogénea: {tipo_senial_adquisidor} en todo el sistema")
            print()

            # ✅ ORQUESTACIÓN: Paso 1 - Adquisición en señal configurada
            print("📡 PASO 1 - ADQUISICIÓN DE LA SEÑAL")
            print("-" * 40)
            print(f"📋 Señal inyectada en adquisidor: {tipo_senial_adquisidor}")

            # 🔄 POLIMORFISMO: El adquisidor trabaja con señal inyectada automáticamente
            # Sin que el lanzador conozca el tipo específico - SRP puro
            adquisidor.leer_senial()
            senial_original = adquisidor.obtener_senial_adquirida()

            print(f"✅ Señal adquirida con {senial_original.obtener_tamanio()} muestras")
            print(f"📊 Estructura confirmada: {type(senial_original).__name__}")

            # 🧪 DIAGNÓSTICO LSP: Verificar comportamiento específico si existe
            if hasattr(senial_original, 'sacar_valor'):
                print(f"🔍 Método específico detectado: sacar_valor() disponible")
                print(f"⚠️ Nota: Esto puede indicar violación LSP (método no polimórfico)")

            Lanzador.tecla()

            # ✅ ORQUESTACIÓN: Paso 2 - Procesamiento
            print(f"\n⚙️  PASO 2 - PROCESAMIENTO")
            print("-" * 40)
            print(f"✅ Procesador configurado: {type(procesador).__name__}")
            print(f"📋 Señal inyectada en procesador: {tipo_senial_procesador}")

            # ✅ USO DIRECTO: Sin wrapper innecesario - Polimorfismo puro
            # 📚 Ver docs/IMPLEMENTACION DE OCP CON ABSTRACCIONES.md - Polimorfismo
            procesador.procesar(senial_original)  # Funciona con cualquier procesador
            senial_procesada = procesador.obtener_senial_procesada()

            print("✅ Procesamiento completado")
            print(f"📊 Señal procesada mantiene estructura: {type(senial_procesada).__name__}")

            # 🧪 VERIFICACIÓN DE CONSISTENCIA: Tipos deben coincidir
            if type(senial_original).__name__ != type(senial_procesada).__name__:
                print("⚠️ INCONSISTENCIA DETECTADA: Tipos de señal diferentes")
                print(f"   Original: {type(senial_original).__name__}")
                print(f"   Procesada: {type(senial_procesada).__name__}")
                print("🎓 Esto puede indicar problemas en la implementación LSP")
            else:
                print(f"✅ Consistencia mantenida: {type(senial_original).__name__}")

            Lanzador.tecla()

            # ✅ ORQUESTACIÓN: Paso 3 - Visualización
            print("\n📊 PASO 3 - VISUALIZACIÓN DE RESULTADOS")
            print("-" * 40)
            print("Comparación entre señal original y procesada:")
            print(f"📋 Ambas señales con estructura: {type(senial_original).__name__}")
            print(f"🔄 Inyectadas automáticamente por el Configurador")
            print()

            print("🔹 SEÑAL ORIGINAL:")
            visualizador.mostrar_datos(senial_original)
            print()

            print("🔸 SEÑAL PROCESADA:")
            visualizador.mostrar_datos(senial_procesada)

            # 🧪 DEMOSTRACIÓN EXPERIMENTAL LSP (si hay métodos específicos)
            if hasattr(senial_original, 'sacar_valor') and hasattr(senial_procesada, 'sacar_valor'):
                print("\n🧪 DEMOSTRACIÓN EXPERIMENTAL - MÉTODOS ESPECÍFICOS:")
                print("⚠️ Nota: Estos métodos NO están en la clase base Senial")
                print("🎓 Su uso indica potencial violación de LSP")

                # Determinar tipo de comportamiento esperado
                if 'Pila' in type(senial_original).__name__:
                    print("📋 Comportamiento esperado: LIFO (Last In, First Out)")
                elif 'Cola' in type(senial_original).__name__:
                    print("📋 Comportamiento esperado: FIFO (First In, First Out)")

                try:
                    if senial_original.obtener_tamanio() > 0:
                        valor_original = senial_original.sacar_valor()
                        print(f"🔹 Valor extraído de señal original: {valor_original}")

                    if senial_procesada.obtener_tamanio() > 0:
                        valor_procesado = senial_procesada.sacar_valor()
                        print(f"🔸 Valor extraído de señal procesada: {valor_procesado}")

                        # Comparar comportamientos si hay datos suficientes
                        if senial_original.obtener_tamanio() > 0 and 'valor_original' in locals():
                            if valor_original == valor_procesado:
                                print("✅ Comportamiento consistente entre señales")
                            else:
                                print("⚠️ Comportamiento diferente - posible efecto del procesamiento")

                except Exception as e:
                    print(f"❌ Error al usar método específico: {e}")
                    print("🎓 Esto demuestra violación LSP: método no funciona polimórficamente")

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
            print("   🔄 LSP: Tipos de señal en evaluación (posibles violaciones)")
            print("   ✅ Preparado para DIP: Configurador listo para inyección")
            print()
            print("📚 LECCIÓN APRENDIDA:")
            print("   🎯 SEPARACIÓN TOTAL de responsabilidades")
            print("   🎯 CONFIGURACIÓN CENTRALIZADA sin input del usuario")
            print("   🎯 ORQUESTACIÓN PURA sin lógica de negocio")
            print("   🎯 TIPOS DE SEÑAL intercambiables (sujeto a LSP)")
            print("="*60)

            print("\n🧪 PARA EXPERIMENTAR CON LSP:")
            print("   EXPERIMENTOS INDEPENDIENTES:")
            print("   A) Modificar Configurador.crear_senial_adquisidor():")
            print("      • crear_senial_lista()  ← Comportamiento baseline (ACTUAL)")
            print("      • crear_senial_pila()   ← Adquisición con LIFO")
            print("      • crear_senial_cola()   ← Adquisición con FIFO")
            print()
            print("   B) Modificar Configurador.crear_senial_procesador():")
            print("      • crear_senial_lista()  ← Procesamiento baseline (ACTUAL)")
            print("      • crear_senial_pila()   ← Procesamiento con LIFO")
            print("      • crear_senial_cola()   ← Procesamiento con FIFO")
            print()
            print("   🎯 EXPERIMENTOS MIXTOS AVANZADOS:")
            print("      • Adquisidor=Lista + Procesador=Pila  ← Transferencia problemática")
            print("      • Adquisidor=Cola + Procesador=Lista  ← Inversión semántica")
            print("      • Adquisidor=Pila + Procesador=Cola   ← Semánticas opuestas")
            print()
            print("📚 DOCUMENTACIÓN COMPLETA:")
            print("   📄 docs/VIOLACIONES DE LSP EN TIPOS DE SEÑAL.md")
            print("   📄 docs/IMPLEMENTACION DE OCP CON ABSTRACCIONES.md")
            print("   📄 docs/INCORPORACION DEL CONFIGURADOR CON FACTORY PATTERN.md")

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

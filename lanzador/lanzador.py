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

Versión: 5.2 - SRP + Patrón Repository con DIP
Autor: Victor Valotto
"""
import platform
import os
from datetime import datetime
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
        2. Obtener repositorios configurados (patrón Repository + DIP)
        3. Ejecutar adquisición de datos → Guardar en repositorio
        4. Ejecutar procesamiento de señal → Guardar en repositorio
        5. Recuperar señales desde repositorios (abstracción de dominio)
        6. Ejecutar visualización de señales recuperadas
        7. Mostrar resumen de principios aplicados

        ✅ SRP DEMOSTRADO:
        Este metodo NO cambia cuando:
        - Se agrega nuevo tipo de adquisidor
        - Se agrega nuevo tipo de procesador
        - Se cambia configuración de componentes
        - Se cambia estrategia de persistencia (Pickle ↔ Archivo)

        🎯 PATRÓN REPOSITORY APLICADO:
        - Repositorio abstrae la persistencia del dominio
        - Contexto se inyecta en repositorio (DIP)
        - API semántica: guardar() / obtener()
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

            # 💾 Obtener repositorios configurados (SRP + DIP - delegado al Configurador)
            repo_adquisicion = Configurador.crear_repositorio_adquisicion()
            repo_procesamiento = Configurador.crear_repositorio_procesamiento()

            Lanzador.limpiar_pantalla()
            print("=== DEMOSTRACIÓN SRP + REPOSITORY PATTERN - PROCESAMIENTO DE SEÑALES v5.2 ===")
            print("Lanzador con responsabilidad única: ORQUESTACIÓN")
            print("Configurador con responsabilidad única: CREACIÓN + INYECCIÓN + COMPOSICIÓN")
            print()
            print("🔄 INYECCIÓN DE DEPENDENCIAS INDEPENDIENTE:")
            print(f"   • Adquisidor configurado con señal: {tipo_senial_adquisidor}")
            print(f"   • Procesador configurado con señal: {tipo_senial_procesador}")

            # ✅ ORQUESTACIÓN: Paso 1 - Adquisición en señal configurada
            print("📡 PASO 1 - ADQUISICIÓN DE LA SEÑAL")
            print("-" * 40)
            print(f"📋 Señal inyectada en adquisidor: {tipo_senial_adquisidor}")

            # 🔄 POLIMORFISMO: El adquisidor trabaja con señal inyectada automáticamente
            # Sin que el lanzador conozca el tipo específico - SRP puro
            adquisidor.leer_senial()
            senial_original = adquisidor.obtener_senial_adquirida()

            # 💾 Agregar metadatos para persistencia
            senial_original.fecha_adquisicion = datetime.now().date()
            senial_original.comentario = input('Descripcion de la señal: ')
            senial_original.id = int(input('Identificacion (nro entero): '))
            print(f'Fecha de lectura: {senial_original.fecha_adquisicion}')
            print(f'Cantidad de valores obtenidos: {senial_original.cantidad}')

            print(f'\n✅ Señal adquirida con {senial_original.obtener_tamanio()} muestras')
            print(f"📊 Estructura confirmada: {type(senial_original).__name__}")

            Lanzador.tecla()
            print('\n💾 PASO 1.1 - Guardando señal en repositorio...')
            repo_adquisicion.guardar(senial_original)
            print(f'✅ Señal persistida con ID: {senial_original.id}')
            print(f'   📁 Repositorio: ./datos_persistidos/adquisicion/')
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

            # 💾 Agregar metadatos para persistencia
            senial_procesada.comentario = input('\nDescripción de la señal procesada: ')
            senial_procesada.id = int(input('Identificación (nro entero): '))

            print("\n✅ Procesamiento completado")
            print(f"📊 Señal procesada mantiene estructura: {type(senial_procesada).__name__}")

            print('\n💾 PASO 2.1 - Guardando señal procesada en repositorio...')
            repo_procesamiento.guardar(senial_procesada)
            print(f'✅ Señal procesada persistida con ID: {senial_procesada.id}')
            print(f'   📁 Repositorio: ./datos_persistidos/procesamiento/')
            Lanzador.tecla()

            # ✅ ORQUESTACIÓN: Paso 3 - Recuperación desde repositorios
            print("\n💾 PASO 3 - RECUPERACIÓN DESDE REPOSITORIOS")
            print("-" * 40)
            print("🎯 PATRÓN REPOSITORY: Acceso a datos a través de abstracción de dominio")
            print()

            # Recuperar señal adquirida desde repositorio
            print(f"🔹 Recuperando señal adquirida (ID: {senial_original.id})...")
            senial_original_recuperada = repo_adquisicion.obtener(str(senial_original.id))
            if senial_original_recuperada:
                print(f"   ✓ Señal recuperada desde repositorio de adquisición")
                print(f"   ✓ Tipo: {type(senial_original_recuperada).__name__}")
                print(f"   ✓ Comentario: {senial_original_recuperada.comentario}")
                print(f"   ✓ Formato: Archivo de texto plano (.dat)")
            else:
                print("   ✗ Error al recuperar señal adquirida")
                senial_original_recuperada = senial_original  # Fallback

            # Recuperar señal procesada desde repositorio
            print(f"\n🔸 Recuperando señal procesada (ID: {senial_procesada.id})...")
            senial_procesada_recuperada = repo_procesamiento.obtener(str(senial_procesada.id))
            if senial_procesada_recuperada:
                print(f"   ✓ Señal recuperada desde repositorio de procesamiento")
                print(f"   ✓ Tipo: {type(senial_procesada_recuperada).__name__}")
                print(f"   ✓ Comentario: {senial_procesada_recuperada.comentario}")
                print(f"   ✓ Formato: Pickle binario (.pickle)")
            else:
                print("   ✗ Error al recuperar señal procesada")
                senial_procesada_recuperada = senial_procesada  # Fallback

            Lanzador.tecla()

            # ✅ ORQUESTACIÓN: Paso 4 - Visualización de señales recuperadas
            print("\n📊 PASO 4 - VISUALIZACIÓN DE RESULTADOS")
            print("-" * 40)
            print("⚠️ IMPORTANTE: Visualizando señales RECUPERADAS desde archivos persistidos")
            print(f"📋 Señal original: {type(senial_original_recuperada).__name__}")
            print(f"📋 Señal procesada: {type(senial_procesada_recuperada).__name__}")
            print()

            print("🔹 SEÑAL ORIGINAL (recuperada desde archivo):")
            visualizador.mostrar_datos(senial_original_recuperada)
            print()

            print("🔸 SEÑAL PROCESADA (recuperada desde archivo):")
            visualizador.mostrar_datos(senial_procesada_recuperada)

            # ✅ RESULTADO: Patrón Repository + SOLID aplicados correctamente
            print(f"\n🎉 DEMOSTRACIÓN PATRÓN REPOSITORY + SOLID COMPLETADA")
            print("="*60)
            print("✅ RESPONSABILIDADES PERFECTAMENTE SEPARADAS:")
            print("   • Lanzador: SOLO orquestar el flujo de procesamiento")
            print("   • Configurador: SOLO crear y configurar objetos + composición")
            print("   • Repositorio: SOLO gestionar persistencia de entidades (dominio)")
            print("   • Contexto: SOLO implementar estrategia de almacenamiento (infra)")
            print("   • Adquisidor: SOLO capturar datos de entrada")
            print("   • Procesador: SOLO transformar señales")
            print("   • Visualizador: SOLO mostrar resultados")
            print()
            print("🏗️  PRINCIPIOS SOLID DEMOSTRADOS:")
            print("   ✅ SRP: Una responsabilidad por clase/paquete")
            print("   ✅ OCP: Procesadores y contextos extensibles sin modificar lanzador")
            print("   ✅ LSP: Tipos de señal intercambiables (SenialBase aplicado)")
            print("   ⚠️ ISP: Contextos con interfaz 'gorda' (persistir + recuperar)")
            print("   ✅ DIP: Repositorio depende de abstracción BaseContexto (inyección)")
            print()
            print("🎯 PATRÓN REPOSITORY APLICADO:")
            print("   • Separación dominio (Repositorio) / infraestructura (Contexto)")
            print("   • API semántica: guardar() / obtener() en lugar de persistir() / recuperar()")
            print("   • Inyección de dependencias: Repositorio(contexto)")
            print("   • Estrategias intercambiables: ContextoPickle / ContextoArchivo")
            print()
            print("📚 LECCIÓN APRENDIDA:")
            print("   🎯 SEPARACIÓN TOTAL de responsabilidades (SRP)")
            print("   🎯 INYECCIÓN DE DEPENDENCIAS explícita (DIP)")
            print("   🎯 CONFIGURACIÓN CENTRALIZADA sin input del usuario")
            print("   🎯 ORQUESTACIÓN PURA sin lógica de negocio")
            print("   🎯 PATRÓN REPOSITORY para abstracción de persistencia")
            print("="*60)

            print()
            print("📚 DOCUMENTACIÓN COMPLETA:")
            print("   📄 docs/PATRON REPOSITORY EN PERSISTENCIA.md")
            print("   📄 docs/VIOLACIONES DE LSP EN TIPOS DE SEÑAL.md")
            print("   📄 docs/SOLUCION LSP CON ABSTRACCIONES.md")
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

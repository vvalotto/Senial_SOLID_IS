#!/usr/bin/env python3
"""
Lanzador principal del sistema que demuestra SRP PURO + DIP COMPLETO aplicado.

Este módulo implementa el patrón COORDINADOR que aplica SRP estrictamente,
separando ORQUESTACIÓN de CONFIGURACIÓN completamente.

🎯 RESPONSABILIDAD ÚNICA: ORQUESTACIÓN
- SOLO coordina la ejecución entre componentes ya configurados
- NO toma decisiones de configuración (delegadas al Configurador + JSON)
- NO interactúa con usuario para configuración
- NO contiene lógica de negocio

🏗️ PATRÓN IMPLEMENTADO:
Coordinador/Orquestador que usa Factory Centralizado con configuración
externa (JSON) para obtener componentes pre-configurados.

🔄 DIP APLICADO:
Todas las dependencias se determinan desde config.json - el lanzador
ni siquiera conoce qué tipos concretos se usan.

Versión: 6.0.0 - SRP + DIP Completo con Configuración Externa JSON
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
        🚀 METODO PRINCIPAL - Orquesta el flujo completo aplicando SRP puro + DIP completo.

        📖 RESPONSABILIDAD ÚNICA:
        Coordinar la interacción entre componentes sin tomar decisiones
        de configuración (delegadas al Configurador + config.json).

        📚 REFERENCIA ARQUITECTÓNICA:
        - docs/IMPLEMETACION DE SRP EN PAQUETES.md - SRP en Factory Centralizado
        - docs/APLICACION_DIP_CONFIGURACION_EXTERNA.md - DIP con JSON

        🔄 FLUJO ORQUESTADO:
        0. Inicializar configuración externa (config.json) ← NUEVO v6.0.0
        1. Obtener componentes configurados (SIN decidir cuáles)
        2. Obtener repositorios configurados (patrón Repository + DIP)
        3. Ejecutar adquisición de datos → Guardar en repositorio
        4. Ejecutar procesamiento de señal → Guardar en repositorio
        5. Recuperar señales desde repositorios (abstracción de dominio)
        6. Ejecutar visualización de señales recuperadas
        7. Mostrar resumen de principios aplicados

        ✅ SRP + DIP DEMOSTRADO:
        Este metodo NO cambia cuando:
        - Se cambia tipo de señal en JSON (lista/pila/cola)
        - Se cambia tipo de adquisidor en JSON (consola/archivo/senoidal)
        - Se cambia tipo de procesador en JSON (amplificador/umbral)
        - Se cambia estrategia de persistencia en JSON (pickle/archivo)
        - Se cambian parámetros en JSON (tamaños, umbrales, factores)

        🎯 DIP COMPLETO:
        - Configuración externa determina TODAS las dependencias
        - Lanzador NO conoce tipos concretos
        - Solo conoce abstracciones y métodos del Configurador

        🎯 PATRÓN REPOSITORY APLICADO:
        - Repositorio abstrae la persistencia del dominio
        - Contexto se inyecta en repositorio (DIP)
        - API semántica: guardar() / obtener()
        """
        try:
            # 🎯 DIP - PASO 0: Inicializar configuración externa (JSON)
            print("\n" + "="*70)
            print("🔧 INICIALIZANDO CONFIGURACIÓN EXTERNA")
            print("="*70)
            try:
                # No se pasa ruta - usa config.json en directorio del módulo configurador
                # Funciona independientemente de desde dónde se ejecute el lanzador
                Configurador.inicializar_configuracion()
                print("📋 Configuración cargada exitosamente desde config.json")
                print("✅ Todas las dependencias determinadas externamente (DIP)")
            except FileNotFoundError:
                print("⚠️  config.json no encontrado - usando configuración por defecto")
            print()

            # ✅ SRP PURO: Solo obtener componentes configurados (sin decidir cuáles)
            # 📚 Ver docs/IMPLEMETACION DE SRP EN PAQUETES.md - Delegación al Configurador
            # 🎯 DIP: Tipos determinados por config.json, no por código
            adquisidor = Configurador.crear_adquisidor()    # Tipo desde JSON
            procesador = Configurador.crear_procesador()    # Tipo desde JSON
            visualizador = Configurador.crear_visualizador()  # Simple

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
            print("=" * 80)
            print("DEMOSTRACIÓN SOLID COMPLETO - PROCESAMIENTO DE SEÑALES v6.0.0")
            print("DIP Aplicado: Configuración Externa JSON + Factories Especializados")
            print("=" * 80)
            print("Lanzador: Responsabilidad única → ORQUESTACIÓN")
            print("Configurador: Responsabilidad única → LEER JSON + DELEGAR A FACTORIES")
            print("Factories: FactorySenial, FactoryAdquisidor, FactoryProcesador, FactoryContexto")
            print()
            print("🎯 CONFIGURACIÓN DESDE JSON (DIP):")
            print(f"   • Adquisidor configurado con señal: {tipo_senial_adquisidor}")
            print(f"   • Procesador configurado con señal: {tipo_senial_procesador}")
            print(f"   • Tipos determinados por config.json, NO por código hardcoded")

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
            print(f'   📝 Auditoría y trazabilidad: Registradas automáticamente')
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
            print(f'   📝 Auditoría y trazabilidad: Registradas automáticamente')
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

            # ✅ RESULTADO: DIP Completo + SOLID aplicados correctamente
            print(f"\n🎉 DEMOSTRACIÓN SOLID COMPLETO CON DIP - PROCESAMIENTO SEÑALES v6.0.0")
            print("="*80)
            print("✅ RESPONSABILIDADES PERFECTAMENTE SEPARADAS:")
            print("   • Lanzador: SOLO orquestar el flujo de procesamiento")
            print("   • Configurador: SOLO leer JSON + delegar a Factories")
            print("   • CargadorConfig: SOLO leer y validar config.json")
            print("   • FactorySenial: SOLO crear señales según tipo")
            print("   • FactoryAdquisidor: SOLO crear adquisidores con señal inyectada")
            print("   • FactoryProcesador: SOLO crear procesadores con señal inyectada")
            print("   • FactoryContexto: SOLO crear contextos de persistencia")
            print("   • Repositorio: SOLO gestionar persistencia de entidades (dominio)")
            print("   • Contexto: SOLO implementar estrategia de almacenamiento (infra)")
            print("   • Adquisidor: SOLO capturar datos de entrada")
            print("   • Procesador: SOLO transformar señales")
            print("   • Visualizador: SOLO mostrar resultados")
            print()
            print("🏗️  PRINCIPIOS SOLID DEMOSTRADOS (COMPLETOS):")
            print("   ✅ SRP: Una responsabilidad por clase/paquete/factory")
            print("   ✅ OCP: Extensible para nuevos tipos editando JSON, sin modificar código")
            print("   ✅ LSP: Tipos de señal intercambiables (SenialBase aplicado)")
            print("   ✅ ISP: Interfaces segregadas - BaseAuditor y BaseTrazador independientes")
            print("   ✅ DIP: **CONFIGURACIÓN EXTERNA (JSON) DETERMINA TODAS LAS DEPENDENCIAS**")
            print("          - Repositorio depende de abstracción BaseContexto")
            print("          - Adquisidor/Procesador reciben señales inyectadas")
            print("          - Configurador delega a Factories especializados")
            print("          - Sistema completamente configurable sin tocar código")
            print()
            print("🎯 ARQUITECTURA DIP APLICADA:")
            print("   config.json → CargadorConfig → Configurador → Factories → Objetos")
            print("   • Tipos de señales: determinados por JSON")
            print("   • Tipos de adquisidores: determinados por JSON")
            print("   • Tipos de procesadores: determinados por JSON")
            print("   • Tipos de contextos: determinados por JSON")
            print("   • Parámetros: determinados por JSON")
            print()
            print("🎯 PATRÓN REPOSITORY + FACTORY:")
            print("   • Separación dominio (Repositorio) / infraestructura (Contexto)")
            print("   • API semántica: guardar() / obtener()")
            print("   • Factories especializados: FactorySenial, FactoryAdquisidor, etc.")
            print("   • Inyección de dependencias: Repositorio(contexto), Adquisidor(señal)")
            print("   • Estrategias intercambiables: ContextoPickle / ContextoArchivo")
            print()
            print("📚 LECCIÓN APRENDIDA:")
            print("   🎯 DIP COMPLETO: Configuración externa determina TODAS las dependencias")
            print("   🎯 SEPARACIÓN TOTAL de responsabilidades (SRP)")
            print("   🎯 FACTORIES ESPECIALIZADOS para cada dominio")
            print("   🎯 CONFIGURACIÓN JSON sin modificar código fuente")
            print("   🎯 ORQUESTACIÓN PURA sin lógica de negocio")
            print("   🎯 CAMBIOS EN COMPORTAMIENTO: Editar JSON, no código")
            print()
            print("📄 CONFIGURACIÓN UTILIZADA: configurador/config.json (ruta dinámica desde módulo)")
            print("📖 DOCUMENTACIÓN: docs/APLICACION_DIP_CONFIGURACION_EXTERNA.md")
            print("="*80)

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

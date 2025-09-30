"""
Configurador - Factory Centralizado para la Aplicación

Este módulo implementa el patrón Factory Centralizado que aplica SRP
para separar completamente las responsabilidades de CREACIÓN y ORQUESTACIÓN.

📚 DOCUMENTACIÓN TÉCNICA:
- SRP aplicado: docs/IMPLEMETACION DE SRP EN PAQUETES.md
- Preparación DIP: Configuración programática como base para inyección futura

🎯 PRINCIPIOS SOLID APLICADOS:
- SRP: Una responsabilidad única - crear y configurar objetos
- Preparación OCP: Extensible para nuevos tipos sin modificar cliente
- Base para DIP: Centralización que facilita inversión de dependencias

🏗️ PATRÓN IMPLEMENTADO:
Factory Centralizado con decisiones "de fábrica" - sin input del usuario,
permitiendo que el Lanzador se enfoque SOLO en orquestación.

Versión: 2.1.1 - SRP Puro con Factory Centralizado + Inyección de Señales
Autor: Victor Valotto
"""
from adquisicion_senial import AdquisidorConsola, AdquisidorArchivo
from procesamiento_senial import ProcesadorAmplificador, ProcesadorConUmbral
from presentacion_senial import Visualizador
from dominio_senial import SenialLista, SenialPila, SenialCola


class Configurador:
    """
    Factory Centralizado que aplica SRP PURO para la creación de objetos.

    📖 RESPONSABILIDAD ÚNICA:
    Crear y configurar todas las instancias de clases que participan en la
    solución de procesamiento de señales, separando completamente esta
    responsabilidad del código que USA los objetos.

    📚 REFERENCIA TEÓRICA:
    - docs/IMPLEMETACION DE SRP EN PAQUETES.md: Evolución de SRP a nivel paquetes
    - docs/IMPLEMENTACION DE OCP CON ABSTRACCIONES.md: Uso de abstracciones

    🎯 DECISIONES "DE FÁBRICA":
    Configuración programática definida en código sin input del usuario,
    permitiendo que el sistema funcione con configuraciones predeterminadas
    mientras se prepara para DIP (Dependency Inversion Principle).

    🔄 INYECCIÓN DE SEÑALES:
    Los componentes pueden reciben tipos de señal independientes:
    - Adquisidores: crear_senial_adquisidor()
    - Procesadores: crear_senial_procesador()
    Permitiendo experimentos LSP sofisticados con tipos mixtos.

    🔄 EVOLUCIÓN PLANIFICADA:
    V2.0: Configuración programática con inyección de señales (ACTUAL)
    V3.0: Configuración externa (archivos JSON/YAML) - DIP aplicado
    V4.0: Inyección de dependencias completa - IoC Container
    """

    @staticmethod
    def crear_adquisidor_consola():
        """
        Crea un adquisidor desde consola con configuración específica.

        📖 CONFIGURACIÓN INTEGRADA:
        - Número de muestras: 5
        - Tipo de señal: Configurado desde factory central

        :return: Instancia configurada de AdquisidorConsola con señal apropiada
        """
        numero_muestras = 5
        adquisidor = AdquisidorConsola(numero_muestras)
        # 🔄 INYECCIÓN DE DEPENDENCIA: Tipo de señal específico para adquisidor
        adquisidor._senial = Configurador.crear_senial_adquisidor()
        return adquisidor

    @staticmethod
    def crear_adquisidor_archivo(ruta_archivo='senial.txt'):
        """
        Crea un adquisidor desde archivo con configuración específica.

        📖 CONFIGURACIÓN INTEGRADA:
        - Archivo: 'senial.txt' por defecto
        - Tipo de señal: Configurado desde factory central

        :param ruta_archivo: Ruta del archivo a leer (por defecto 'senial.txt')
        :return: Instancia configurada de AdquisidorArchivo con señal apropiada
        """
        adquisidor = AdquisidorArchivo(ruta_archivo)
        # 🔄 INYECCIÓN DE DEPENDENCIA: Tipo de señal específico para adquisidor
        adquisidor._senial = Configurador.crear_senial_adquisidor()
        return adquisidor

    @staticmethod
    def crear_adquisidor():
        """
        🏭 FACTORY METHOD PRINCIPAL - Adquisidor configurado de fábrica.

        📖 SRP APLICADO:
        El Configurador DECIDE qué adquisidor usar sin consultar al usuario,
        separando la responsabilidad de configuración de la orquestación.

        📚 REFERENCIA OCP:
        docs/IMPLEMENTACION DE OCP CON ABSTRACCIONES.md - Demuestra cómo
        cambiar implementaciones sin modificar código cliente (Lanzador).

        🎯 DECISIÓN "DE FÁBRICA":
        AdquisidorArchivo('senial.txt') - Lectura desde archivo sin interacción.
        Esta decisión puede cambiar aquí sin afectar el Lanzador (OCP).

        🔄 INYECCIÓN AUTOMÁTICA:
        El adquisidor recibe automáticamente el tipo de señal configurado
        en crear_senial_adquisidor(), permitiendo experimentos LSP controlados.

        :return: BaseAdquisidor - Abstracción que garantiza polimorfismo
        :rtype: BaseAdquisidor
        """
        return Configurador.crear_adquisidor_archivo()

    @staticmethod
    def crear_procesador_amplificador():
        """
        Crea un procesador amplificador con configuración específica.

        📖 CONFIGURACIÓN INTEGRADA:
        - Factor de amplificación: 4.0
        - Tipo de señal: Configurado desde factory central

        :return: Instancia configurada de ProcesadorAmplificador con señal apropiada
        """
        factor_amplificacion = 4.0
        procesador = ProcesadorAmplificador(factor_amplificacion)
        # 🔄 INYECCIÓN DE DEPENDENCIA: Tipo de señal específico para procesador
        procesador._senial = Configurador.crear_senial_procesador()
        return procesador

    @staticmethod
    def crear_procesador_umbral():
        """
        Crea un procesador con umbral con configuración específica.

        📖 CONFIGURACIÓN INTEGRADA:
        - Umbral: 8.0
        - Tipo de señal: Configurado desde factory central

        :return: Instancia configurada de ProcesadorConUmbral con señal apropiada
        """
        umbral = 8.0
        procesador = ProcesadorConUmbral(umbral)
        # 🔄 INYECCIÓN DE DEPENDENCIA: Tipo de señal específico para procesador
        procesador._senial = Configurador.crear_senial_procesador()
        return procesador

    @staticmethod
    def crear_procesador():
        """
        🏭 FACTORY METHOD PRINCIPAL - Procesador configurado de fábrica.

        📖 SRP + OCP DEMOSTRADO:
        El Configurador decide qué procesador usar (SRP) y puede cambiar
        la implementación sin afectar el Lanzador (OCP).

        📚 REFERENCIA ARQUITECTÓNICA:
        docs/IMPLEMENTACION DE OCP CON ABSTRACCIONES.md - Sección "Factory Pattern"
        Explica cómo este metodo centraliza decisiones manteniendo extensibilidad.

        🎯 DECISIÓN "DE FÁBRICA":
        ProcesadorAmplificador(4.0) - Amplificación por factor 4 sin input usuario.
        Cambiar a ProcesadorConUmbral aquí NO requiere modificar Lanzador.

        🔄 INYECCIÓN AUTOMÁTICA:
        El procesador recibe automáticamente el tipo de señal configurado
        en crear_senial_procesador(), permitiendo experimentos LSP independientes.

        🔄 EJEMPLO EXTENSIÓN SIN MODIFICACIÓN:
        # return Configurador.crear_procesador_umbral()  # ← Cambio OCP
        # return Configurador.crear_procesador_suavizado()  # ← Futuro

        :return: BaseProcesador - Abstracción que garantiza polimorfismo
        :rtype: BaseProcesador
        """
        return Configurador.crear_procesador_amplificador()

    @staticmethod
    def crear_visualizador():
        """
        Crea el visualizador de señales configurado para la aplicación.

        :return: Instancia configurada de Visualizador
        """
        return Visualizador()

    @staticmethod
    def crear_senial_lista():
        """
        🏭 FACTORY METHOD - Crea señal con comportamiento de lista.

        📖 CONFIGURACIÓN "DE FÁBRICA":
        Señal básica con acceso secuencial por índice y tamaño por defecto.
        Comportamiento: Lista dinámica estándar.

        ✅ LSP APLICADO: SenialLista cumple contrato de SenialBase completamente.

        :return: Instancia configurada de SenialLista (comportamiento lista)
        :rtype: SenialLista
        """
        return SenialLista()

    @staticmethod
    def crear_senial_pila():
        """
        🏭 FACTORY METHOD - Crea señal con comportamiento de pila (LIFO).

        📖 CONFIGURACIÓN "DE FÁBRICA":
        Señal que actúa como pila - Last In, First Out.
        Comportamiento: Extracción desde el final con sacar_valor().

        ✅ LSP APLICADO: SenialPila cumple contrato de SenialBase completamente.
        Intercambiable polimórficamente con cualquier otra señal.

        :return: Instancia configurada de SenialPila (comportamiento LIFO)
        :rtype: SenialPila
        """
        return SenialPila()

    @staticmethod
    def crear_senial_cola():
        """
        🏭 FACTORY METHOD - Crea señal con comportamiento de cola circular (FIFO).

        📖 CONFIGURACIÓN "DE FÁBRICA":
        Señal que actúa como cola circular - First In, First Out.
        Comportamiento: Extracción desde el inicio con punteros circulares.
        Tamaño: 10 elementos (configuración por defecto).

        ✅ LSP APLICADO (CORRECCIONES):
        - ✅ Constructor ahora acepta parámetro opcional
        - ✅ Métodos con firmas consistentes con SenialBase
        - ✅ Intercambiable polimórficamente con otras señales
        - ✅ obtener_valor() implementa lógica circular correcta

        :return: Instancia configurada de SenialCola (comportamiento FIFO)
        :rtype: SenialCola
        """
        tamanio_cola = 10  # Configuración "de fábrica"
        return SenialCola(tamanio_cola)

    @staticmethod
    def crear_senial_adquisidor():
        """
        🏭 FACTORY METHOD ESPECÍFICO - Señal para componentes de adquisición.

        📖 PROPÓSITO:
        Permite configurar tipos de señal específicos para adquisidores,
        independientemente del tipo usado en procesadores.

        🎯 EXPERIMENTOS LSP AVANZADOS:
        Cambiar este método permite probar violaciones LSP específicas
        en la fase de adquisición sin afectar el procesamiento.

        Ejemplos experimentales:
        - return Configurador.crear_senial_pila()   # ← Adquisición con LIFO
        - return Configurador.crear_senial_cola()   # ← Adquisición con FIFO

        :return: Señal configurada específicamente para adquisidores
        :rtype: Senial
        """
        return Configurador.crear_senial_pila()

    @staticmethod
    def crear_senial_procesador():
        """
        🏭 FACTORY METHOD ESPECÍFICO - Señal para componentes de procesamiento.

        📖 PROPÓSITO:
        Permite configurar tipos de señal específicos para procesadores,
        independientemente del tipo usado en adquisidores.

        🎯 EXPERIMENTOS LSP AVANZADOS:
        Cambiar este método permite probar violaciones LSP específicas
        en la fase de procesamiento, creando inconsistencias interesantes.

        🧪 ESCENARIOS EXPERIMENTALES:
        - Adquisidor: Lista, Procesador: Pila  ← Inconsistencia mixta
        - Adquisidor: Cola, Procesador: Lista  ← Transferencia problemática
        - Adquisidor: Pila, Procesador: Cola   ← Semánticas opuestas

        :return: Señal configurada específicamente para procesadores
        :rtype: Senial
        """
        return Configurador.crear_senial_cola()

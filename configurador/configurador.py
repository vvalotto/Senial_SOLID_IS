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

Versión: 2.2.0 - SRP Puro + Persistencia integrada (preparado para ISP)
Autor: Victor Valotto
"""
from adquisicion_senial import AdquisidorConsola, AdquisidorArchivo
from procesamiento_senial import ProcesadorAmplificador, ProcesadorConUmbral
from presentacion_senial import Visualizador
from dominio_senial import SenialLista, SenialPila, SenialCola
from persistidor_senial import PersistidorPickle, PersistidorArchivo


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

    💾 PERSISTENCIA INTEGRADA (v2.2.0):
    Factory methods para persistidores con violaciones ISP intencionales:
    - crear_persistidor() → PersistidorPickle (genérico)
    - crear_persistidor_adquisidor() → Persistidor para señales adquiridas
    - crear_persistidor_procesador() → Persistidor para señales procesadas
    - crear_persistidor_pickle() → Serialización binaria
    - crear_persistidor_archivo() → Archivos de texto plano

    🔄 INYECCIÓN INDEPENDIENTE DE PERSISTIDORES:
    Permite configurar estrategias de persistencia diferentes por fase:
    - Adquisidor puede guardar en formato binario (rápido)
    - Procesador puede guardar en texto plano (analizable)

    🔄 EVOLUCIÓN PLANIFICADA:
    V2.0: Configuración programática con inyección de señales
    V2.2: Persistencia integrada - Preparado para demostración ISP (ACTUAL)
    V3.0: Aplicación de ISP - Interfaces segregadas
    V4.0: Configuración externa (archivos JSON/YAML) - DIP aplicado
    V5.0: Inyección de dependencias completa - IoC Container
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

    @staticmethod
    def crear_persistidor_pickle():
        """
        🏭 FACTORY METHOD - Crea persistidor basado en pickle (serialización binaria).

        📖 CONFIGURACIÓN "DE FÁBRICA":
        Persistidor que usa pickle para serialización binaria eficiente.
        Directorio: './datos_persistidos/adquisicion'

        ✅ CARACTERÍSTICAS:
        - Serialización rápida y eficiente
        - Preserva estructura completa del objeto
        - Formato binario (.pickle)

        ⚠️ VIOLACIÓN ISP:
        Este persistidor tiene métodos persistir() y recuperar() en la misma interfaz,
        forzando a los clientes a depender de métodos que pueden no necesitar.

        :return: Instancia configurada de PersistidorPickle
        :rtype: PersistidorPickle
        """
        recurso = './datos_persistidos/adquisicion'
        return PersistidorPickle(recurso)

    @staticmethod
    def crear_persistidor_archivo():
        """
        🏭 FACTORY METHOD - Crea persistidor basado en archivos de texto plano.

        📖 CONFIGURACIÓN "DE FÁBRICA":
        Persistidor que usa formato de texto plano con mapeo custom.
        Directorio: './datos_persistidos/procesamiento'

        ✅ CARACTERÍSTICAS:
        - Formato de texto plano (.dat)
        - Human-readable para debugging
        - Soporta listas y colecciones

        ⚠️ VIOLACIÓN ISP:
        Este persistidor tiene métodos persistir() y recuperar() en la misma interfaz,
        forzando a los clientes a depender de métodos que pueden no necesitar.

        :return: Instancia configurada de PersistidorArchivo
        :rtype: PersistidorArchivo
        """
        recurso = './datos_persistidos/procesamiento'
        return PersistidorArchivo(recurso)

    @staticmethod
    def crear_persistidor_adquisidor():
        """
        🏭 FACTORY METHOD ESPECÍFICO - Persistidor para señales del adquisidor.

        📖 PROPÓSITO:
        Permite configurar persistidor específico para guardar señales adquiridas,
        independientemente del persistidor usado para señales procesadas.

        🎯 INYECCIÓN INDEPENDIENTE:
        Permite experimentar con diferentes estrategias de persistencia por fase:
        - Adquisidor puede usar Pickle (rápido)
        - Procesador puede usar Archivo (human-readable)

        ⚠️ VIOLACIÓN ISP PRESENTE:
        El persistidor tiene métodos persistir() y recuperar() juntos,
        aunque el adquisidor solo necesita persistir.

        🧪 ESCENARIOS EXPERIMENTALES:
        - return Configurador.crear_persistidor_pickle()   # ← Binario rápido
        - return PersistidorArchivo('./datos_persistidos/adquisicion')  # ← Texto debuggeable

        :return: Persistidor configurado para señales del adquisidor
        :rtype: PersistidorPickle | PersistidorArchivo
        """
        recurso = './datos_persistidos/adquisicion'
        return PersistidorArchivo(recurso)

    @staticmethod
    def crear_persistidor_procesador():
        """
        🏭 FACTORY METHOD ESPECÍFICO - Persistidor para señales del procesador.

        📖 PROPÓSITO:
        Permite configurar persistidor específico para guardar señales procesadas,
        independientemente del persistidor usado para señales adquiridas.

        🎯 INYECCIÓN INDEPENDIENTE:
        Permite experimentar con diferentes estrategias de persistencia por fase:
        - Señal original: carpeta adquisicion
        - Señal procesada: carpeta procesamiento

        ⚠️ VIOLACIÓN ISP PRESENTE:
        El persistidor tiene métodos persistir() y recuperar() juntos,
        aunque el procesador solo necesita persistir.

        🧪 ESCENARIOS EXPERIMENTALES:
        - return PersistidorPickle('./datos_persistidos/procesamiento')  # ← Binario
        - return Configurador.crear_persistidor_archivo()  # ← Texto analizable

        :return: Persistidor configurado para señales del procesador
        :rtype: PersistidorPickle | PersistidorArchivo
        """
        recurso = './datos_persistidos/procesamiento'
        return PersistidorPickle(recurso)

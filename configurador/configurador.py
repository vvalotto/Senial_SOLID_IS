"""
Configurador - Factory Centralizado con Configuración Externa (DIP Aplicado)

Este módulo implementa el patrón Factory Centralizado con configuración JSON externa,
aplicando completamente el principio DIP (Dependency Inversion Principle).

📚 DOCUMENTACIÓN TÉCNICA:
- SRP aplicado: docs/IMPLEMETACION DE SRP EN PAQUETES.md
- DIP con configuración externa: docs/APLICACION_DIP_CONFIGURACION_EXTERNA.md

🎯 PRINCIPIOS SOLID APLICADOS:
- SRP: Una responsabilidad única - crear y configurar objetos desde JSON
- OCP: Extensible para nuevos tipos sin modificar código cliente
- DIP: Configuración externa (JSON) determina las dependencias del sistema

🏗️ PATRÓN IMPLEMENTADO:
Factory Centralizado con Configuración Externa - Las dependencias se leen desde
config.json, permitiendo cambiar el comportamiento del sistema sin modificar código.

🔄 MIGRACIÓN XML → JSON:
Versión 2.0.0: Configuración desde XML (minidom.parse)
Versión 3.0.0: Configuración desde JSON con Factories especializados (ACTUAL)

Versión: 3.0.0 - DIP Completo con Configuración Externa JSON
Autor: Victor Valotto
"""
# Imports de abstracciones
from presentacion_senial import Visualizador

# Imports de Factories especializados (DIP)
from dominio_senial import FactorySenial
from adquisicion_senial import FactoryAdquisidor
from procesamiento_senial import FactoryProcesador
from persistidor_senial import FactoryContexto

# Imports para Patrón Repository
from persistidor_senial import RepositorioSenial

# Cargador de configuración externa
from configurador.cargador_config import CargadorConfig


class Configurador:
    """
    Factory Centralizado con Configuración Externa (DIP Aplicado).

    📖 RESPONSABILIDAD ÚNICA:
    Crear y configurar todas las instancias desde configuración externa (JSON),
    delegando la creación de objetos a Factories especializados.

    📚 REFERENCIA TEÓRICA:
    - docs/IMPLEMETACION DE SRP EN PAQUETES.md: Evolución de SRP a nivel paquetes
    - docs/APLICACION_DIP_CONFIGURACION_EXTERNA.md: DIP con JSON

    🎯 DIP APLICADO:
    Las dependencias del sistema se determinan desde config.json:
    - Tipos de señales: JSON decide lista/pila/cola
    - Tipos de adquisidores: JSON decide consola/archivo/senoidal
    - Tipos de procesadores: JSON decide amplificador/umbral
    - Tipos de contextos: JSON decide pickle/archivo

    🏭 FACTORIES ESPECIALIZADOS:
    - FactorySenial: Crea señales según tipo y configuración
    - FactoryAdquisidor: Crea adquisidores con señal inyectada
    - FactoryProcesador: Crea procesadores con señal inyectada
    - FactoryContexto: Crea contextos de persistencia

    🔄 SIMPLIFICACIÓN V3.0:
    Solo métodos que leen del JSON. Métodos específicos eliminados (redundantes).
    Toda la configuración viene del archivo config.json.

    🔄 EVOLUCIÓN COMPLETADA:
    ✅ V2.0: Configuración programática con inyección de señales
    ✅ V2.2: Persistencia integrada - Patrón Repository
    ✅ V3.0: Configuración externa (JSON) + Factories + Simplificación (ACTUAL)
    📋 V4.0: Validación de esquemas JSON
    📋 V5.0: Inyección de dependencias completa - IoC Container
    """

    # Instancia singleton del cargador de configuración
    _cargador = None

    # =========================================================================
    # INICIALIZACIÓN
    # =========================================================================

    @staticmethod
    def inicializar_configuracion(ruta_config: str = None):
        """
        🚀 Inicializa el sistema de configuración externa.

        📖 DIP APLICADO:
        Carga la configuración JSON que determinará todas las dependencias
        del sistema. Este método debe llamarse ANTES de crear componentes.

        🔄 RUTA DINÁMICA:
        Si no se proporciona ruta_config, busca config.json en el directorio
        del módulo configurador (usando __file__), independientemente de
        desde dónde se ejecute el lanzador.

        🔄 EQUIVALENTE A: minidom.parse("./datos/configuracion.xml")

        🧪 USO EN LANZADOR:
        ```python
        # Al inicio del programa (sin especificar ruta - usa default)
        Configurador.inicializar_configuracion()

        # O con ruta explícita
        Configurador.inicializar_configuracion('/ruta/custom/config.json')

        # Luego crear componentes (ya configurados desde JSON)
        adquisidor = Configurador.crear_adquisidor()
        procesador = Configurador.crear_procesador()
        ```

        :param ruta_config: Ruta al archivo config.json (None = usa directorio del módulo)
        :raises FileNotFoundError: Si el archivo no existe
        :raises json.JSONDecodeError: Si el JSON es inválido
        """
        Configurador._cargador = CargadorConfig(ruta_config)
        Configurador._cargador.cargar()
        print(f"✅ Configuración cargada desde {Configurador._cargador.ruta_config}")

    # =========================================================================
    # CREACIÓN DE SEÑALES (desde JSON)
    # =========================================================================

    @staticmethod
    def crear_senial_adquisidor():
        """
        🏭 FACTORY METHOD - Señal para componentes de adquisición.

        🔄 REFACTORIZADO V3.0: Lee configuración desde JSON

        📖 DIP APLICADO:
        La configuración externa (JSON) determina el tipo de señal.
        Si no hay configuración, usa fallback (lista, tamaño 10).

        🔄 EQUIVALENTE A: definir_senial_adquirir() (versión XML v2.0.0)

        XML: <senial_adq>cola<tamanio>20</tamanio></senial_adq>
        JSON: "senial_adquisidor": {"tipo": "cola", "tamanio": 20}

        :return: Señal configurada desde JSON para adquisidores
        """
        if Configurador._cargador is None:
            # Fallback: sin configuración externa
            config = {'tamanio': 10}
            return FactorySenial.crear('lista', config)

        # Leer configuración desde JSON
        config = Configurador._cargador.obtener_config_senial_adquisidor()
        tipo = config.get('tipo', 'lista')
        return FactorySenial.crear(tipo, config)

    @staticmethod
    def crear_senial_procesador():
        """
        🏭 FACTORY METHOD - Señal para componentes de procesamiento.

        🔄 REFACTORIZADO V3.0: Lee configuración desde JSON

        📖 DIP APLICADO:
        La configuración externa (JSON) determina el tipo de señal.
        Si no hay configuración, usa fallback (lista, tamaño 10).

        🔄 EQUIVALENTE A: definir_senial_procesar() (versión XML v2.0.0)

        XML: <senial_pro>pila<tamanio>20</tamanio></senial_pro>
        JSON: "senial_procesador": {"tipo": "pila", "tamanio": 20}

        :return: Señal configurada desde JSON para procesadores
        """
        if Configurador._cargador is None:
            # Fallback: sin configuración externa
            config = {'tamanio': 10}
            return FactorySenial.crear('lista', config)

        # Leer configuración desde JSON
        config = Configurador._cargador.obtener_config_senial_procesador()
        tipo = config.get('tipo', 'lista')
        return FactorySenial.crear(tipo, config)

    # =========================================================================
    # CREACIÓN DE ADQUISIDORES (desde JSON)
    # =========================================================================

    @staticmethod
    def crear_adquisidor():
        """
        🏭 FACTORY METHOD PRINCIPAL - Adquisidor configurado desde JSON.

        🔄 REFACTORIZADO V3.0: Lee configuración desde JSON

        📖 DIP APLICADO:
        La configuración externa (JSON) determina:
        - Tipo de adquisidor (consola/archivo/senoidal)
        - Parámetros específicos (ruta_archivo, num_muestras, etc.)
        - Tipo de señal a usar

        🔄 EQUIVALENTE A: definir_adquisidor() (versión XML v2.0.0)

        XML: <adquisidor>archivo
             <param id="dir_entrada_datos">./adquisidor/datos.txt</param>
             </adquisidor>
        JSON: "adquisidor": {"tipo": "archivo",
              "ruta_archivo": "./adquisidor/datos.txt"}

        :return: BaseAdquisidor configurado desde JSON
        """
        if Configurador._cargador is None:
            # Fallback: sin configuración externa
            config = {'ruta_archivo': 'senial.txt'}
            senial = Configurador.crear_senial_adquisidor()
            return FactoryAdquisidor.crear('archivo', config, senial)

        # Leer configuración desde JSON
        config = Configurador._cargador.obtener_config_adquisidor()
        tipo = config.get('tipo', 'archivo')

        # Crear señal configurada
        senial = Configurador.crear_senial_adquisidor()

        # Usar factory con configuración externa
        return FactoryAdquisidor.crear(tipo, config, senial)

    # =========================================================================
    # CREACIÓN DE PROCESADORES (desde JSON)
    # =========================================================================

    @staticmethod
    def crear_procesador():
        """
        🏭 FACTORY METHOD PRINCIPAL - Procesador configurado desde JSON.

        🔄 REFACTORIZADO V3.0: Lee configuración desde JSON

        📖 DIP APLICADO:
        La configuración externa (JSON) determina:
        - Tipo de procesador (amplificador/umbral)
        - Parámetros específicos (factor, umbral)
        - Tipo de señal a usar

        🔄 EQUIVALENTE A: definir_procesador() (versión XML v2.0.0)

        XML: <procesador>umbral<param id="umbral">100</param></procesador>
        JSON: "procesador": {"tipo": "umbral", "umbral": 100}

        :return: BaseProcesador configurado desde JSON
        """
        if Configurador._cargador is None:
            # Fallback: sin configuración externa
            config = {'factor': 4.0}
            senial = Configurador.crear_senial_procesador()
            return FactoryProcesador.crear('amplificador', config, senial)

        # Leer configuración desde JSON
        config = Configurador._cargador.obtener_config_procesador()
        tipo = config.get('tipo', 'amplificador')

        # Crear señal configurada
        senial = Configurador.crear_senial_procesador()

        # Usar factory con configuración externa
        return FactoryProcesador.crear(tipo, config, senial)

    # =========================================================================
    # CREACIÓN DE VISUALIZADORES
    # =========================================================================

    @staticmethod
    def crear_visualizador():
        """
        Crea el visualizador de señales configurado para la aplicación.

        :return: Instancia configurada de Visualizador
        """
        return Visualizador()

    # =========================================================================
    # CREACIÓN DE REPOSITORIOS (desde JSON)
    # =========================================================================

    @staticmethod
    def crear_repositorio_adquisicion():
        """
        🏭 FACTORY METHOD - Repositorio para señales adquiridas (desde JSON).

        🔄 REFACTORIZADO V3.0: Usa factories directamente sin wrappers

        📖 DIP APLICADO:
        La configuración externa (JSON) determina:
        - Tipo de contexto (pickle/archivo)
        - Recurso/directorio de persistencia

        🔄 EQUIVALENTE A: definir_repositorio(ctx_datos_adquisicion) (versión XML v2.0.0)

        XML: <contexto>pickle</contexto> + <dir_recurso_datos>./tmp/datos</dir_recurso_datos>
        JSON: "contexto_adquisicion": {"tipo": "pickle", "recurso": "./tmp/datos/adquisicion"}

        🏭 FLUJO DIP:
        JSON → CargadorConfig → FactoryContexto → RepositorioSenial

        :return: Repositorio configurado desde JSON para señales adquiridas
        """
        if Configurador._cargador is None:
            # Fallback: sin configuración externa
            config = {'recurso': './datos_persistidos/adquisicion'}
            ctx = FactoryContexto.crear('archivo', config)
            return RepositorioSenial(ctx)

        # Leer configuración desde JSON
        config = Configurador._cargador.obtener_config_contexto_adquisicion()
        tipo = config.get('tipo', 'pickle')

        # Crear contexto con FactoryContexto (sin wrapper)
        ctx = FactoryContexto.crear(tipo, config)

        # Crear repositorio directamente (sin wrapper)
        return RepositorioSenial(ctx)

    @staticmethod
    def crear_repositorio_procesamiento():
        """
        🏭 FACTORY METHOD - Repositorio para señales procesadas (desde JSON).

        🔄 REFACTORIZADO V3.0: Usa factories directamente sin wrappers

        📖 DIP APLICADO:
        La configuración externa (JSON) determina:
        - Tipo de contexto (pickle/archivo)
        - Recurso/directorio de persistencia

        🔄 EQUIVALENTE A: definir_repositorio(ctx_datos_procesamiento) (versión XML v2.0.0)

        XML: <contexto>pickle</contexto> + <dir_recurso_datos>./tmp/datos</dir_recurso_datos>
        JSON: "contexto_procesamiento": {"tipo": "pickle", "recurso": "./tmp/datos/procesamiento"}

        🏭 FLUJO DIP:
        JSON → CargadorConfig → FactoryContexto → RepositorioSenial

        :return: Repositorio configurado desde JSON para señales procesadas
        """
        if Configurador._cargador is None:
            # Fallback: sin configuración externa
            config = {'recurso': './datos_persistidos/procesamiento'}
            ctx = FactoryContexto.crear('pickle', config)
            return RepositorioSenial(ctx)

        # Leer configuración desde JSON
        config = Configurador._cargador.obtener_config_contexto_procesamiento()
        tipo = config.get('tipo', 'pickle')

        # Crear contexto con FactoryContexto (sin wrapper)
        ctx = FactoryContexto.crear(tipo, config)

        # Crear repositorio directamente (sin wrapper)
        return RepositorioSenial(ctx)

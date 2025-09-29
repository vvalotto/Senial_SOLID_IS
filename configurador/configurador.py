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

Versión: 2.0.0 - SRP Puro con Factory Centralizado
Autor: Victor Valotto
"""
from adquisicion_senial import AdquisidorConsola, AdquisidorArchivo
from procesamiento_senial import ProcesadorAmplificador, ProcesadorConUmbral
from presentacion_senial import Visualizador


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

    🔄 EVOLUCIÓN PLANIFICADA:
    V2.0: Configuración programática (ACTUAL)
    V3.0: Configuración externa (archivos JSON/YAML) - DIP aplicado
    V4.0: Inyección de dependencias completa - IoC Container
    """

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

        :return: BaseAdquisidor - Abstracción que garantiza polimorfismo
        :rtype: BaseAdquisidor
        """
        return Configurador.crear_adquisidor_archivo()

    @staticmethod
    def crear_adquisidor_consola():
        """
        Crea un adquisidor desde consola con configuración específica.

        Configuración actual: 5 muestras por señal
        :return: Instancia configurada de AdquisidorConsola
        """
        numero_muestras = 5
        return AdquisidorConsola(numero_muestras)

    @staticmethod
    def crear_adquisidor_archivo(ruta_archivo='senial.txt'):
        """
        Crea un adquisidor desde archivo con configuración específica.

        :param ruta_archivo: Ruta del archivo a leer (por defecto 'senial.txt')
        :return: Instancia configurada de AdquisidorArchivo
        """
        return AdquisidorArchivo(ruta_archivo)

    @staticmethod
    def crear_procesador_amplificador():
        """
        Crea un procesador amplificador con configuración específica.

        Configuración actual: Factor de amplificación 4.0
        :return: Instancia configurada de ProcesadorAmplificador
        """
        factor_amplificacion = 4.0
        return ProcesadorAmplificador(factor_amplificacion)

    @staticmethod
    def crear_procesador_umbral():
        """m
        Crea un procesador con umbral con configuración específica.

        Configuración actual: Umbral de 8.0
        :return: Instancia configurada de ProcesadorConUmbral
        """
        umbral = 8.0
        return ProcesadorConUmbral(umbral)

    @staticmethod
    def crear_procesador():
        """
        🏭 FACTORY METHOD PRINCIPAL - Procesador configurado de fábrica.

        📖 SRP + OCP DEMOSTRADO:
        El Configurador decide qué procesador usar (SRP) y puede cambiar
        la implementación sin afectar el Lanzador (OCP).

        📚 REFERENCIA ARQUITECTÓNICA:
        docs/IMPLEMENTACION DE OCP CON ABSTRACCIONES.md - Sección "Factory Pattern"
        Explica cómo este método centraliza decisiones manteniendo extensibilidad.

        🎯 DECISIÓN "DE FÁBRICA":
        ProcesadorAmplificador(4.0) - Amplificación por factor 4 sin input usuario.
        Cambiar a ProcesadorConUmbral aquí NO requiere modificar Lanzador.

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

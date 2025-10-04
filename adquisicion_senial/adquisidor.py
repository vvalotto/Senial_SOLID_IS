"""
Paquete adquisicion_senial - Aplicación de OCP con Strategy Pattern

Este módulo demuestra la implementación correcta del Open/Closed Principle
usando el patrón Strategy para diferentes tipos de adquisición de señales digitales.

📚 DOCUMENTACIÓN TÉCNICA:
- OCP completo: docs/IMPLEMENTACION DE OCP CON ABSTRACCIONES.md
- Strategy Pattern: Abstracciones + polimorfismo + extensibilidad infinita

🎯 PRINCIPIOS SOLID APLICADOS:
- SRP: Cada adquisidor tiene responsabilidad única y específica
- OCP: Extensible para nuevos tipos sin modificar código existente
- LSP: Todas las implementaciones son intercambiables polimórficamente

🏗️ PATRÓN STRATEGY IMPLEMENTADO:
- BaseAdquisidor: Abstracción que define el contrato común
- AdquisidorConsola: Estrategia concreta para entrada interactiva
- AdquisidorArchivo: Estrategia concreta para lectura de archivos
- Futuras extensiones: Sensores, APIs, bases de datos, etc.

Versión: 2.1.0 - OCP + DIP (Dependency Inversion Principle)
Autor: Victor Valotto
"""
from abc import ABCMeta, abstractmethod
from dominio_senial.senial import SenialBase


class BaseAdquisidor(metaclass=ABCMeta):
    """
    🏗️ ABSTRACCIÓN BASE - Strategy Pattern para adquisición extensible.

    📚 REFERENCIA OCP:
    docs/IMPLEMENTACION DE OCP CON ABSTRACCIONES.md - Sección "Strategy Pattern"
    Demuestra cómo las abstracciones permiten extensibilidad infinita.

    🎯 CONTRATO COMÚN:
    Define la interfaz que TODAS las implementaciones deben cumplir,
    garantizando intercambiabilidad polimórfica (LSP).

    ✅ CUMPLE OCP:
    - Abierto para extensión: Nuevos adquisidores heredan de esta clase
    - Cerrado para modificación: Este contrato NO cambia
    - Polimorfismo: Cliente usa BaseAdquisidor, no implementaciones específicas

    🔄 EXTENSIBILIDAD DEMOSTRADA:
    Agregar AdquisidorSensor, AdquisidorAPI, etc. NO requiere modificar:
    - Esta clase abstracta
    - Código que usa BaseAdquisidor
    - Tests polimórficos existentes

    ✅ DIP APLICADO:
    Depende de SenialBase (abstracción), no de implementaciones concretas.
    El tipo específico (SenialLista, SenialPila, SenialCola) es inyectado
    por el Configurador en tiempo de creación.
    """
    def __init__(self, numero_muestras):
        """
        Inicializa el adquisidor base.

        ✅ DIP: No instancia señal concreta aquí. El Configurador inyectará
        el tipo específico mediante self._senial = Configurador.crear_senial_xxx()

        :param numero_muestras: Cantidad de muestras a adquirir
        """
        self._senial: SenialBase = None  # Inyectado por Configurador
        self._numero_muestras = numero_muestras

    def obtener_senial_adquirida(self):
        """
        Devuelve la señal adquirida.

        :return: Instancia de Senial con los datos adquiridos
        """
        return self._senial

    @abstractmethod
    def leer_senial(self):
        """
        🔄 METODO ABSTRACTO - Punto de extensión OCP.

        📚 REFERENCIA ARQUITECTÓNICA:
        docs/IMPLEMENTACION DE OCP CON ABSTRACCIONES.md - "Abstract Methods"
        Explica cómo los métodos abstractos garantizan implementación obligatoria.

        🎯 CONTRATO OBLIGATORIO:
        Cada implementación concreta DEBE definir cómo adquiere los datos
        específicos de su fuente (consola, archivo, sensor, API, etc.).

        ✅ EXTENSIBILIDAD OCP:
        Nuevas implementaciones solo deben implementar este método:
        - AdquisidorConsola.leer_senial() → Input desde teclado
        - AdquisidorArchivo.leer_senial() → Lectura desde archivos
        - AdquisidorSensor.leer_senial() → Captura desde hardware IoT
        - AdquisidorAPI.leer_senial() → Descarga desde REST API

        🔒 INVARIANTE LSP:
        Todas las implementaciones deben llenar self._senial con datos válidos.
        """
        pass


class AdquisidorConsola(BaseAdquisidor):
    """
    🖥️ ESTRATEGIA CONCRETA - Adquisición interactiva desde consola.

    📚 REFERENCIA OCP:
    docs/IMPLEMENTACION DE OCP CON ABSTRACCIONES.md - "Implementaciones Concretas"
    Demuestra extensión sin modificación de código existente.

    🎯 RESPONSABILIDAD ESPECÍFICA (SRP):
    Capturar valores numéricos ingresados por el usuario a través de la consola,
    con validación de entrada y manejo de errores.

    ✅ CUMPLE LSP:
    - Intercambiable con cualquier BaseAdquisidor
    - Respeta el contrato: llenar self._senial con datos válidos
    - Comportamiento consistente con la abstracción

    🔄 EJEMPLO POLIMORFISMO:
    def usar_adquisidor(adq: BaseAdquisidor):  # ← Funciona con CUALQUIERA
        adq.leer_senial()  # ← Este metodo funciona automáticamente
        return adq.obtener_senial_adquirida()
    """
    @staticmethod
    def _leer_dato_entrada():
        """
        Lee un valor numérico desde la consola con validación.

        :return: Valor numérico ingresado por el usuario
        :raises: Continúa pidiendo input hasta recibir un número válido
        """
        while True:
            try:
                return float(input('Ingresar Valor: '))
            except ValueError:
                print('❌ Dato mal ingresado. Por favor ingrese un número válido.')

    def leer_senial(self):
        """
        Implementa la adquisición de datos desde consola.

        Lee la cantidad especificada de muestras solicitando input del usuario.
        """
        print("📡 Lectura de la señal desde consola")
        for i in range(self._numero_muestras):
            print(f"Dato nro: {i}")
            self._senial.poner_valor(self._leer_dato_entrada())


class AdquisidorArchivo(BaseAdquisidor):
    """
    Adquisidor de datos desde archivo.

    Implementación concreta que lee valores numéricos desde un archivo de texto,
    donde cada línea contiene un valor de la señal.
    """

    def __init__(self, ruta_archivo):
        """
        Inicializa el adquisidor con la ruta del archivo a leer.

        :param ruta_archivo: Ruta completa al archivo que contiene los datos
        :raises ValueError: Si la ruta no es una cadena válida
        """
        super().__init__(0)  # No conocemos el tamaño hasta leer el archivo
        if isinstance(ruta_archivo, str):
            self._ruta_archivo = ruta_archivo
        else:
            raise ValueError('La ruta del archivo debe ser una cadena de texto válida')

    @property
    def ruta_archivo(self):
        """
        Getter para la ruta del archivo.

        :return: Ruta del archivo configurado
        """
        return self._ruta_archivo

    def leer_senial(self):
        """
        Implementa la adquisición de datos desde archivo.

        Lee valores numéricos línea por línea desde el archivo especificado.
        Cada línea debe contener un único valor numérico.
        """
        print(f"📁 Lectura de la señal desde archivo: {self._ruta_archivo}")
        try:
            with open(self._ruta_archivo, 'r', encoding='utf-8') as archivo:
                for numero_linea, linea in enumerate(archivo, 1):
                    try:
                        dato = float(linea.strip())
                        self._senial.poner_valor(dato)
                        print(f"  Línea {numero_linea}: {dato}")
                    except ValueError:
                        print(f"⚠️  Advertencia: Línea {numero_linea} contiene dato inválido: '{linea.strip()}'")
                        continue
        except FileNotFoundError:
            print(f"❌ Error: Archivo no encontrado: {self._ruta_archivo}")
        except IOError as e:
            print(f"❌ Error de lectura: {e}")

        print(f"✅ Adquisición completada: {self._senial.obtener_tamanio()} muestras leídas")


class AdquisidorSenoidal(BaseAdquisidor):
    """
    🌊 ESTRATEGIA CONCRETA - Generador de señal senoidal sintética.

    📚 REFERENCIA OCP:
    Implementación concreta que genera valores senoidales calculados
    matemáticamente, útil para testing y simulaciones.

    🎯 RESPONSABILIDAD ESPECÍFICA (SRP):
    Generar una señal senoidal sintética con amplitud y frecuencia predefinidas,
    útil para pruebas sin necesidad de datos reales.

    ✅ CUMPLE LSP:
    - Intercambiable con cualquier BaseAdquisidor
    - Respeta el contrato: llenar self._senial con datos válidos
    - Comportamiento predecible: generación determinística

    ⚠️ NOTA: Constructor recibe numero_muestras para consistencia con BaseAdquisidor
    """
    def __init__(self, numero_muestras: int = 10):
        """
        Inicializa el generador de señal senoidal.

        ✅ CORRECCIÓN: Ahora consistente con BaseAdquisidor
        - Recibe numero_muestras (no señal)
        - La señal será inyectada por el factory

        :param numero_muestras: Cantidad de muestras a generar (default: 10)
        """
        super().__init__(numero_muestras)
        self._valor = 0.0
        self._i = 0

    def _leer_dato_entrada(self):
        """
        Genera un valor senoidal calculado matemáticamente.

        🔢 FÓRMULA:
        valor = sin((i / num_muestras) * 2π) * 10

        :return: Valor senoidal calculado
        """
        import math
        # Generar valor senoidal con amplitud 10
        self._valor = math.sin((float(self._i) / float(self._numero_muestras)) * 2 * math.pi) * 10
        self._i += 1
        return self._valor

    def leer_senial(self):
        """
        Implementa la generación de señal senoidal.

        Genera la cantidad especificada de muestras senoidales y las
        almacena en la señal inyectada.
        """
        print(f'🌊 Generación de señal senoidal ({self._numero_muestras} muestras)')
        i = 0
        try:
            while i < self._numero_muestras:
                valor = self._leer_dato_entrada()
                self._senial.poner_valor(valor)
                print(f"  Muestra {i}: {valor:.2f}")
                i += 1
            print(f"✅ Generación completada: {self._senial.obtener_tamanio()} muestras")
        except Exception as ex:
            print(f"❌ Error en la generación de datos: {ex}")
            raise

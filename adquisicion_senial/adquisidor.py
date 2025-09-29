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

Versión: 2.0.0 - OCP con Strategy Pattern
Autor: Victor Valotto
"""
from abc import ABCMeta, abstractmethod
from dominio_senial.senial import Senial


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
    """
    def __init__(self, numero_muestras):
        """
        Inicializa el adquisidor base con una señal vacía.

        :param numero_muestras: Cantidad de muestras a adquirir
        """
        self._senial = Senial()
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
        🔄 MÉTODO ABSTRACTO - Punto de extensión OCP.

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
        adq.leer_senial()  # ← Este método funciona automáticamente
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
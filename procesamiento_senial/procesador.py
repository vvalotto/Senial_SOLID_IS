"""
Paquete procesamiento_senial - Aplicación completa de OCP con Strategy Pattern

Este módulo demuestra la implementación correcta del Open/Closed Principle
refactorizando desde violación hacia extensibilidad sin modificación.

📚 DOCUMENTACIÓN TÉCNICA:
- OCP completo: docs/IMPLEMENTACION DE OCP CON ABSTRACCIONES.md
- Strategy + Factory Pattern: Abstracciones + polimorfismo + creación extensible

🎯 EVOLUCIÓN OCP DEMOSTRADA:
ANTES: Modificar clase existente para cada nuevo tipo (violación OCP)
DESPUÉS: Solo agregar nueva clase que herede de BaseProcesador (cumple OCP)

🏗️ PATRÓN STRATEGY IMPLEMENTADO:
- BaseProcesador: Abstracción que define contrato común
- ProcesadorAmplificador: Estrategia concreta para amplificación
- ProcesadorConUmbral: Estrategia concreta para filtrado por umbral
- Futuras extensiones: FFT, Wavelets, Filtros digitales, etc.

Versión: 2.1.0 - OCP + DIP (Dependency Inversion Principle)
Autor: Victor Valotto
"""
from abc import ABCMeta, abstractmethod
from dominio_senial.senial import SenialBase


class BaseProcesador(metaclass=ABCMeta):
    """
    🏗️ ABSTRACCIÓN BASE - Strategy Pattern para procesamiento extensible.

    📚 REFERENCIA OCP:
    docs/IMPLEMENTACION DE OCP CON ABSTRACCIONES.md - "Factory Pattern + Polimorfismo"
    Demuestra cómo las abstracciones permiten extensibilidad infinita sin modificación.

    🎯 CONTRATO COMÚN:
    Define la interfaz estable que TODAS las implementaciones deben cumplir,
    permitiendo intercambiabilidad polimórfica total (LSP).

    ✅ CUMPLE OCP PERFECTAMENTE:
    - Abierto para extensión: Infinitas implementaciones posibles
    - Cerrado para modificación: Esta abstracción NUNCA cambia
    - Polimorfismo: Cliente usa BaseProcesador, ignora implementaciones específicas

    🔄 EXTENSIBILIDAD SIN LÍMITES:
    Agregar ProcesadorFFT, ProcesadorWavelet, ProcesadorFiltroDigital NO requiere:
    - Modificar esta clase abstracta
    - Modificar código que usa BaseProcesador
    - Modificar Factory methods existentes
    - Modificar tests polimórficos

    ✅ DIP APLICADO:
    Depende de SenialBase (abstracción), no de implementaciones concretas.
    El tipo específico (SenialLista, SenialPila, SenialCola) es inyectado
    por el Configurador en tiempo de creación.
    """
    def __init__(self):
        """
        Se inicializa con la señal que se va a procesar.

        ✅ DIP: No instancia señal concreta aquí. El Configurador inyectará
        el tipo específico mediante self._senial = Configurador.crear_senial_xxx()
        """
        self._senial: SenialBase = None  # Inyectado por Configurador

    @abstractmethod
    def procesar(self, senial):
        """
        Metodo abstracto que se implementara para cada tipo de procesamiento
        """

    def obtener_senial_procesada(self):
        """
        Devuelve la señal procesada
        """
        return self._senial


class ProcesadorAmplificador(BaseProcesador):
    """
    🔊 ESTRATEGIA CONCRETA - Amplificación con factor configurable.

    📚 REFERENCIA OCP:
    docs/IMPLEMENTACION DE OCP CON ABSTRACCIONES.md - "Extensiones sin Modificación"
    Primera implementación que demuestra extensión del contrato base.

    🎯 RESPONSABILIDAD ESPECÍFICA (SRP):
    Amplificar cada valor de la señal por un factor configurable,
    aplicando transformación matemática simple: valor_nuevo = valor_original * factor.

    ✅ CUMPLE LSP:
    - Intercambiable con cualquier BaseProcesador
    - Respeta el contrato: procesar() llena self._senial
    - Comportamiento predecible: amplificación determinística

    🔄 EJEMPLO EXTENSIÓN OCP:
    Esta clase se agregó SIN modificar BaseProcesador ni código cliente.
    Futuras clases (ProcesadorConUmbral, etc.) siguen el mismo patrón.
    """
    def __init__(self, amplificacion):
        """
        Sobreescribe el constructor de la clase abstracta para inicializar el valor de amplificacion
        :param amplificacion: Factor de amplificación a aplicar
        """
        super().__init__()
        self._amplificacion = amplificacion

    def procesar(self, senial):
        """
        Implementa el procesamiento de amplificar cada valor de senial
        :param senial: Señal a procesar
        """
        print(f"Procesando amplificación (factor {self._amplificacion}x)...")

        # 🔄 TRANSFERENCIA CORRECTA: Usar métodos públicos para compatibilidad LSP
        # Procesar cada valor y agregarlo usando el metodo apropiado
        for i in range(senial.obtener_tamanio()):
            valor_original = senial.obtener_valor(i)
            valor_amplificado = self._amplificar(valor_original)
            self._senial.poner_valor(valor_amplificado)

    def _amplificar(self, valor):
        """
        Función que amplifica un valor por el factor establecido

        🛡️ CORRECCIÓN DEFENSIVA: Manejo de valores None
        Esta validación es necesaria debido a violaciones LSP en SenialCola
        que inicializa con [None] * tamanio, causando que obtener_valor()
        devuelva None para posiciones no llenadas.

        ⚠️ NOTA DIDÁCTICA: Esta corrección NO arregla el anti-patrón,
        solo evita el crash para permitir la demostración educativa.

        :param valor: Valor a amplificar (puede ser None debido a LSP violado)
        :return: Valor amplificado o 0.0 si el valor es None
        """
        if valor is None:
            # 🛡️ Manejo defensivo: SenialCola puede devolver None
            # Esto es consecuencia directa de violaciones LSP en el dominio
            return 0.0
        return valor * self._amplificacion

class ProcesadorConUmbral(BaseProcesador):
    """
    🚧 ESTRATEGIA CONCRETA - Filtrado por umbral configurable.

    📚 REFERENCIA OCP:
    docs/IMPLEMENTACION DE OCP CON ABSTRACCIONES.md - "Nuevos Tipos sin Modificación"
    Segunda implementación que demuestra OCP: extensión sin tocar código existente.

    🎯 RESPONSABILIDAD ESPECÍFICA (SRP):
    Filtrar valores de la señal por umbral configurable:
    - Valores < umbral: se mantienen
    - Valores >= umbral: se ponen en 0

    ✅ CUMPLE LSP:
    - Intercambiable con ProcesadorAmplificador y cualquier BaseProcesador
    - Respeta el contrato abstracto completamente
    - Comportamiento consistente: filtrado determinístico

    🔄 BENEFICIO OCP DEMOSTRADO:
    Esta clase se agregó DESPUÉS de ProcesadorAmplificador sin:
    - Modificar BaseProcesador
    - Modificar ProcesadorAmplificador
    - Modificar código que usa procesadores (Lanzador, Configurador)
    - Romper tests existentes
    """
    def __init__(self, umbral):
        """
        Sobreescribe el constructor de la clase abstracta para inicializar el umbral
        :param umbral: Valor del umbral para filtrado
        """
        super().__init__()
        self._umbral = umbral

    def procesar(self, senial):
        """
        Implementa el procesamiento de la señal con filtrado por umbral
        :param senial: Señal a procesar
        """
        print(f"Procesando filtro por umbral ({self._umbral})...")

        # 🔄 TRANSFERENCIA CORRECTA: Usar métodos públicos para compatibilidad LSP
        # Procesar cada valor y agregarlo usando el metodo apropiado
        for i in range(senial.obtener_tamanio()):
            valor_original = senial.obtener_valor(i)
            valor_filtrado = self._funcion_umbral(valor_original)
            self._senial.poner_valor(valor_filtrado)

    def _funcion_umbral(self, valor):
        """
        Función que filtra valores según el umbral establecido

        🛡️ CORRECCIÓN DEFENSIVA: Manejo de valores None
        Esta validación es necesaria debido a violaciones LSP en SenialCola
        que puede devolver None desde obtener_valor().

        ⚠️ NOTA DIDÁCTICA: Esta corrección NO arregla el anti-patrón,
        solo evita comparaciones None < umbral que causan TypeError.

        :param valor: Valor a evaluar (puede ser None debido a LSP violado)
        :return: Valor original si es menor al umbral, 0 en caso contrario
        """
        if valor is None:
            # 🛡️ Manejo defensivo: SenialCola puede devolver None
            # Tratamos None como 0 para evitar TypeError en comparación
            return 0
        return valor if valor < self._umbral else 0

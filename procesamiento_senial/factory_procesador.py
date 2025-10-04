"""
Factory de Procesadores - Patrón Factory + Dependency Injection

Este módulo implementa el Factory Pattern especializado para la creación
de procesadores con inyección de dependencias.

🎯 PRINCIPIOS SOLID APLICADOS:
- SRP: Responsabilidad única - crear procesadores configurados
- OCP: Extensible para nuevos tipos sin modificar clientes
- DIP: Recibe dependencias (señal) como parámetros - inversión de control

🏗️ PATRÓN IMPLEMENTADO:
Factory especializado que conoce solo el dominio de procesamiento,
delegando la decisión de QUÉ señal usar al Configurador (nivel superior).

Versión: 1.0.0 - Factory Local con DIP
Autor: Victor Valotto
"""
from typing import Dict, Any

from procesamiento_senial.procesador import (
    BaseProcesador,
    ProcesadorAmplificador,
    ProcesadorConUmbral
)
from dominio_senial.senial import SenialBase


class FactoryProcesador:
    """
    ✅ Factory especializado para procesadores.

    📖 RESPONSABILIDAD ÚNICA:
    Crear instancias de procesadores con configuración específica,
    inyectando las dependencias que vienen del Configurador.

    ✅ DIP APLICADO:
    - Recibe señal como parámetro (abstracción SenialBase)
    - No decide QUÉ tipo de señal usar (responsabilidad del Configurador)
    - Solo ensambla el procesador con sus dependencias

    🔄 EXTENSIBILIDAD:
    Agregar nuevos tipos de procesador solo requiere modificar este factory,
    sin afectar al Configurador ni a otros componentes.
    """

    @staticmethod
    def crear(tipo_procesador: str, config: Dict[str, Any], senial: SenialBase) -> BaseProcesador:
        """
        🏭 FACTORY METHOD - Crea procesador con dependencias inyectadas.

        📖 DIP EXPLÍCITO:
        La señal es INYECTADA desde el exterior (Configurador), no creada aquí.
        El factory solo ensambla el procesador con sus dependencias.

        🎯 PARÁMETROS:
        :param tipo_procesador: Tipo de procesador a crear
            - 'amplificador': Amplificación por factor configurable
            - 'umbral': Filtrado por umbral configurable
        :param config: Diccionario con configuración específica del tipo
            - Para 'amplificador': {'factor': float}
            - Para 'umbral': {'umbral': float}
        :param senial: Instancia de señal INYECTADA (SenialBase)

        :return: Procesador configurado con dependencias inyectadas
        :rtype: BaseProcesador
        :raises ValueError: Si el tipo no está soportado

        🧪 EJEMPLO DE USO:
        ```python
        # Configurador decide la señal (DIP)
        senial = SenialCola()

        # Factory ensambla con la señal inyectada
        procesador = FactoryProcesador.crear(
            tipo_procesador='amplificador',
            config={'factor': 4.0},
            senial=senial  # ← Inyección de dependencia
        )
        ```
        """
        procesador = None

        if tipo_procesador == 'amplificador':
            # Crear procesador amplificador
            factor = config.get('factor', 2.0)
            procesador = ProcesadorAmplificador(factor)
            # ✅ Inyección de dependencia explícita
            procesador._senial = senial

        elif tipo_procesador == 'umbral':
            # Crear procesador con umbral
            umbral = config.get('umbral', 5.0)
            procesador = ProcesadorConUmbral(umbral)
            # ✅ Inyección de dependencia explícita
            procesador._senial = senial

        else:
            raise ValueError(
                f"Tipo de procesador no soportado: '{tipo_procesador}'. "
                f"Valores válidos: 'amplificador', 'umbral'"
            )

        return procesador

"""
Factory de Señales - Patrón Factory + Configuración Externa

Este módulo implementa el Factory Pattern especializado para la creación
de señales con diferentes estructuras de datos (Lista, Pila, Cola).

🎯 PRINCIPIOS SOLID APLICADOS:
- SRP: Responsabilidad única - crear señales configuradas
- OCP: Extensible para nuevos tipos sin modificar clientes
- LSP: Todas las señales son intercambiables (SenialBase)

🏗️ PATRÓN IMPLEMENTADO:
Factory especializado que crea instancias de señales según configuración externa,
permitiendo que el Configurador decida el tipo de colección a usar.

Versión: 1.0.0 - Factory de Dominio
Autor: Victor Valotto
"""
from typing import Dict, Any

from dominio_senial.senial import (
    SenialBase,
    SenialLista,
    SenialPila,
    SenialCola
)


class FactorySenial:
    """
    ✅ Factory especializado para señales.

    📖 RESPONSABILIDAD ÚNICA:
    Crear instancias de señales con estructura de datos específica,
    según la configuración externa (JSON).

    ✅ LSP GARANTIZADO:
    Todas las señales creadas implementan SenialBase y son
    completamente intercambiables polimórficamente.

    🔄 EXTENSIBILIDAD:
    Agregar nuevos tipos de señal solo requiere modificar este factory,
    sin afectar al Configurador ni a otros componentes.
    """

    @staticmethod
    def crear(tipo_senial: str, config: Dict[str, Any]) -> SenialBase:
        """
        🏭 FACTORY METHOD - Crea señal con estructura específica.

        📖 CONFIGURACIÓN EXTERNA:
        El tipo y parámetros vienen de configuración externa (JSON),
        permitiendo cambiar la estructura de datos sin modificar código.

        🎯 PARÁMETROS:
        :param tipo_senial: Tipo de señal a crear
            - 'lista': Señal con comportamiento de lista dinámica
            - 'pila': Señal con comportamiento LIFO (Last In, First Out)
            - 'cola': Señal con comportamiento FIFO (First In, First Out)
        :param config: Diccionario con configuración específica del tipo
            - Para todos: {'tamanio': int}  (opcional, default: 10)

        :return: Señal configurada (SenialBase)
        :rtype: SenialBase
        :raises ValueError: Si el tipo no está soportado

        🧪 EJEMPLO DE USO:
        ```python
        # Configuración desde JSON
        config = {'tamanio': 20}

        # Factory crea señal según tipo
        senial = FactorySenial.crear('lista', config)
        # ✅ Retorna SenialLista(20)
        ```

        📋 CONFIGURACIÓN JSON EJEMPLO:
        ```json
        {
          "senial_adquisicion": {
            "tipo": "pila",
            "tamanio": 15
          },
          "senial_procesamiento": {
            "tipo": "cola",
            "tamanio": 20
          }
        }
        ```
        """
        senial = None

        # Extraer tamaño con valor por defecto
        tamanio = config.get('tamanio', 10)

        if tipo_senial == 'lista':
            # Crear señal con comportamiento de lista
            senial = SenialLista(tamanio)

        elif tipo_senial == 'pila':
            # Crear señal con comportamiento LIFO
            senial = SenialPila(tamanio)

        elif tipo_senial == 'cola':
            # Crear señal con comportamiento FIFO (cola circular)
            senial = SenialCola(tamanio)

        else:
            raise ValueError(
                f"Tipo de señal no soportado: '{tipo_senial}'. "
                f"Valores válidos: 'lista', 'pila', 'cola'"
            )

        return senial

"""
Factory de Contextos - Patrón Factory + Strategy Pattern

Este módulo implementa el Factory Pattern especializado para la creación
de contextos de persistencia con diferentes estrategias de almacenamiento.

🎯 PRINCIPIOS SOLID APLICADOS:
- SRP: Responsabilidad única - crear contextos de persistencia
- OCP: Extensible para nuevos tipos sin modificar clientes
- LSP: Todos los contextos son intercambiables (BaseContexto)
- DIP: Configuración externa determina el tipo

🏗️ PATRÓN IMPLEMENTADO:
Factory especializado que crea instancias de contextos según configuración externa,
permitiendo que el Configurador/Repositorio decida la estrategia de persistencia.

Versión: 1.0.0 - Factory de Infraestructura
Autor: Victor Valotto
"""
from typing import Dict, Any

from persistidor_senial.contexto import (
    BaseContexto,
    ContextoPickle,
    ContextoArchivo
)


class FactoryContexto:
    """
    ✅ Factory especializado para contextos de persistencia.

    📖 RESPONSABILIDAD ÚNICA:
    Crear instancias de contextos con estrategia de almacenamiento específica,
    según la configuración externa (JSON).

    ✅ STRATEGY PATTERN:
    Cada contexto implementa una estrategia diferente de persistencia:
    - ContextoPickle: Serialización binaria (rápida, eficiente)
    - ContextoArchivo: Texto plano (human-readable, debuggeable)

    🔄 EXTENSIBILIDAD:
    Agregar nuevos tipos de contexto (BD, Cloud, etc.) solo requiere
    modificar este factory, sin afectar al Configurador ni Repositorios.
    """

    @staticmethod
    def crear(tipo_contexto: str, config: Dict[str, Any]) -> BaseContexto:
        """
        🏭 FACTORY METHOD - Crea contexto con estrategia específica.

        📖 CONFIGURACIÓN EXTERNA:
        El tipo y parámetros vienen de configuración externa (JSON),
        permitiendo cambiar la estrategia de persistencia sin modificar código.

        🎯 PARÁMETROS:
        :param tipo_contexto: Tipo de contexto a crear
            - 'pickle': Serialización binaria con pickle
            - 'archivo': Archivos de texto plano con mapeador
        :param config: Diccionario con configuración específica del tipo
            - Para todos: {'recurso': str}  (path del directorio)

        :return: Contexto configurado (BaseContexto)
        :rtype: BaseContexto
        :raises ValueError: Si el tipo no está soportado
        :raises ValueError: Si falta el parámetro 'recurso'

        🧪 EJEMPLO DE USO:
        ```python
        # Configuración desde JSON
        config = {'recurso': './datos_persistidos/adquisicion'}

        # Factory crea contexto según tipo
        contexto = FactoryContexto.crear('pickle', config)
        # ✅ Retorna ContextoPickle('./datos_persistidos/adquisicion')
        ```

        📋 CONFIGURACIÓN JSON EJEMPLO:
        ```json
        {
          "contexto_adquisicion": {
            "tipo": "archivo",
            "recurso": "./datos_persistidos/adquisicion"
          },
          "contexto_procesamiento": {
            "tipo": "pickle",
            "recurso": "./datos_persistidos/procesamiento"
          }
        }
        ```

        🔄 ESTRATEGIAS DE PERSISTENCIA:

        **ContextoPickle** (tipo='pickle'):
        - ✅ Serialización binaria rápida
        - ✅ Preserva estructura completa del objeto
        - ✅ Reconstrucción automática
        - ❌ No human-readable
        - 📁 Extensión: .pickle

        **ContextoArchivo** (tipo='archivo'):
        - ✅ Formato de texto plano
        - ✅ Human-readable para debugging
        - ✅ Soporta listas y colecciones
        - ❌ Más lento que pickle
        - 📁 Extensión: .dat
        """
        contexto = None

        # Extraer recurso (obligatorio)
        recurso = config.get('recurso')
        if not recurso:
            raise ValueError(
                "Falta parámetro obligatorio 'recurso' en la configuración del contexto"
            )

        if tipo_contexto == 'pickle':
            # Crear contexto con serialización binaria
            contexto = ContextoPickle(recurso)

        elif tipo_contexto == 'archivo':
            # Crear contexto con archivos de texto plano
            contexto = ContextoArchivo(recurso)

        else:
            raise ValueError(
                f"Tipo de contexto no soportado: '{tipo_contexto}'. "
                f"Valores válidos: 'pickle', 'archivo'"
            )

        return contexto

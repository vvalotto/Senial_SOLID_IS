"""
Factory de Adquisidores - Patrón Factory + Dependency Injection

Este módulo implementa el Factory Pattern especializado para la creación
de adquisidores con inyección de dependencias.

🎯 PRINCIPIOS SOLID APLICADOS:
- SRP: Responsabilidad única - crear adquisidores configurados
- OCP: Extensible para nuevos tipos sin modificar clientes
- DIP: Recibe dependencias (señal) como parámetros - inversión de control

🏗️ PATRÓN IMPLEMENTADO:
Factory especializado que conoce solo el dominio de adquisición,
delegando la decisión de QUÉ señal usar al Configurador (nivel superior).

Versión: 1.0.0 - Factory Local con DIP
Autor: Victor Valotto
"""
from typing import Dict, Any

from adquisicion_senial.adquisidor import (
    BaseAdquisidor,
    AdquisidorConsola,
    AdquisidorArchivo,
    AdquisidorSenoidal
)
from dominio_senial.senial import SenialBase


class FactoryAdquisidor:
    """
    ✅ Factory especializado para adquisidores.

    📖 RESPONSABILIDAD ÚNICA:
    Crear instancias de adquisidores con configuración específica,
    inyectando las dependencias que vienen del Configurador.

    ✅ DIP APLICADO:
    - Recibe señal como parámetro (abstracción SenialBase)
    - No decide QUÉ tipo de señal usar (responsabilidad del Configurador)
    - Solo ensambla el adquisidor con sus dependencias

    🔄 EXTENSIBILIDAD:
    Agregar nuevos tipos de adquisidor solo requiere modificar este factory,
    sin afectar al Configurador ni a otros componentes.
    """

    @staticmethod
    def crear(tipo_adquisidor: str, config: Dict[str, Any], senial: SenialBase) -> BaseAdquisidor:
        """
        🏭 FACTORY METHOD - Crea adquisidor con dependencias inyectadas.

        📖 DIP EXPLÍCITO:
        La señal es INYECTADA desde el exterior (Configurador), no creada aquí.
        El factory solo ensambla el adquisidor con sus dependencias.

        🎯 PARÁMETROS:
        :param tipo_adquisidor: Tipo de adquisidor a crear
            - 'consola': Entrada interactiva desde teclado
            - 'archivo': Lectura desde archivo de datos
            - 'senoidal': Generación de señal senoidal sintética
        :param config: Diccionario con configuración específica del tipo
            - Para 'consola': {'num_muestras': int}
            - Para 'archivo': {'ruta': str}
            - Para 'senoidal': {} (no requiere config adicional)
        :param senial: Instancia de señal INYECTADA (SenialBase)

        :return: Adquisidor configurado con dependencias inyectadas
        :rtype: BaseAdquisidor
        :raises ValueError: Si el tipo no está soportado

        🧪 EJEMPLO DE USO:
        ```python
        # Configurador decide la señal (DIP)
        senial = SenialLista()

        # Factory ensambla con la señal inyectada
        adquisidor = FactoryAdquisidor.crear(
            tipo_adquisidor='archivo',
            config={'ruta': 'senial.txt'},
            senial=senial  # ← Inyección de dependencia
        )
        ```
        """
        adquisidor = None

        if tipo_adquisidor == 'consola':
            # Crear adquisidor de consola
            num_muestras = config.get('num_muestras', 5)
            adquisidor = AdquisidorConsola(num_muestras)
            # ✅ Inyección de dependencia explícita
            adquisidor._senial = senial

        elif tipo_adquisidor == 'archivo':
            # Crear adquisidor de archivo
            ruta = config.get('ruta', 'senial.txt')
            adquisidor = AdquisidorArchivo(ruta)
            # ✅ Inyección de dependencia explícita
            adquisidor._senial = senial

        elif tipo_adquisidor == 'senoidal':
            # Crear adquisidor senoidal (generador sintético)
            num_muestras = config.get('num_muestras', 20)
            adquisidor = AdquisidorSenoidal(num_muestras)
            # ✅ Inyección de dependencia explícita
            adquisidor._senial = senial

        else:
            raise ValueError(
                f"Tipo de adquisidor no soportado: '{tipo_adquisidor}'. "
                f"Valores válidos: 'consola', 'archivo', 'senoidal'"
            )

        return adquisidor

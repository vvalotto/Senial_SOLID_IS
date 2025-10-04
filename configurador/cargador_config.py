"""
Cargador de Configuración Externa - DIP Aplicado

Este módulo implementa la carga de configuración desde archivo JSON externo,
completando la aplicación del principio DIP (Dependency Inversion Principle).

🎯 PRINCIPIOS SOLID APLICADOS:
- DIP: Configuración externa determina las dependencias
- SRP: Responsabilidad única - leer y validar configuración
- OCP: Extensible para nuevos formatos (YAML, TOML)

📚 MIGRACIÓN XML → JSON:
Este módulo reemplaza la lectura XML (minidom.parse) de versiones anteriores
con una implementación JSON moderna y más mantenible.

Versión: 1.0.0 - DIP con configuración externa JSON
Autor: Victor Valotto
"""
import json
from pathlib import Path
from typing import Dict, Any


class CargadorConfig:
    """
    ✅ Cargador de configuración externa desde JSON.

    📖 RESPONSABILIDAD ÚNICA:
    Leer, validar y proporcionar acceso a la configuración del sistema
    desde archivo JSON externo.

    🎯 DIP APLICADO:
    El sistema no decide sus dependencias - la configuración externa lo hace.
    """

    def __init__(self, ruta_config: str = None):
        """
        Inicializa el cargador con la ruta al archivo de configuración.

        Si no se proporciona ruta, busca config.json en el mismo directorio
        que este módulo, independientemente de desde dónde se ejecute.

        :param ruta_config: Ruta al archivo JSON de configuración (opcional)
        """
        if ruta_config is None:
            # Determinar ruta relativa al módulo configurador, no al CWD
            modulo_dir = Path(__file__).parent
            self.ruta_config = modulo_dir / 'config.json'
        else:
            self.ruta_config = Path(ruta_config)
        self._config = None

    def cargar(self) -> Dict[str, Any]:
        """
        Carga la configuración desde el archivo JSON.

        :return: Diccionario con toda la configuración
        :raises FileNotFoundError: Si el archivo no existe
        :raises json.JSONDecodeError: Si el JSON es inválido
        """
        if not self.ruta_config.exists():
            raise FileNotFoundError(
                f"Archivo de configuración no encontrado: {self.ruta_config}"
            )

        with open(self.ruta_config, 'r', encoding='utf-8') as f:
            self._config = json.load(f)

        return self._config

    def obtener_dir_datos(self) -> str:
        """
        Obtiene el directorio de recursos de datos.
        JSON: "dir_recurso_datos": "./tmp/datos"
        :return: Path del directorio de datos
        """
        if self._config is None:
            self.cargar()
        return self._config.get('dir_recurso_datos', './tmp/datos')

    def obtener_config_senial_adquisidor(self) -> Dict[str, Any]:
        """
        Retorna configuración de señal para adquisidor.
        JSON: "senial_adquisidor": {"tipo": "cola", "tamanio": 20}
        :return: {'tipo': str, 'tamanio': int}
        """
        if self._config is None:
            self.cargar()
        return self._config.get('senial_adquisidor', {'tipo': 'lista', 'tamanio': 10})

    def obtener_config_senial_procesador(self) -> Dict[str, Any]:
        """
        Retorna configuración de señal para procesador.
        JSON: "senial_procesador": {"tipo": "pila", "tamanio": 20}
        :return: {'tipo': str, 'tamanio': int}
        """
        if self._config is None:
            self.cargar()
        return self._config.get('senial_procesador', {'tipo': 'lista', 'tamanio': 10})

    def obtener_config_adquisidor(self) -> Dict[str, Any]:
        """
        Retorna configuración de adquisidor.
        JSON: "adquisidor": {"tipo": "archivo", "ruta_archivo": "./adquisidor/datos.txt"}
        :return: {'tipo': str, 'ruta_archivo': str, ...}
        """
        if self._config is None:
            self.cargar()
        return self._config.get('adquisidor', {'tipo': 'consola', 'num_muestras': 5})

    def obtener_config_procesador(self) -> Dict[str, Any]:
        """
        Retorna configuración de procesador.
        JSON: "procesador": {"tipo": "umbral", "umbral": 100}
        :return: {'tipo': str, 'factor': float, 'umbral': float, ...}
        """
        if self._config is None:
            self.cargar()
        return self._config.get('procesador', {'tipo': 'amplificador', 'factor': 4.0})

    def obtener_config_contexto_adquisicion(self) -> Dict[str, Any]:
        """
        Retorna configuración de contexto de adquisición.
        JSON: "contexto_adquisicion": {"tipo": "pickle", "recurso": "./tmp/datos/adquisicion"}
        :return: {'tipo': str, 'recurso': str}
        """
        if self._config is None:
            self.cargar()
        return self._config.get('contexto_adquisicion', {
            'tipo': 'pickle',
            'recurso': './tmp/datos/adquisicion'
        })

    def obtener_config_contexto_procesamiento(self) -> Dict[str, Any]:
        """
        Retorna configuración de contexto de procesamiento.
        JSON: "contexto_procesamiento": {"tipo": "pickle", "recurso": "./tmp/datos/procesamiento"}
        :return: {'tipo': str, 'recurso': str}
        """
        if self._config is None:
            self.cargar()
        return self._config.get('contexto_procesamiento', {
            'tipo': 'pickle',
            'recurso': './tmp/datos/procesamiento'
        })

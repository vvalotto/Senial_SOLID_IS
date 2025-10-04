# CARGADOR CONFIG - Gestión de Configuración Externa JSON

**Proyecto**: Senial SOLID IS
**Autor**: Victor Valotto
**Fecha**: Octubre 2024
**Versión**: 1.0.0
**Objetivo**: Documentar la implementación del CargadorConfig como componente responsable de leer y validar configuración externa JSON

---

## 📋 Resumen Ejecutivo

Este documento presenta la **arquitectura del CargadorConfig**, el componente central responsable de **leer, validar y proporcionar acceso** a la configuración externa del sistema desde archivos JSON. El CargadorConfig implementa **SRP (Single Responsibility Principle)** en su forma más pura y habilita la aplicación completa de **DIP (Dependency Inversion Principle)**.

### 🎯 **Responsabilidad Única**

```
CargadorConfig: SOLO leer y validar configuración JSON
- NO crea objetos
- NO toma decisiones de negocio
- NO orquesta flujos
- SOLO proporciona datos de configuración
```

### 🔄 **Migración XML → JSON**

```
v2.0: minidom.parse("configuracion.xml")
v3.0: CargadorConfig("config.json")

Antes: Parsing XML con minidom
Después: Parsing JSON nativo de Python
```

---

## 🎯 Responsabilidad del CargadorConfig

### Definición SRP

> **CargadorConfig tiene UNA responsabilidad: Leer y proporcionar configuración desde JSON**

### Lo que SÍ hace

✅ **Leer archivo JSON** desde disco
✅ **Validar formato JSON** (syntax)
✅ **Proporcionar acceso** a secciones de configuración
✅ **Fallbacks** para valores no encontrados
✅ **Ruta dinámica** usando `__file__`

### Lo que NO hace

❌ **NO crea objetos** (delegado a Factories)
❌ **NO toma decisiones** de negocio (delegado a Configurador)
❌ **NO orquesta flujos** (delegado a Lanzador)
❌ **NO valida semántica** de valores (cada componente valida sus datos)
❌ **NO persiste configuración** (read-only)

---

## 🏗️ Arquitectura del CargadorConfig

### Ubicación en la Arquitectura DIP

```
┌────────────────────────────────────────┐
│         config.json                    │
│    (Configuración Externa)             │
└─────────────────┬──────────────────────┘
                  ↓ leído por
┌─────────────────────────────────────────┐
│       CargadorConfig                    │  ← ESTE COMPONENTE
│   (SRP: Leer y validar JSON)            │
│   - cargar()                            │
│   - obtener_config_*()                  │
│   - Ruta dinámica con __file__          │
└─────────────────┬───────────────────────┘
                  ↓ usado por (singleton)
┌─────────────────────────────────────────┐
│       Configurador                      │
│   _cargador = CargadorConfig()          │
│   Delega a Factories                    │
└─────────────────────────────────────────┘
```

### Patrón Singleton en Configurador

```python
# CargadorConfig se instancia UNA vez como singleton
class Configurador:
    _cargador = None  # Singleton

    @staticmethod
    def inicializar_configuracion(ruta_config: str = None):
        # Crear instancia única
        Configurador._cargador = CargadorConfig(ruta_config)
        Configurador._cargador.cargar()

    @staticmethod
    def crear_adquisidor():
        # Usar instancia singleton
        config = Configurador._cargador.obtener_config_adquisidor()
        # ...
```

---

## 💻 Implementación Completa

### Código del CargadorConfig

```python
"""
Cargador de Configuración Externa - DIP Aplicado

Responsabilidad única: Leer y validar configuración JSON
"""
import json
from pathlib import Path
from typing import Dict, Any


class CargadorConfig:
    """
    ✅ SRP: Leer y validar configuración JSON
    ✅ DIP: Proporciona datos para inversión de dependencias

    NO crea objetos, NO toma decisiones de negocio
    """

    def __init__(self, ruta_config: str = None):
        """
        Inicializa el cargador con ruta al archivo de configuración.

        🎯 RUTA DINÁMICA:
        Si no se proporciona ruta, busca config.json en el mismo
        directorio que este módulo (usando __file__), independientemente
        de desde dónde se ejecute el lanzador.

        :param ruta_config: Ruta al archivo JSON (None = default)
        """
        if ruta_config is None:
            # Ruta relativa al módulo configurador, NO al CWD
            modulo_dir = Path(__file__).parent
            self.ruta_config = modulo_dir / 'config.json'
        else:
            self.ruta_config = Path(ruta_config)

        self._config = None  # Cache de configuración

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

    # =========================================================================
    # MÉTODOS DE ACCESO A CONFIGURACIÓN
    # =========================================================================

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

        JSON:
        "senial_adquisidor": {
          "tipo": "cola",
          "tamanio": 20
        }

        :return: {'tipo': str, 'tamanio': int}
        """
        if self._config is None:
            self.cargar()
        return self._config.get('senial_adquisidor', {
            'tipo': 'lista',
            'tamanio': 10
        })

    def obtener_config_senial_procesador(self) -> Dict[str, Any]:
        """
        Retorna configuración de señal para procesador.

        JSON:
        "senial_procesador": {
          "tipo": "pila",
          "tamanio": 20
        }

        :return: {'tipo': str, 'tamanio': int}
        """
        if self._config is None:
            self.cargar()
        return self._config.get('senial_procesador', {
            'tipo': 'lista',
            'tamanio': 10
        })

    def obtener_config_adquisidor(self) -> Dict[str, Any]:
        """
        Retorna configuración de adquisidor.

        JSON:
        "adquisidor": {
          "tipo": "archivo",
          "ruta_archivo": "senial.txt"
        }

        :return: {'tipo': str, 'ruta_archivo': str, 'num_muestras': int, ...}
        """
        if self._config is None:
            self.cargar()
        return self._config.get('adquisidor', {
            'tipo': 'consola',
            'num_muestras': 5
        })

    def obtener_config_procesador(self) -> Dict[str, Any]:
        """
        Retorna configuración de procesador.

        JSON:
        "procesador": {
          "tipo": "umbral",
          "umbral": 100
        }

        :return: {'tipo': str, 'factor': float, 'umbral': int, ...}
        """
        if self._config is None:
            self.cargar()
        return self._config.get('procesador', {
            'tipo': 'amplificador',
            'factor': 4.0
        })

    def obtener_config_contexto_adquisicion(self) -> Dict[str, Any]:
        """
        Retorna configuración de contexto de adquisición.

        JSON:
        "contexto_adquisicion": {
          "tipo": "pickle",
          "recurso": "./tmp/datos/adquisicion"
        }

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

        JSON:
        "contexto_procesamiento": {
          "tipo": "pickle",
          "recurso": "./tmp/datos/procesamiento"
        }

        :return: {'tipo': str, 'recurso': str}
        """
        if self._config is None:
            self.cargar()
        return self._config.get('contexto_procesamiento', {
            'tipo': 'pickle',
            'recurso': './tmp/datos/procesamiento'
        })
```

---

## 🎯 Características Clave

### 1. Ruta Dinámica con `__file__`

#### Problema: Dependencia del CWD

```python
# ❌ PROBLEMA: Ruta relativa al CWD (Current Working Directory)
ruta_config = Path('./configurador/config.json')

# Ejecutar desde raíz:
cd /Users/victor/proyecto
python3 lanzador.py  # ✓ Encuentra ./configurador/config.json

# Ejecutar desde /tmp:
cd /tmp
python3 -m lanzador.lanzador  # ✗ NO encuentra ./configurador/config.json
```

#### Solución: Ruta Relativa al Módulo

```python
# ✅ SOLUCIÓN: Ruta relativa al módulo usando __file__
if ruta_config is None:
    modulo_dir = Path(__file__).parent  # Directorio del módulo
    self.ruta_config = modulo_dir / 'config.json'

# __file__ = /Users/victor/proyecto/configurador/cargador_config.py
# modulo_dir = /Users/victor/proyecto/configurador
# ruta_config = /Users/victor/proyecto/configurador/config.json

# ✓ Funciona desde cualquier directorio
```

#### Pruebas de Portabilidad

```bash
# Test 1: Desde raíz del proyecto
cd /Users/victor/proyecto
python3 -m lanzador.lanzador
# → ✅ Encuentra: /Users/victor/proyecto/configurador/config.json

# Test 2: Desde /tmp
cd /tmp
python3 -c "import sys; sys.path.insert(0, '/Users/victor/proyecto'); from lanzador import Lanzador; Lanzador.ejecutar()"
# → ✅ Encuentra: /Users/victor/proyecto/configurador/config.json

# Test 3: Desde subdirectorio
cd /Users/victor/proyecto/docs
python3 -m lanzador.lanzador
# → ✅ Encuentra: /Users/victor/proyecto/configurador/config.json
```

### 2. Lazy Loading

```python
# Configuración se carga solo cuando se necesita
def obtener_config_adquisidor(self) -> Dict[str, Any]:
    if self._config is None:  # ← Lazy loading
        self.cargar()
    return self._config.get('adquisidor', {...})
```

**Ventajas:**
- ✅ No carga JSON innecesariamente
- ✅ Permite crear instancia sin archivo (testing)
- ✅ Cache en memoria después de primera carga

### 3. Fallbacks Defensivos

```python
# Valores por defecto si sección no existe
return self._config.get('procesador', {
    'tipo': 'amplificador',  # ← Fallback
    'factor': 4.0
})
```

**Ventajas:**
- ✅ Sistema robusto ante JSON incompleto
- ✅ No falla por sección faltante
- ✅ Valores sensatos por defecto

### 4. Validación de Sintaxis

```python
# json.load() valida sintaxis automáticamente
with open(self.ruta_config, 'r', encoding='utf-8') as f:
    self._config = json.load(f)
    # → JSONDecodeError si sintaxis inválida
```

**Ejemplos de errores detectados:**

```json
// ❌ Error: Coma extra
{
  "procesador": {
    "tipo": "amplificador",
  }
}
// → JSONDecodeError: Expecting property name

// ❌ Error: Comillas simples
{
  'procesador': {
    'tipo': 'amplificador'
  }
}
// → JSONDecodeError: Expecting property name

// ❌ Error: Número como string cuando debe ser int
{
  "adquisidor": {
    "num_muestras": "20"  // ← String, debería ser número
  }
}
// → Causa error posterior en comparación: '<' not supported between 'int' and 'str'
```

---

## 📊 Estructura del config.json

### Esquema Completo

```json
{
  "version": "1.0.0",
  "descripcion": "Configuración externa del sistema - DIP aplicado",

  "dir_recurso_datos": "./tmp/datos",

  "senial_adquisidor": {
    "tipo": "lista|pila|cola",
    "tamanio": 20
  },

  "senial_procesador": {
    "tipo": "lista|pila|cola",
    "tamanio": 20
  },

  "adquisidor": {
    "tipo": "consola|archivo|senoidal",
    "num_muestras": 20,
    "ruta_archivo": "senial.txt"
  },

  "procesador": {
    "tipo": "amplificador|umbral",
    "factor": 4.0,
    "umbral": 100
  },

  "contexto_adquisicion": {
    "tipo": "pickle|archivo",
    "recurso": "./tmp/datos/adquisicion"
  },

  "contexto_procesamiento": {
    "tipo": "pickle|archivo",
    "recurso": "./tmp/datos/procesamiento"
  }
}
```

### Tipos de Datos

| Campo | Tipo Python | Ejemplo JSON |
|-------|-------------|--------------|
| `version` | `str` | `"1.0.0"` |
| `tipo` (señal/adq/proc) | `str` | `"lista"` |
| `tamanio` | `int` | `20` |
| `num_muestras` | `int` | `20` |
| `ruta_archivo` | `str` | `"senial.txt"` |
| `factor` | `float` | `4.0` |
| `umbral` | `int` | `100` |
| `recurso` | `str` | `"./tmp/datos"` |

⚠️ **IMPORTANTE**: Los números deben ser números, NO strings:

```json
// ✅ CORRECTO
"num_muestras": 20

// ❌ INCORRECTO
"num_muestras": "20"
```

---

## 🔄 Flujo de Uso

### Inicialización en Configurador

```python
# Paso 1: Configurador inicializa CargadorConfig (singleton)
class Configurador:
    _cargador = None

    @staticmethod
    def inicializar_configuracion(ruta_config: str = None):
        Configurador._cargador = CargadorConfig(ruta_config)
        Configurador._cargador.cargar()
        print(f"✅ Configuración cargada desde {Configurador._cargador.ruta_config}")
```

### Uso en Métodos del Configurador

```python
# Paso 2: Configurador usa CargadorConfig para obtener datos
@staticmethod
def crear_adquisidor():
    # Obtener configuración desde CargadorConfig
    config = Configurador._cargador.obtener_config_adquisidor()
    tipo = config.get('tipo', 'archivo')

    # Obtener señal
    senial = Configurador.crear_senial_adquisidor()

    # Delegar a Factory
    return FactoryAdquisidor.crear(tipo, config, senial)
```

### Inicialización en Lanzador

```python
# Paso 3: Lanzador inicializa configuración al inicio
class Lanzador:
    @staticmethod
    def ejecutar():
        # PASO 0: Inicializar configuración externa
        try:
            Configurador.inicializar_configuracion()  # ← Sin ruta = usa default
            print("✅ Configuración cargada desde config.json")
        except FileNotFoundError:
            print("⚠️  config.json no encontrado - usando fallbacks")

        # PASO 1: Crear componentes (ya configurados desde JSON)
        adquisidor = Configurador.crear_adquisidor()
        procesador = Configurador.crear_procesador()
        # ...
```

---

## 🎯 Principios SOLID Aplicados

### SRP (Single Responsibility Principle)

✅ **Una responsabilidad: Leer JSON**

**Razones para cambiar CargadorConfig:**
1. Cambiar formato de configuración (JSON → YAML → TOML)

**NO son razones para cambiar:**
- ❌ Agregar nuevo tipo de señal → Modificar Factory
- ❌ Agregar nuevo tipo de adquisidor → Modificar Factory
- ❌ Cambiar lógica de orquestación → Modificar Lanzador
- ❌ Cambiar lógica de creación → Modificar Configurador

### OCP (Open/Closed Principle)

✅ **Extensible para nuevas secciones**

```python
# Agregar nueva sección de configuración:
def obtener_config_visualizador(self) -> Dict[str, Any]:
    if self._config is None:
        self.cargar()
    return self._config.get('visualizador', {
        'tipo': 'consola',
        'formato': 'tabla'
    })
# ← Un método, sin modificar métodos existentes
```

### DIP (Dependency Inversion Principle)

✅ **Habilita inversión de dependencias**

```
CargadorConfig NO depende de:
- ❌ Factories (no los conoce)
- ❌ Clases concretas de señales (no las conoce)
- ❌ Lógica de negocio (no la conoce)

CargadorConfig SOLO depende de:
- ✅ Librería json (estándar Python)
- ✅ Librería pathlib (estándar Python)
```

---

## 🧪 Testing del CargadorConfig

### Tests Unitarios

```python
import pytest
import json
from pathlib import Path
from configurador.cargador_config import CargadorConfig


def test_cargador_carga_json_existente(tmp_path):
    """Test: Carga correcta de JSON válido"""
    # Crear archivo temporal
    config_file = tmp_path / "config.json"
    config_data = {
        "senial_adquisidor": {"tipo": "lista", "tamanio": 20},
        "adquisidor": {"tipo": "archivo", "ruta_archivo": "test.txt"}
    }
    config_file.write_text(json.dumps(config_data))

    # Cargar configuración
    cargador = CargadorConfig(str(config_file))
    config = cargador.cargar()

    assert config == config_data


def test_cargador_lanza_error_archivo_no_existe():
    """Test: FileNotFoundError si archivo no existe"""
    cargador = CargadorConfig("/ruta/inexistente/config.json")

    with pytest.raises(FileNotFoundError) as excinfo:
        cargador.cargar()

    assert "Archivo de configuración no encontrado" in str(excinfo.value)


def test_cargador_lanza_error_json_invalido(tmp_path):
    """Test: JSONDecodeError si JSON es inválido"""
    # Crear archivo con JSON inválido
    config_file = tmp_path / "invalid.json"
    config_file.write_text("{invalid json")

    cargador = CargadorConfig(str(config_file))

    with pytest.raises(json.JSONDecodeError):
        cargador.cargar()


def test_cargador_retorna_fallback_seccion_no_existe(tmp_path):
    """Test: Retorna fallback si sección no existe"""
    # Crear JSON sin sección 'procesador'
    config_file = tmp_path / "config.json"
    config_data = {
        "senial_adquisidor": {"tipo": "lista", "tamanio": 20}
    }
    config_file.write_text(json.dumps(config_data))

    cargador = CargadorConfig(str(config_file))
    cargador.cargar()

    # Obtener configuración de procesador (no existe en JSON)
    config_procesador = cargador.obtener_config_procesador()

    # Debe retornar fallback
    assert config_procesador == {
        'tipo': 'amplificador',
        'factor': 4.0
    }


def test_cargador_lazy_loading(tmp_path):
    """Test: Lazy loading - solo carga cuando se necesita"""
    config_file = tmp_path / "config.json"
    config_data = {"test": "value"}
    config_file.write_text(json.dumps(config_data))

    cargador = CargadorConfig(str(config_file))

    # No ha cargado aún
    assert cargador._config is None

    # Primera llamada: carga
    config = cargador.obtener_config_adquisidor()

    # Ahora está cargado
    assert cargador._config is not None


def test_cargador_ruta_dinamica():
    """Test: Ruta dinámica con __file__ funciona correctamente"""
    # Sin especificar ruta (usa default)
    cargador = CargadorConfig()

    # Debe construir ruta relativa al módulo
    assert 'configurador' in str(cargador.ruta_config)
    assert cargador.ruta_config.name == 'config.json'
```

### Integración con Configurador

```python
def test_configurador_usa_cargador():
    """Test: Configurador inicializa y usa CargadorConfig"""
    from configurador import Configurador

    # Inicializar configuración
    Configurador.inicializar_configuracion()

    # Verificar que cargador está inicializado
    assert Configurador._cargador is not None
    assert Configurador._cargador._config is not None

    # Crear componentes usando configuración
    adquisidor = Configurador.crear_adquisidor()
    procesador = Configurador.crear_procesador()

    assert adquisidor is not None
    assert procesador is not None
```

---

## 📚 Lecciones Aprendidas

### ✅ **Hacer (Best Practices)**

1. **Ruta Dinámica**: Usar `Path(__file__).parent` para portabilidad
2. **Lazy Loading**: Cargar configuración solo cuando se necesita
3. **Fallbacks**: Proveer valores por defecto sensatos
4. **Validación**: Dejar que `json.load()` valide sintaxis
5. **Singleton**: Instanciar una vez en Configurador
6. **Encapsulación**: Configuración en `_config` (privado)
7. **Tipos Correctos**: Números como números, NO strings
8. **Documentación**: Docstrings claros con formato JSON esperado

### ❌ **Evitar (Anti-Patterns)**

1. **CWD Dependence**: NO usar rutas relativas al CWD
2. **Eager Loading**: NO cargar JSON en `__init__`
3. **Sin Fallbacks**: NO fallar si sección no existe
4. **Múltiples Instancias**: NO crear varias instancias de CargadorConfig
5. **Hardcoding**: NO hardcodear rutas absolutas
6. **Strings como Números**: NO usar `"20"` cuando debe ser `20`
7. **Responsabilidades Mixtas**: CargadorConfig NO debe crear objetos
8. **Sin Validación**: NO asumir que JSON siempre es válido

---

## 🔮 Evolución Futura

### v2.0 - Validación de Esquemas

```python
import jsonschema

class CargadorConfig:
    SCHEMA = {
        "type": "object",
        "properties": {
            "senial_adquisidor": {
                "type": "object",
                "properties": {
                    "tipo": {"type": "string", "enum": ["lista", "pila", "cola"]},
                    "tamanio": {"type": "integer", "minimum": 1}
                },
                "required": ["tipo", "tamanio"]
            },
            # ...
        }
    }

    def cargar(self) -> Dict[str, Any]:
        with open(self.ruta_config, 'r', encoding='utf-8') as f:
            self._config = json.load(f)

        # Validar contra esquema
        jsonschema.validate(self._config, self.SCHEMA)

        return self._config
```

### v3.0 - Soporte Múltiples Formatos

```python
class CargadorConfig:
    def cargar(self) -> Dict[str, Any]:
        ext = self.ruta_config.suffix

        if ext == '.json':
            return self._cargar_json()
        elif ext == '.yaml':
            return self._cargar_yaml()
        elif ext == '.toml':
            return self._cargar_toml()
        else:
            raise ValueError(f"Formato no soportado: {ext}")
```

### v4.0 - Configuración por Entorno

```python
class CargadorConfig:
    def __init__(self, ruta_config: str = None, env: str = None):
        self.env = env or os.getenv('ENV', 'development')

        if ruta_config is None:
            modulo_dir = Path(__file__).parent
            # Buscar config.{env}.json (ej: config.production.json)
            self.ruta_config = modulo_dir / f'config.{self.env}.json'

            # Fallback a config.json
            if not self.ruta_config.exists():
                self.ruta_config = modulo_dir / 'config.json'
```

---

## 📖 Conclusión

El **CargadorConfig** es un componente fundamental que habilita la aplicación completa de **DIP (Dependency Inversion Principle)** en el sistema. Al separar completamente la responsabilidad de **leer configuración** de la responsabilidad de **crear objetos** y **orquestar flujos**, logramos:

1. ✅ **SRP Perfecto**: Una responsabilidad - leer JSON
2. ✅ **Portabilidad**: Ruta dinámica con `__file__`
3. ✅ **Robustez**: Fallbacks defensivos
4. ✅ **Simplicidad**: API clara con métodos `obtener_config_*()`
5. ✅ **Testabilidad**: Fácil de testear aisladamente
6. ✅ **DIP Habilitado**: Configuración externa determina dependencias

**El CargadorConfig demuestra que la configuración externa no es solo una conveniencia - es un componente arquitectónico clave para invertir el flujo de dependencias y lograr sistemas verdaderamente flexibles y mantenibles.**

---

**📖 Documento Técnico - CargadorConfig**
**Victor Valotto - Octubre 2024**
**v1.0.0 - Gestión de Configuración Externa JSON**

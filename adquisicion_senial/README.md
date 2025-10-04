# 📡 Adquisición Señal - Factory Pattern + Configuración Externa

**Versión**: 3.0.0 - Factory + DIP + Configuración Externa JSON
**Autor**: Victor Valotto
**Responsabilidad**: Adquisición de datos desde múltiples fuentes usando Strategy + Factory Pattern

Paquete independiente que implementa **adquisición extensible** de señales digitales con **Factory especializado** e **inyección de dependencias** preparado para configuración externa JSON.

## 📋 Descripción

Este paquete implementa la **capa de adquisición** usando el **patrón Strategy**, permitiendo capturar datos desde múltiples fuentes sin modificar código existente. Demuestra la aplicación correcta del **OCP (Open/Closed Principle)**.

## 🎯 Principios SOLID Aplicados

### ✅ SRP (Single Responsibility Principle)
- **Una responsabilidad**: Adquisición de datos de señales digitales
- **Cada adquisidor**: Un método específico de captura

### ✅ OCP (Open/Closed Principle)
- **Abierto para extensión**: Nuevos tipos de adquisidores sin modificar existentes
- **Cerrado para modificación**: Código probado permanece intacto
- **Mecanismo**: Abstracciones + herencia + polimorfismo

### ✅ LSP (Liskov Substitution Principle)
- **Intercambiabilidad**: Cualquier adquisidor funciona polimórficamente
- **Contrato consistente**: Todas las implementaciones cumplen `BaseAdquisidor`

### ✅ DIP (Dependency Inversion Principle)
- **Depende de abstracción**: `self._senial: SenialBase` (no implementaciones concretas)
- **Inyección de dependencias**: El `Configurador` inyecta el tipo concreto (`SenialLista`, `SenialPila`, `SenialCola`)
- **Flexibilidad**: Cambiar tipo de señal sin modificar el adquisidor

## 🏗️ Arquitectura Strategy Pattern

### 📦 Estructura del Paquete

```
adquisicion_senial/
├── __init__.py              # Exporta BaseAdquisidor, Adquisidores, FactoryAdquisidor
├── adquisidor.py            # Implementación de Strategy Pattern
├── factory_adquisidor.py    # ✨ Factory especializado con DIP
├── setup.py                # Configuración del paquete independiente
├── README.md               # Documentación completa
└── tests/                  # Tests unitarios polimórficos
    └── test_adquisidor.py
```

### 🏗️ Clases y Jerarquía

```python
📊 Arquitectura OCP
┌─────────────────────────────────────┐
│         BaseAdquisidor              │ ← Abstracción (Strategy)
│  + obtener_senial_adquirida()       │
│  + leer_senial() [abstracto]        │
└─────────────────────────────────────┘
           ▲                    ▲
           │                    │
┌─────────────────┐    ┌─────────────────┐
│AdquisidorConsola│    │AdquisidorArchivo│ ← Implementaciones concretas
│+ leer_senial()  │    │+ leer_senial()  │
└─────────────────┘    └─────────────────┘
```

## 📦 Implementaciones Disponibles

### 🔹 BaseAdquisidor (Estrategia Abstracta)

```python
from abc import ABCMeta, abstractmethod
from dominio_senial.senial import SenialBase

class BaseAdquisidor(metaclass=ABCMeta):
    """Contrato común para todos los adquisidores"""

    def __init__(self, numero_muestras):
        # ✅ DIP: Depende de abstracción, no de implementación concreta
        self._senial: SenialBase = None  # Inyectado por Configurador
        self._numero_muestras = numero_muestras

    @abstractmethod
    def leer_senial(self):
        """Método que debe implementar cada adquisidor específico"""
        pass

    def obtener_senial_adquirida(self):
        """Método común para obtener la señal"""
        return self._senial
```

### 🔹 AdquisidorConsola (Entrada Interactiva)

**Responsabilidad**: Captura datos desde teclado con validación.

```python
class AdquisidorConsola(BaseAdquisidor):
    """Adquisidor de datos desde consola interactiva"""

    def __init__(self, numero_muestras):
        super().__init__(numero_muestras)

    def leer_senial(self):
        """Implementación específica para entrada desde consola"""
        # Pide input al usuario con validación
```

### 🔹 AdquisidorArchivo (Lectura de Archivos)

**Responsabilidad**: Captura datos desde archivos de texto.

```python
class AdquisidorArchivo(BaseAdquisidor):
    """Adquisidor de datos desde archivos"""

    def __init__(self, ruta_archivo):
        super().__init__(0)  # Tamaño se determina del archivo
        self._ruta_archivo = ruta_archivo

    def leer_senial(self):
        """Implementación específica para lectura de archivos"""
        # Lee valores línea por línea con manejo de errores
```

### 🔹 AdquisidorSenoidal (Generador Sintético)

**Responsabilidad**: Genera señal senoidal sintética matemáticamente.

```python
class AdquisidorSenoidal(BaseAdquisidor):
    """Generador de señal senoidal para testing y simulaciones"""

    def __init__(self, numero_muestras: int = 10):
        super().__init__(numero_muestras)
        self._valor = 0.0
        self._i = 0

    def leer_senial(self):
        """Genera valores senoidales calculados: sin((i/N) * 2π) * 10"""
        # Genera muestras senoidales automáticamente
```

## 🏭 Factory Pattern - Inyección de Dependencias

### 🔹 FactoryAdquisidor (Creación con DIP)

**Versión**: 3.0.0 - Factory especializado con inyección de dependencias
**Responsabilidad**: Crear adquisidores con configuración externa e inyección de señal

```python
from typing import Dict, Any
from adquisicion_senial.factory_adquisidor import FactoryAdquisidor
from dominio_senial import SenialBase

class FactoryAdquisidor:
    """
    ✅ Factory especializado para adquisidores.

    🎯 DIP APLICADO:
    - Recibe señal como parámetro (abstracción SenialBase)
    - NO decide QUÉ tipo de señal usar (responsabilidad del Configurador)
    - Solo ensambla el adquisidor con sus dependencias

    📖 CONFIGURACIÓN EXTERNA:
    - Valores vienen de JSON externo
    - config.get() con valores por defecto seguros
    - Preparado para IoC Container
    """

    @staticmethod
    def crear(tipo_adquisidor: str, config: Dict[str, Any], senial: SenialBase):
        """
        Crea adquisidor con dependencias inyectadas.

        :param tipo_adquisidor: 'consola', 'archivo', 'senoidal'
        :param config: Diccionario con configuración (desde JSON)
        :param senial: Señal INYECTADA desde el Configurador
        :return: Adquisidor configurado
        """
        if tipo_adquisidor == 'consola':
            num_muestras = config.get('num_muestras', 5)  # ← Default si JSON no lo especifica
            adquisidor = AdquisidorConsola(num_muestras)
            adquisidor._senial = senial  # ← Inyección de dependencia
            return adquisidor

        elif tipo_adquisidor == 'archivo':
            ruta = config.get('ruta', 'senial.txt')  # ← Default si JSON no lo especifica
            adquisidor = AdquisidorArchivo(ruta)
            adquisidor._senial = senial  # ← Inyección de dependencia
            return adquisidor

        elif tipo_adquisidor == 'senoidal':
            num_muestras = config.get('num_muestras', 20)  # ← Default si JSON no lo especifica
            adquisidor = AdquisidorSenoidal(num_muestras)
            adquisidor._senial = senial  # ← Inyección de dependencia
            return adquisidor

        else:
            raise ValueError(f"Tipo no soportado: '{tipo_adquisidor}'")
```

### 📋 Configuración Externa JSON (Preparado)

**Arquitectura de configuración externa:**

```json
{
  "adquisidor": {
    "tipo": "consola",
    "num_muestras": 5
  }
}
```

**Flujo de inyección de dependencias:**

```
📄 config.json          →    🏭 Configurador (Lee JSON)    →    🔧 Factory (Recibe config)
{                            |                                    |
  "adquisidor": {            | config = json_data['adquisidor']   | crear(tipo, config, señal)
    "tipo": "consola",       |                                    |
    "num_muestras": 5        | señal = SenialLista()              | num_muestras = config.get(...)
  }                          |                                    |
}                            ▼                                    ▼
                        Pasa dict config                    Ensambla con señal inyectada
```

**Valores por defecto seguros:**

El método `config.get(clave, default)` proporciona valores de respaldo:

```python
# Si JSON tiene el valor
config = {'num_muestras': 10}
num_muestras = config.get('num_muestras', 5)  # → 10 (del JSON)

# Si JSON NO tiene el valor
config = {}
num_muestras = config.get('num_muestras', 5)  # → 5 (default seguro)
```

**Beneficios de esta arquitectura:**

- ✅ **Configuración externa**: Cambiar comportamiento sin modificar código
- ✅ **Valores seguros**: Defaults si configuración incompleta
- ✅ **DIP aplicado**: Factory recibe dependencias, no las crea
- ✅ **Testeable**: Fácil inyectar mocks para testing
- ✅ **Extensible**: Preparado para IoC Container futuro

## 🚀 Instalación

```bash
# Como paquete independiente
pip install adquisicion-senial

# O como parte del proyecto completo
pip install -e .

# Dependencias
pip install dominio-senial>=1.0.0
```

## 💻 Uso y Ejemplos

### Ejemplo Básico - Polimorfismo

```python
from adquisicion_senial import BaseAdquisidor, AdquisidorConsola, AdquisidorArchivo

# ✅ POLIMORFISMO: Cualquier adquisidor funciona igual
def procesar_con_adquisidor(adquisidor: BaseAdquisidor):
    """Función genérica que funciona con cualquier adquisidor"""
    adquisidor.leer_senial()
    senial = adquisidor.obtener_senial_adquirida()
    print(f"📊 Adquiridas {senial.obtener_tamanio()} muestras")
    return senial

# Uso intercambiable
adq_consola = AdquisidorConsola(5)
adq_archivo = AdquisidorArchivo('senial.txt')

# ✅ MISMO CÓDIGO funciona con diferentes implementaciones
senial1 = procesar_con_adquisidor(adq_consola)
senial2 = procesar_con_adquisidor(adq_archivo)
```

### Ejemplo Consola Interactiva

```python
from adquisicion_senial import AdquisidorConsola

# Crear adquisidor para 3 muestras
adquisidor = AdquisidorConsola(3)

# Capturar datos (solicita input al usuario)
print("📡 Iniciando adquisición desde consola...")
adquisidor.leer_senial()

# Obtener resultado
senial = adquisidor.obtener_senial_adquirida()
print(f"✅ Capturadas {senial.obtener_tamanio()} muestras")
```

### Ejemplo Lectura desde Archivo

```python
from adquisicion_senial import AdquisidorArchivo

# Crear archivo con datos
# senial.txt:
# 1.5
# 2.8
# 3.2

# Adquisidor desde archivo
adquisidor = AdquisidorArchivo('senial.txt')

# Leer automáticamente
print("📁 Iniciando adquisición desde archivo...")
adquisidor.leer_senial()

# Obtener resultado
senial = adquisidor.obtener_senial_adquirida()
print(f"✅ Leídas {senial.obtener_tamanio()} muestras del archivo")
```

### Ejemplo de Extensión (OCP)

```python
# ✅ EXTENSIÓN SIN MODIFICAR código existente
class AdquisidorRandom(BaseAdquisidor):
    """Nuevo adquisidor que genera datos aleatorios"""

    def __init__(self, numero_muestras, rango=(0, 10)):
        super().__init__(numero_muestras)
        self._rango = rango

    def leer_senial(self):
        """Implementación específica para datos aleatorios"""
        import random
        print(f"🎲 Generando {self._numero_muestras} valores aleatorios...")
        for i in range(self._numero_muestras):
            valor = random.uniform(*self._rango)
            self._senial.poner_valor(valor)
            print(f"  Muestra {i}: {valor:.2f}")

# ✅ FUNCIONA automáticamente con código existente
adq_random = AdquisidorRandom(4, rango=(1, 5))
senial_random = procesar_con_adquisidor(adq_random)  # ¡Sin modificar función!
```

## 🏗️ Uso del Factory con Inyección de Dependencias

### Ejemplo 1: Uso directo del Factory

```python
from adquisicion_senial import FactoryAdquisidor
from dominio_senial import SenialLista

# 1. Configurador decide el tipo de señal (DIP - nivel superior)
senial = SenialLista()

# 2. Configuración puede venir de JSON
config_consola = {'num_muestras': 5}
config_archivo = {'ruta': 'datos.txt'}
config_senoidal = {'num_muestras': 20}

# 3. Factory ensambla con dependencias inyectadas
adq_consola = FactoryAdquisidor.crear('consola', config_consola, senial)
adq_archivo = FactoryAdquisidor.crear('archivo', config_archivo, senial)
adq_senoidal = FactoryAdquisidor.crear('senoidal', config_senoidal, senial)

# 4. Usar adquisidor
adq_archivo.leer_senial()
senial_adquirida = adq_archivo.obtener_senial_adquirida()
```

### Ejemplo 2: Con configuración JSON (preparado)

```python
import json
from adquisicion_senial import FactoryAdquisidor
from dominio_senial import SenialLista

# 1. Leer configuración externa
with open('config.json', 'r') as f:
    json_config = json.load(f)

# 2. Extraer configuración del adquisidor
adq_config = json_config['adquisidor']
tipo = adq_config['tipo']           # 'archivo'
params = adq_config                 # {'tipo': 'archivo', 'ruta': 'datos.txt'}

# 3. Configurador decide señal (separación de responsabilidades)
senial = SenialLista()

# 4. Factory crea con config externa + señal inyectada
adquisidor = FactoryAdquisidor.crear(tipo, params, senial)

# 5. Usar
adquisidor.leer_senial()
```

### Ejemplo 3: Valores por defecto seguros

```python
# Si JSON está incompleto, el factory usa defaults
config_incompleto = {}  # Sin 'num_muestras' ni 'ruta'

# ✅ Factory usa valores por defecto seguros
adq = FactoryAdquisidor.crear('consola', config_incompleto, senial)
# → num_muestras = 5 (default del factory)

adq = FactoryAdquisidor.crear('archivo', config_incompleto, senial)
# → ruta = 'senial.txt' (default del factory)
```

## 🧪 Testing Polimórfico

```bash
# Ejecutar tests del paquete
cd adquisicion_senial
pytest tests/ -v

# Tests específicos por implementación
pytest tests/test_adquisidor.py::test_adquisidor_consola -v
pytest tests/test_adquisidor.py::test_adquisidor_archivo -v
```

### Ejemplo de Test OCP

```python
import pytest
from adquisicion_senial import BaseAdquisidor, AdquisidorConsola, AdquisidorArchivo

class TestOCP:
    """Tests que validan el cumplimiento del OCP"""

    def test_todos_adquisidores_son_intercambiables(self):
        """Valida que todos los adquisidores cumplen LSP"""
        adquisidores = [
            AdquisidorConsola(3),
            AdquisidorArchivo('test_data.txt'),
            # ✅ FUTURO: Agregar AdquisidorRandom sin cambiar test
        ]

        for adquisidor in adquisidores:
            # ✅ POLIMORFISMO: Mismo interface para todos
            assert isinstance(adquisidor, BaseAdquisidor)
            assert hasattr(adquisidor, 'leer_senial')
            assert hasattr(adquisidor, 'obtener_senial_adquirida')
```

## 📈 Métricas de Extensibilidad

### Agregar Nuevo Adquisidor
- **Líneas de código a modificar**: 0 (solo crear nueva clase)
- **Tests existentes afectados**: 0
- **Tiempo de integración**: < 30 minutos
- **Riesgo de regresión**: 0%

### Comparación Antes/Después OCP

```python
# ❌ ANTES (violación OCP): Modificar clase existente
class Adquisidor:
    def __init__(self, tipo="consola"):
        if tipo == "archivo":  # ← Modificación requerida
            # Nueva lógica aquí

# ✅ DESPUÉS (cumple OCP): Solo agregar nueva clase
class AdquisidorNuevo(BaseAdquisidor):
    def leer_senial(self):
        # Nueva implementación sin tocar código existente
```

## 🔮 Extensiones Futuras Preparadas

```python
# ✅ Listas para implementar sin modificar código existente

class AdquisidorSensor(BaseAdquisidor):
    """Adquisición desde sensores IoT"""

class AdquisidorAPI(BaseAdquisidor):
    """Adquisición desde APIs REST"""

class AdquisidorBD(BaseAdquisidor):
    """Adquisición desde bases de datos"""

class AdquisidorRed(BaseAdquisidor):
    """Adquisición desde sockets de red"""
```

## 🎯 Valor Didáctico

### Conceptos Demostrados

1. **Strategy Pattern**: Algoritmos intercambiables en tiempo de ejecución
2. **Factory Pattern**: Creación centralizada con inyección de dependencias
3. **OCP Práctico**: Extensión real sin modificación de código existente
4. **DIP Aplicado**: Inyección de dependencias (señal) + Configuración externa (JSON)
5. **Polimorfismo**: Un interfaz, múltiples implementaciones
6. **Abstracciones**: Contratos estables que facilitan extensibilidad
7. **LSP**: Intercambiabilidad garantizada

### Lecciones Aprendidas

- **Las abstracciones bien diseñadas** facilitan extensibilidad infinita
- **El polimorfismo elimina** condicionales y facilita testing
- **OCP reduce riesgos** al agregar funcionalidad nueva
- **Factory + DIP** separan creación de uso y permiten configuración externa
- **Valores por defecto seguros** (`config.get()`) hacen el sistema robusto
- **Inyección de dependencias** facilita testing y flexibilidad

### Evolución del Paquete

| Versión | Características | Principios |
|---------|----------------|------------|
| **1.0** | Clases concretas básicas | - |
| **2.0** | Strategy Pattern + Abstracciones | SRP, OCP, LSP |
| **2.1** | DIP - Inyección de tipo de señal | + DIP |
| **3.0** | Factory + Configuración Externa | + Factory Pattern |

---

**📡 Paquete Adquisición - Victor Valotto**
**📖 Proyecto Didáctico**: Demostración de SOLID + Factory Pattern + DIP
**🎯 Extensibilidad**: Configuración externa JSON + Inyección de dependencias
**🏭 Arquitectura**: Strategy + Factory + Dependency Injection
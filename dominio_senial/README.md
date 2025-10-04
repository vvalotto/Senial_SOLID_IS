# 🏠 Dominio Señal - Entidades del Dominio

**Versión**: 4.0.0 - LSP Completo + Arquitectura Limpia
**Autor**: Victor Valotto
**Responsabilidad**: Entidades fundamentales del dominio de señales digitales

Paquete independiente que implementa el **núcleo del dominio** en la arquitectura de procesamiento de señales, siguiendo principios SOLID y Clean Architecture.

## ⚠️ BREAKING CHANGES v4.0.0

- **Eliminado alias `Senial`** - Usar clases específicas explícitamente
- **Nueva jerarquía LSP** - `SenialBase` como abstracción, implementaciones `SenialLista`, `SenialPila`, `SenialCola`
- **Intercambiabilidad garantizada** - 100% polimorfismo funcional

## 📋 Descripción

Este paquete representa la **capa más interna** de la arquitectura, conteniendo únicamente las entidades esenciales del dominio de señales digitales. Es completamente independiente de infraestructura, frameworks o librerías externas.

## 🎯 Responsabilidad Única (SRP)

**Una única razón para cambiar**: Modificaciones en las entidades del dominio de señales digitales.

## 🏗️ Arquitectura LSP v4.0.0

### Jerarquía de Clases

```
SenialBase (ABC)
├── Abstracción con contrato común
├── Métodos abstractos obligatorios
└── Propiedades comunes

    ├── SenialLista (Concreta)
    │   └── Comportamiento: Lista dinámica
    │
    ├── SenialPila (Concreta)
    │   └── Comportamiento: LIFO (Last In, First Out)
    │
    └── SenialCola (Concreta)
        └── Comportamiento: FIFO (First In, First Out)
```

## 📦 Entidades del Dominio

### 🔹 Clase Abstracta `SenialBase`

**Responsabilidad**: Definir el contrato común para todas las señales.

```python
from abc import ABC, abstractmethod
from typing import Optional

class SenialBase(ABC):
    """Abstracción base que define el contrato para todas las señales"""

    def __init__(self, tamanio: int = 10)

    # Propiedades comunes
    @property
    def fecha_adquisicion(self) -> Any
    @property
    def cantidad(self) -> int
    @property
    def tamanio(self) -> int

    # Métodos abstractos (obligatorios)
    @abstractmethod
    def poner_valor(self, valor: float) -> None

    @abstractmethod
    def sacar_valor(self) -> Optional[float]

    @abstractmethod
    def limpiar(self) -> None

    @abstractmethod
    def obtener_valor(self, indice: int) -> Optional[float]

    @abstractmethod
    def obtener_tamanio(self) -> int
```

### ✅ Implementaciones Concretas

#### 1. **SenialLista** - Lista Dinámica

```python
from dominio_senial import SenialLista

# Comportamiento: Acceso secuencial y por índice
lista = SenialLista()
lista.poner_valor(1.0)
lista.poner_valor(2.0)
lista.sacar_valor()  # → 2.0 (extrae del final)
```

#### 2. **SenialPila** - LIFO

```python
from dominio_senial import SenialPila

# Comportamiento: Last In, First Out
pila = SenialPila()
pila.poner_valor(1.0)
pila.poner_valor(2.0)
pila.poner_valor(3.0)
pila.sacar_valor()  # → 3.0 (último ingresado)
```

#### 3. **SenialCola** - FIFO (Cola Circular)

```python
from dominio_senial import SenialCola

# Comportamiento: First In, First Out
cola = SenialCola()
cola.poner_valor(1.0)
cola.poner_valor(2.0)
cola.poner_valor(3.0)
cola.sacar_valor()  # → 1.0 (primero ingresado)
```

## 🚀 Instalación

```bash
# Como paquete independiente
pip install dominio-senial

# O como parte del proyecto completo
pip install -e .
```

## 💻 Uso y Ejemplos

### Ejemplo 1: Polimorfismo LSP

```python
from dominio_senial import SenialBase, SenialLista, SenialPila, SenialCola

def procesar_cualquier_senial(senial: SenialBase):
    """✅ Función genérica que funciona con CUALQUIER tipo de señal"""
    senial.poner_valor(10.0)
    senial.poner_valor(20.0)
    senial.poner_valor(30.0)

    print(f"Tamaño: {senial.obtener_tamanio()}")
    valor = senial.sacar_valor()
    print(f"Extraído: {valor}")

# ✅ Funciona con las 3 implementaciones
for tipo in [SenialLista, SenialPila, SenialCola]:
    print(f"\n{tipo.__name__}:")
    procesar_cualquier_senial(tipo())
```

### Ejemplo 2: Factory Pattern

```python
from dominio_senial import SenialBase, SenialLista, SenialPila, SenialCola

def crear_senial(tipo: str, tamanio: int = 10) -> SenialBase:
    """✅ Factory uniforme para todas las señales"""
    tipos = {
        'lista': SenialLista,
        'pila': SenialPila,
        'cola': SenialCola
    }
    return tipos[tipo](tamanio)

# ✅ Todas instanciables uniformemente
lista = crear_senial('lista')
pila = crear_senial('pila')
cola = crear_senial('cola')
```

### Ejemplo 3: Testing Genérico

```python
import pytest
from dominio_senial import SenialBase, SenialLista, SenialPila, SenialCola

@pytest.mark.parametrize("tipo_senial", [
    SenialLista,
    SenialPila,
    SenialCola
])
def test_contrato_base(tipo_senial):
    """✅ Test único para todas las implementaciones"""
    senial = tipo_senial()

    # Test del contrato común
    senial.poner_valor(42.0)
    assert senial.obtener_tamanio() == 1

    valor = senial.sacar_valor()
    assert valor == 42.0
    assert senial.obtener_tamanio() == 0
```

## 🏗️ Posición en la Arquitectura

### Clean Architecture - Capa de Dominio

```
🏗️ Arquitectura del Sistema
┌─────────────────────────────────────────┐
│                UI/CLI                   │ ← lanzador
├─────────────────────────────────────────┤
│           Use Cases                     │ ← configurador
├─────────────────────────────────────────┤
│     Interface Adapters                  │ ← adquisicion, procesamiento, presentacion
├─────────────────────────────────────────┤
│          🏠 DOMINIO 🏠                  │ ← dominio_senial (ESTE PAQUETE)
│     SenialBase + Implementaciones       │    v4.0.0 - LSP Completo
└─────────────────────────────────────────┘
```

### Principios SOLID Aplicados

- **✅ SRP**: Una responsabilidad - gestionar entidades de señales
- **✅ OCP**: Extensible sin modificación - agregar nuevas señales sin tocar la base
- **✅ LSP**: Intercambiabilidad garantizada - todas las señales funcionan polimórficamente
- **⭐ Estabilidad**: Centro estable - todos los demás paquetes dependen de este
- **🚫 Independencia**: No depende de ningún otro paquete

## 🧪 Testing

```bash
# Ejecutar tests del dominio
cd dominio_senial
pytest tests/

# Tests específicos
pytest tests/test_senial.py -v

# Cobertura
pytest tests/ --cov=dominio_senial --cov-report=html
```

### Tests LSP Incluidos

```python
def test_constructores_uniformes():
    """✅ Todos los constructores funcionan sin parámetros"""
    lista = SenialLista()
    pila = SenialPila()
    cola = SenialCola()  # v4.0.0: ahora con parámetro opcional

    assert all(isinstance(s, SenialBase) for s in [lista, pila, cola])

def test_firmas_consistentes():
    """✅ sacar_valor() sin parámetros en todas"""
    señales = [SenialLista(), SenialPila(), SenialCola()]

    for senial in señales:
        senial.poner_valor(100.0)
        valor = senial.sacar_valor()  # ✅ Sin parámetros
        assert valor == 100.0
```

## 🔗 Integración con Otros Paquetes

```python
# ✅ v4.0.0: Integración con DIP (Dependency Inversion)
from dominio_senial import SenialBase

# Paquete adquisicion_senial
class BaseAdquisidor:
    def __init__(self):
        self._senial: SenialBase = None  # ✅ Depende de abstracción
        # Tipo concreto inyectado por Configurador

# Paquete procesamiento_senial
class BaseProcesador:
    def __init__(self):
        self._senial: SenialBase = None  # ✅ Depende de abstracción
        # Tipo concreto inyectado por Configurador

# Paquete presentacion_senial
class Visualizador:
    def mostrar_datos(self, senial: SenialBase):  # ✅ Acepta abstracción
        # Lógica de visualización polimórfica
        for i in range(senial.obtener_tamanio()):
            print(senial.obtener_valor(i))
```

## 📈 Métricas de Calidad v4.0.0

### Complejidad
- **Clases**: 4 (`SenialBase`, `SenialLista`, `SenialPila`, `SenialCola`)
- **Métodos públicos por clase**: 8-10
- **Dependencias**: 0 (solo Python estándar + `abc` + `typing`)
- **Líneas de código**: ~420

### Cobertura de Tests
- **Cobertura objetivo**: 100%
- **Tests LSP**: Constructores, firmas, polimorfismo, factory pattern
- **Tests específicos**: Cada implementación con su semántica

### Métricas LSP
- **Violaciones LSP**: 0 (antes: 4 críticas)
- **Intercambiabilidad**: 100% (antes: 0%)
- **Uso de `isinstance`**: 0 (antes: 1 anti-patrón)
- **Factory Pattern**: Funcional (antes: roto)

## 🎓 Valor Didáctico

### Conceptos Demostrados v4.0.0

1. **✅ LSP Aplicado**: Intercambiabilidad polimórfica garantizada
2. **✅ Abstracción Correcta**: `SenialBase` define contrato robusto
3. **✅ Contratos Consistentes**: Firmas idénticas en todas las subclases
4. **✅ Semánticas Específicas**: LIFO vs FIFO respetando el contrato
5. **✅ Eliminación de Anti-patrones**: Sin `isinstance`, sin alias confusos

### Evolución del Proyecto

| Versión | Estado | Características |
|---------|--------|-----------------|
| v1.0.0 | Inicial | Clase `Senial` concreta básica |
| v2.0.0 | Violaciones | Herencia con violaciones LSP |
| v3.0.0 | Análisis | Violaciones documentadas |
| **v4.0.0** | **LSP Completo** | **Abstracción + Implementaciones correctas** |

### Lecciones Aprendidas

- **Las abstracciones deben definir contratos claros** con métodos abstractos
- **Firmas consistentes son esenciales** para intercambiabilidad
- **Semánticas diferentes no violan LSP** si respetan el contrato
- **Eliminar alias confusos** mejora la claridad arquitectural
- **Testing genérico valida LSP** - un test funciona con todas las implementaciones

## 📚 Documentación Relacionada

- **`docs/VIOLACIONES DE LSP EN TIPOS DE SEÑAL.md`** - Análisis de problemas (versión anterior)
- **`docs/SOLUCION LSP CON ABSTRACCIONES.md`** - Solución completa v4.0.0 ⭐


**🏠 Paquete Dominio v4.0.0 - Victor Valotto**
**📖 Proyecto Didáctico**: Demostración de Clean Architecture y SOLID
**✅ LSP Completo**: Intercambiabilidad polimórfica garantizada
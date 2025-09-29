# 📡 Adquisición Señal - OCP para Captura de Datos

**Versión**: 2.0.0 (refactorizada para OCP)
**Autor**: Victor Valotto
**Responsabilidad**: Adquisición de datos desde múltiples fuentes usando Strategy Pattern

Paquete independiente que implementa **adquisición extensible** de señales digitales desde diferentes fuentes, aplicando el principio Open/Closed para máxima flexibilidad.

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

## 🏗️ Arquitectura Strategy Pattern

### 📦 Estructura del Paquete

```
adquisicion_senial/
├── __init__.py          # Exporta BaseAdquisidor, AdquisidorConsola, AdquisidorArchivo
├── adquisidor.py        # Implementación de Strategy Pattern
├── setup.py            # Configuración del paquete independiente
└── tests/              # Tests unitarios polimórficos
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

class BaseAdquisidor(metaclass=ABCMeta):
    """Contrato común para todos los adquisidores"""

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

## 🏗️ Integración con Configurador

```python
# El Configurador usa las implementaciones específicas
from configurador import Configurador

# Configuración "de fábrica" actual
adquisidor = Configurador.crear_adquisidor()  # AdquisidorArchivo('senial.txt')

# Opciones alternativas disponibles
adq_consola = Configurador.crear_adquisidor_consola()      # AdquisidorConsola(5)
adq_archivo = Configurador.crear_adquisidor_archivo('mi_archivo.txt')  # AdquisidorArchivo
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
2. **OCP Práctico**: Extensión real sin modificación de código existente
3. **Polimorfismo**: Un interfaz, múltiples implementaciones
4. **Abstracciones**: Contratos estables que facilitan extensibilidad
5. **LSP**: Intercambiabilidad garantizada

### Lecciones Aprendidas

- **Las abstracciones bien diseñadas** facilitan extensibilidad infinita
- **El polimorfismo elimina** condicionales y facilita testing
- **OCP reduce riesgos** al agregar funcionalidad nueva
- **Strategy Pattern es ideal** para familias de algoritmos relacionados

---

**📡 Paquete Adquisición - Victor Valotto**
**📖 Proyecto Didáctico**: Demostración de OCP y Strategy Pattern
**🎯 Extensibilidad**: Infinita capacidad de agregar fuentes de datos
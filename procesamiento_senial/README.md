# ⚙️ Procesamiento Señal - OCP para Algoritmos de Transformación

**Versión**: 2.1.0 - OCP + DIP Aplicado
**Autor**: Victor Valotto
**Responsabilidad**: Procesamiento y transformación de señales usando Strategy Pattern

Paquete independiente que implementa **procesamiento extensible** de señales digitales con diferentes algoritmos, aplicando el principio Open/Closed para máxima flexibilidad.

## 📋 Descripción

Este paquete implementa la **capa de procesamiento** usando el **patrón Strategy**, permitiendo aplicar diferentes algoritmos sin modificar código existente. Demuestra la aplicación correcta del **OCP (Open/Closed Principle)**.

## 🎯 Principios SOLID Aplicados

### ✅ SRP (Single Responsibility Principle)
- **Una responsabilidad**: Procesamiento y transformación de señales
- **Cada procesador**: Un algoritmo específico de transformación

### ✅ OCP (Open/Closed Principle)
- **Abierto para extensión**: Nuevos tipos de procesadores sin modificar existentes
- **Cerrado para modificación**: Código probado permanece intacto
- **Mecanismo**: Abstracciones + herencia + polimorfismo

### ✅ LSP (Liskov Substitution Principle)
- **Intercambiabilidad**: Cualquier procesador funciona polimórficamente
- **Contrato consistente**: Todas las implementaciones cumplen `BaseProcesador`

### ✅ DIP (Dependency Inversion Principle)
- **Depende de abstracción**: `self._senial: SenialBase` (no implementaciones concretas)
- **Inyección de dependencias**: El `Configurador` inyecta el tipo concreto (`SenialLista`, `SenialPila`, `SenialCola`)
- **Flexibilidad**: Cambiar tipo de señal sin modificar el procesador

## 🏗️ Arquitectura Strategy Pattern

### 📦 Estructura del Paquete

```
procesamiento_senial/
├── __init__.py          # Exporta BaseProcesador, ProcesadorAmplificador, ProcesadorConUmbral
├── procesador.py        # Implementación de Strategy Pattern
├── setup.py            # Configuración del paquete independiente
└── tests/              # Tests unitarios polimórficos
    └── test_procesador.py
```

### 🏗️ Clases y Jerarquía

```python
📊 Arquitectura OCP
┌─────────────────────────────────────┐
│         BaseProcesador              │ ← Abstracción (Strategy)
│  + obtener_senial_procesada()       │
│  + procesar(senial) [abstracto]     │
└─────────────────────────────────────┘
           ▲                    ▲
           │                    │
┌──────────────────────┐  ┌──────────────────────┐
│ProcesadorAmplificador│  │ProcesadorConUmbral  │ ← Implementaciones concretas
│+ procesar(senial)    │  │+ procesar(senial)    │
└──────────────────────┘  └──────────────────────┘
```

## 📦 Implementaciones Disponibles

### 🔹 BaseProcesador (Estrategia Abstracta)

```python
from abc import ABCMeta, abstractmethod
from dominio_senial.senial import SenialBase

class BaseProcesador(metaclass=ABCMeta):
    """Contrato común para todos los procesadores"""

    def __init__(self):
        # ✅ DIP: Depende de abstracción, no de implementación concreta
        self._senial: SenialBase = None  # Inyectado por Configurador

    @abstractmethod
    def procesar(self, senial):
        """Método que debe implementar cada procesador específico"""
        pass

    def obtener_senial_procesada(self):
        """Método común para obtener la señal procesada"""
        return self._senial
```

### 🔹 ProcesadorAmplificador (Amplificación)

**Responsabilidad**: Amplifica cada valor de la señal por un factor configurable.

```python
class ProcesadorAmplificador(BaseProcesador):
    """Procesador que amplifica valores de la señal"""

    def __init__(self, amplificacion):
        super().__init__()
        self._amplificacion = amplificacion

    def procesar(self, senial):
        """Implementación específica para amplificación"""
        for i in range(senial.obtener_tamanio()):
            valor_original = senial.obtener_valor(i)
            valor_amplificado = valor_original * self._amplificacion
            self._senial.poner_valor(valor_amplificado)
```

### 🔹 ProcesadorConUmbral (Filtrado)

**Responsabilidad**: Filtra valores por umbral (valores >= umbral se ponen en 0).

```python
class ProcesadorConUmbral(BaseProcesador):
    """Procesador que filtra valores por umbral"""

    def __init__(self, umbral):
        super().__init__()
        self._umbral = umbral

    def procesar(self, senial):
        """Implementación específica para filtrado por umbral"""
        for i in range(senial.obtener_tamanio()):
            valor_original = senial.obtener_valor(i)
            valor_filtrado = valor_original if valor_original < self._umbral else 0
            self._senial.poner_valor(valor_filtrado)
```

## 🚀 Instalación

```bash
# Como paquete independiente
pip install procesamiento-senial

# O como parte del proyecto completo
pip install -e .

# Dependencias
pip install dominio-senial>=4.0.0
```

## 💻 Uso y Ejemplos

### Ejemplo Básico - Polimorfismo

```python
from procesamiento_senial import BaseProcesador, ProcesadorAmplificador, ProcesadorConUmbral
from dominio_senial import SenialLista

# ✅ POLIMORFISMO: Cualquier procesador funciona igual
def aplicar_procesamiento(procesador: BaseProcesador, senial):
    """Función genérica que funciona con cualquier procesador"""
    procesador.procesar(senial)
    senial_procesada = procesador.obtener_senial_procesada()
    print(f"📊 Procesada: {senial_procesada.obtener_tamanio()} valores")
    return senial_procesada

# Crear señal de ejemplo
senial = SenialLista()
senial.poner_valor(1.0)
senial.poner_valor(2.0)
senial.poner_valor(3.0)

# Uso intercambiable
proc_amp = ProcesadorAmplificador(2.0)
proc_umbral = ProcesadorConUmbral(2.5)

# ✅ MISMO CÓDIGO funciona con diferentes implementaciones
senial_amp = aplicar_procesamiento(proc_amp, senial)
senial_filtrada = aplicar_procesamiento(proc_umbral, senial)
```

### Ejemplo de Extensión (OCP)

```python
# ✅ EXTENSIÓN SIN MODIFICAR código existente
class ProcesadorSuavizado(BaseProcesador):
    """Nuevo procesador que aplica suavizado (media móvil)"""

    def __init__(self, ventana=3):
        super().__init__()
        self._ventana = ventana

    def procesar(self, senial):
        """Implementación específica para suavizado"""
        tamanio = senial.obtener_tamanio()
        for i in range(tamanio):
            # Calcular media de ventana
            suma = 0
            count = 0
            for j in range(max(0, i-self._ventana+1), i+1):
                suma += senial.obtener_valor(j)
                count += 1
            valor_suavizado = suma / count
            self._senial.poner_valor(valor_suavizado)

# ✅ FUNCIONA automáticamente con código existente
proc_suavizado = ProcesadorSuavizado(ventana=2)
senial_suavizada = aplicar_procesamiento(proc_suavizado, senial)  # ¡Sin modificar función!
```

## 🏗️ Integración con Configurador

```python
# El Configurador usa las implementaciones específicas
from configurador import Configurador

# Configuración "de fábrica" actual
procesador = Configurador.crear_procesador()  # ProcesadorAmplificador(4.0)

# ✅ DIP APLICADO: El Configurador inyecta el tipo de señal específico
# procesador._senial = Configurador.crear_senial_procesador()  # → SenialCola
# Esto permite cambiar el tipo de colección sin modificar el procesador

# Opciones alternativas disponibles
proc_amp = Configurador.crear_procesador_amplificador(2.0)      # ProcesadorAmplificador
proc_umbral = Configurador.crear_procesador_con_umbral(3.5)    # ProcesadorConUmbral
```

## 🧪 Testing Polimórfico

```bash
# Ejecutar tests del paquete
cd procesamiento_senial
pytest tests/ -v

# Tests específicos por implementación
pytest tests/test_procesador.py::test_procesador_amplificador -v
pytest tests/test_procesador.py::test_procesador_con_umbral -v
```

### Ejemplo de Test OCP

```python
import pytest
from procesamiento_senial import BaseProcesador, ProcesadorAmplificador, ProcesadorConUmbral

class TestOCP:
    """Tests que validan el cumplimiento del OCP"""

    def test_todos_procesadores_son_intercambiables(self):
        """Valida que todos los procesadores cumplen LSP"""
        procesadores = [
            ProcesadorAmplificador(2.0),
            ProcesadorConUmbral(3.0),
            # ✅ FUTURO: Agregar ProcesadorSuavizado sin cambiar test
        ]

        for procesador in procesadores:
            # ✅ POLIMORFISMO: Mismo interface para todos
            assert isinstance(procesador, BaseProcesador)
            assert hasattr(procesador, 'procesar')
            assert hasattr(procesador, 'obtener_senial_procesada')
```

## 📈 Métricas de Extensibilidad

### Agregar Nuevo Procesador
- **Líneas de código a modificar**: 0 (solo crear nueva clase)
- **Tests existentes afectados**: 0
- **Tiempo de integración**: < 30 minutos
- **Riesgo de regresión**: 0%

### Comparación Antes/Después OCP

```python
# ❌ ANTES (violación OCP): Modificar clase existente
class Procesador:
    def __init__(self, tipo="amplificacion"):
        if tipo == "umbral":  # ← Modificación requerida
            # Nueva lógica aquí

# ✅ DESPUÉS (cumple OCP): Solo agregar nueva clase
class ProcesadorNuevo(BaseProcesador):
    def procesar(self, senial):
        # Nueva implementación sin tocar código existente
```

## 🔮 Extensiones Futuras Preparadas

```python
# ✅ Listas para implementar sin modificar código existente

class ProcesadorFFT(BaseProcesador):
    """Procesamiento con Transformada Rápida de Fourier"""

class ProcesadorWavelet(BaseProcesador):
    """Procesamiento con transformada Wavelet"""

class ProcesadorFiltroDigital(BaseProcesador):
    """Filtros digitales IIR/FIR"""

class ProcesadorNormalizador(BaseProcesador):
    """Normalización de señales"""
```

## 🎯 Valor Didáctico

### Conceptos Demostrados

1. **Strategy Pattern**: Algoritmos intercambiables en tiempo de ejecución
2. **OCP Práctico**: Extensión real sin modificación de código existente
3. **Polimorfismo**: Un interfaz, múltiples implementaciones
4. **Abstracciones**: Contratos estables que facilitan extensibilidad
5. **LSP**: Intercambiabilidad garantizada
6. **DIP**: Dependencia de abstracciones, no de implementaciones concretas

### Lecciones Aprendidas

- **Las abstracciones bien diseñadas** facilitan extensibilidad infinita
- **El polimorfismo elimina** condicionales y facilita testing
- **OCP reduce riesgos** al agregar funcionalidad nueva
- **Strategy Pattern es ideal** para familias de algoritmos relacionados
- **DIP permite flexibilidad** en las estructuras de datos internas

---

**⚙️ Paquete Procesamiento - Victor Valotto**
**📖 Proyecto Didáctico**: Demostración de OCP, Strategy Pattern y DIP
**🎯 Extensibilidad**: Infinita capacidad de agregar algoritmos de procesamiento
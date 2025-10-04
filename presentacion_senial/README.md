# 📊 Presentación Señal - Visualización Polimórfica

**Versión**: 2.0.0 - LSP + DIP Aplicado
**Autor**: Victor Valotto
**Responsabilidad**: Visualización de señales usando polimorfismo LSP

Paquete independiente que implementa **visualización polimórfica** de señales digitales, funcionando con cualquier tipo de señal (`SenialLista`, `SenialPila`, `SenialCola`) gracias a LSP.

## 📋 Descripción

Este paquete implementa la **capa de presentación** trabajando con la abstracción `SenialBase`, lo que le permite visualizar cualquier implementación de señal sin cambios. Demuestra la aplicación correcta de **LSP (Liskov Substitution Principle)** y **DIP (Dependency Inversion Principle)**.

## 🎯 Principios SOLID Aplicados

### ✅ SRP (Single Responsibility Principle)
- **Una responsabilidad**: Visualización de señales en consola
- **Sin lógica de negocio**: Solo presentación de datos

### ✅ LSP (Liskov Substitution Principle)
- **Acepta SenialBase**: Funciona con `SenialLista`, `SenialPila`, `SenialCola` sin cambios
- **Polimorfismo puro**: No usa `isinstance()` para diferenciar tipos
- **Contrato común**: Solo usa métodos de `SenialBase`

### ✅ DIP (Dependency Inversion Principle)
- **Depende de abstracción**: Parámetro `senial: SenialBase` (no implementaciones concretas)
- **No crea instancias**: Solo recibe señales ya creadas
- **Desacoplamiento total**: No conoce las implementaciones concretas

## 📦 Contenido

### Estructura del Paquete

```
presentacion_senial/
├── __init__.py          # Exporta la clase Visualizador
├── visualizador.py      # Visualización polimórfica
├── setup.py            # Configuración del paquete
└── tests/              # Tests polimórficos
    └── test_visualizador.py
```

### 🔹 Clase Visualizador

```python
from dominio_senial import SenialBase

class Visualizador:
    """
    Visualizador polimórfico de señales digitales.

    ✅ LSP: Funciona con cualquier SenialBase sin cambios
    ✅ DIP: Depende de abstracción, no de implementaciones concretas
    """

    def __init__(self):
        """Inicializa el visualizador de señales."""

    def mostrar_datos(self, senial: SenialBase) -> None:
        """
        Muestra los datos de una señal en formato simple.

        ✅ LSP: Acepta cualquier SenialBase (SenialLista, SenialPila, SenialCola)

        :param senial: Señal a visualizar (cualquier implementación de SenialBase)
        :raises TypeError: Si la señal no es del tipo correcto
        :raises ValueError: Si la señal está vacía
        """
        if not isinstance(senial, SenialBase):
            raise TypeError("El parámetro debe ser una instancia de SenialBase")

        if senial.obtener_tamanio() == 0:
            raise ValueError("No se puede visualizar una señal vacía")

        print("=== VISUALIZACIÓN DE SEÑAL ===")
        print(f"Número de muestras: {senial.obtener_tamanio()}")
        print("Valores de la señal:")

        for i in range(senial.obtener_tamanio()):
            valor = senial.obtener_valor(i)
            print(f"  Muestra {i}: {valor}")

        print("=" * 31)
```

## 🚀 Instalación

```bash
# Como paquete independiente
pip install presentacion-senial

# O como parte del proyecto completo
pip install -e .

# Dependencias
pip install dominio-senial>=4.0.0
```

## 💻 Uso y Ejemplos

### Ejemplo Básico - Polimorfismo LSP

```python
from presentacion_senial import Visualizador
from dominio_senial import SenialLista, SenialPila, SenialCola

# Crear visualizador
visualizador = Visualizador()

# ✅ POLIMORFISMO LSP: Funciona con CUALQUIER tipo de señal

# 1. Visualizar SenialLista
lista = SenialLista()
lista.poner_valor(1.0)
lista.poner_valor(2.5)
lista.poner_valor(3.8)
visualizador.mostrar_datos(lista)  # ✅ Funciona

# 2. Visualizar SenialPila
pila = SenialPila()
pila.poner_valor(10.0)
pila.poner_valor(20.0)
pila.poner_valor(30.0)
visualizador.mostrar_datos(pila)  # ✅ Funciona

# 3. Visualizar SenialCola
cola = SenialCola()
cola.poner_valor(100.0)
cola.poner_valor(200.0)
cola.poner_valor(300.0)
visualizador.mostrar_datos(cola)  # ✅ Funciona

# ✅ MISMO CÓDIGO para todos los tipos - ¡Eso es LSP!
```

### Ejemplo con Función Genérica

```python
from presentacion_senial import Visualizador
from dominio_senial import SenialBase, SenialLista, SenialPila, SenialCola

def procesar_y_visualizar(senial: SenialBase):
    """
    Función genérica que funciona con CUALQUIER señal.

    ✅ LSP: No necesita saber qué tipo específico de señal es.
    """
    print(f"Procesando señal con {senial.obtener_tamanio()} valores...")

    # Visualizar usando polimorfismo
    visualizador = Visualizador()
    visualizador.mostrar_datos(senial)

# ✅ Funciona con todos los tipos
for tipo_senial in [SenialLista, SenialPila, SenialCola]:
    print(f"\n=== {tipo_senial.__name__} ===")
    senial = tipo_senial()
    senial.poner_valor(42.0)
    procesar_y_visualizar(senial)  # ✅ Sin cambios de código
```

## 🏗️ Integración con Sistema Completo

```python
# El Visualizador es usado por el Lanzador
from lanzador import Lanzador
from configurador import Configurador

# El Configurador decide qué tipo de señal usar
senial_adquirida = adquisidor.obtener_senial_adquirida()  # Podría ser cualquier tipo
senial_procesada = procesador.obtener_senial_procesada()  # Podría ser cualquier tipo

# ✅ DIP: El Visualizador no necesita saber cuál es
visualizador = Configurador.crear_visualizador()
visualizador.mostrar_datos(senial_adquirida)   # ✅ Funciona
visualizador.mostrar_datos(senial_procesada)   # ✅ Funciona
```

## 📈 Beneficios del Diseño

### ✅ Extensibilidad sin Cambios
- Agregar `SenialDeque`, `SenialBuffer`, etc. → **Visualizador sin cambios**
- Cambiar tipo de señal en Configurador → **Visualizador sin cambios**
- Nuevos formatos de visualización → **Solo agregar nueva clase**

### ✅ Testing Simplificado
- **Un test funciona para todos los tipos** gracias a polimorfismo
- No necesita tests específicos por implementación
- Cobertura garantizada por contrato `SenialBase`

### ✅ Mantenibilidad
- Cambios en dominio → Propagación automática
- No hay acoplamiento a implementaciones concretas
- Código cliente limpio y simple

## 🎯 Valor Didáctico

### Conceptos Demostrados

1. **LSP Aplicado**: Intercambiabilidad total sin cambios de código
2. **DIP Aplicado**: Dependencia de abstracción `SenialBase`
3. **Polimorfismo Puro**: No usa `isinstance()` para diferenciar
4. **Contrato por Interfaz**: Solo usa métodos de `SenialBase`
5. **Desacoplamiento**: No conoce implementaciones concretas

### Lecciones Aprendidas

- **Las abstracciones bien diseñadas** eliminan la necesidad de código condicional
- **LSP permite testing genérico** que funciona con todas las implementaciones
- **DIP facilita cambios** en las estructuras de datos sin afectar presentación
- **Polimorfismo simplifica** el código cliente dramáticamente

---

**📊 Paquete Presentación - Victor Valotto**
**📖 Proyecto Didáctico**: Demostración de LSP y DIP en acción
**🎯 Polimorfismo**: Funciona con cualquier tipo de señal sin cambios
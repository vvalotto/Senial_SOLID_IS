
# 🏠 Dominio Señal - Entidades del Dominio

**Versión**: 1.0.0
**Autor**: Victor Valotto
**Responsabilidad**: Entidades fundamentales del dominio de señales digitales

Paquete independiente que implementa el **núcleo del dominio** en la arquitectura de procesamiento de señales, siguiendo principios SOLID y Clean Architecture.

## 📋 Descripción

Este paquete representa la **capa más interna** de la arquitectura, conteniendo únicamente las entidades esenciales del dominio de señales digitales. Es completamente independiente de infraestructura, frameworks o librerías externas.

## 🎯 Responsabilidad Única (SRP)

**Una única razón para cambiar**: Modificaciones en las entidades del dominio de señales digitales.

## 📦 Entidades del Dominio

### 🔹 Clase `Senial`

**Responsabilidad**: Representar una señal digital y gestionar su colección de valores.

```python
class Senial:
    """Entidad que representa una señal digital"""

    def poner_valor(self, valor)           # Agregar muestra a la señal
    def obtener_valor(self, indice)        # Obtener muestra por índice
    def obtener_tamanio(self)              # Cantidad de muestras
    def esta_vacia(self)                   # Verificar si está vacía
```

### ✅ Características de la Entidad

- **Encapsulación**: Datos internos protegidos (`_valores`)
- **Validación**: Manejo de índices fuera de rango
- **Inmutable por interfaz**: Solo operaciones seguras expuestas
- **Sin dependencias**: Código puro de Python

## 🚀 Instalación

```bash
# Como paquete independiente
pip install dominio-senial

# O como parte del proyecto completo
pip install -e .
```

## 💻 Uso y Ejemplos

### Ejemplo Básico

```python
from dominio_senial import Senial

# Crear señal vacía
senial = Senial()

# Construir señal con datos
valores = [1.5, 2.8, 3.2, 4.1, 5.7]
for valor in valores:
    senial.poner_valor(valor)

# Consultar información
print(f"📊 Señal con {senial.obtener_tamanio()} muestras")
print(f"🔸 Primera muestra: {senial.obtener_valor(0)}")
print(f"🔸 Última muestra: {senial.obtener_valor(senial.obtener_tamanio()-1)}")
```

### Ejemplo con Validación

```python
# Manejo seguro de índices
senial = Senial()
senial.poner_valor(42.0)

# Acceso válido
valor = senial.obtener_valor(0)  # Retorna 42.0

# Acceso inválido
valor = senial.obtener_valor(5)  # Retorna None (manejo seguro)
```

### Uso en Arquitectura

```python
# La entidad es agnóstica de su uso
def procesar_senial_generica(senial: Senial):
    """Función que funciona con cualquier señal, independiente del origen"""
    if senial.esta_vacia():
        return None

    # Procesamiento genérico
    resultado = Senial()
    for i in range(senial.obtener_tamanio()):
        valor_original = senial.obtener_valor(i)
        valor_procesado = valor_original * 2  # Ejemplo de procesamiento
        resultado.poner_valor(valor_procesado)

    return resultado
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
└─────────────────────────────────────────┘
```

### Principios Aplicados

- **🎯 SRP**: Una responsabilidad - gestionar entidades de señales
- **⭐ Estabilidad**: Centro estable - todos los demás paquetes dependen de este
- **🚫 Independencia**: No depende de ningún otro paquete
- **♻️ Reutilización**: Puede usarse en cualquier contexto de señales digitales

## 🧪 Testing

```bash
# Ejecutar tests del dominio
cd dominio_senial
pytest tests/

# Tests específicos
pytest tests/test_senial.py -v
```

### Ejemplo de Test

```python
def test_senial_basica():
    """Test de la funcionalidad básica de Senial"""
    senial = Senial()

    # Test señal vacía
    assert senial.esta_vacia() is True
    assert senial.obtener_tamanio() == 0

    # Test agregar valores
    senial.poner_valor(1.5)
    senial.poner_valor(2.0)

    assert senial.esta_vacia() is False
    assert senial.obtener_tamanio() == 2
    assert senial.obtener_valor(0) == 1.5
    assert senial.obtener_valor(1) == 2.0
```

## 🔗 Integración con Otros Paquetes

```python
# Ejemplo de como otros paquetes usan el dominio
from dominio_senial import Senial

# Paquete adquisicion_senial
class BaseAdquisidor:
    def __init__(self):
        self._senial = Senial()  # ✅ Usa entidad del dominio

# Paquete procesamiento_senial
class BaseProcesador:
    def __init__(self):
        self._senial_procesada = Senial()  # ✅ Usa entidad del dominio

# Paquete presentacion_senial
class Visualizador:
    def mostrar_datos(self, senial: Senial):  # ✅ Recibe entidad del dominio
        # Lógica de visualización
        pass
```

## 📈 Métricas de Calidad

### Complejidad
- **Clases**: 1 (`Senial`)
- **Métodos públicos**: 4
- **Dependencias**: 0 (solo Python estándar)
- **Líneas de código**: ~60

### Cobertura de Tests
- **Cobertura objetivo**: 100%
- **Casos de prueba**: Funcionalidad básica, casos extremos, validaciones

## 🎓 Valor Didáctico

### Conceptos Demostrados

1. **Entidades de Dominio**: Objetos que representan conceptos del negocio
2. **Encapsulación**: Protección de datos internos con interfaz controlada
3. **Independencia**: Núcleo que no depende de infraestructura
4. **Estabilidad**: Capa que cambia menos frecuentemente
5. **Reutilización**: Código que funciona en múltiples contextos

### Lecciones Aprendidas

- **Las entidades deben ser simples** pero completas para su dominio
- **La independencia facilita el testing** y la reutilización
- **Un buen dominio es la base** para toda la arquitectura
- **La estabilidad del dominio** reduce el impacto de cambios

---

**🏠 Paquete Dominio - Victor Valotto**
**📖 Proyecto Didáctico**: Demostración de Clean Architecture y SOLID
**🎯 Núcleo Estable**: Base para toda la aplicación de señales digitales
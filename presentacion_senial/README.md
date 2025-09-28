# Presentación Señal - Visualización de Datos

Paquete especializado en la presentación y visualización de señales digitales.

## 📋 Descripción

Este paquete implementa la **responsabilidad de presentación** en la arquitectura de procesamiento de señales, siguiendo los principios SOLID y Clean Architecture. Se encarga exclusivamente de mostrar y visualizar datos de señales.

## 🎯 Responsabilidad Única (SRP)

**Una única razón para cambiar**: Modificaciones en la forma de presentar y visualizar datos de señales.

## 📦 Contenido

### Estructura del Paquete

```
presentacion_senial/
├── __init__.py          # Exporta la clase Visualizador
├── visualizador.py      # Módulo con la clase Visualizador
├── setup.py            # Configuración del paquete
└── tests/              # Tests unitarios
```

### Clases Principales

- **`Visualizador`** (en `visualizador.py`): Clase responsable de mostrar señales digitales en consola con formato claro y organizado.

## 🚀 Instalación

```bash
pip install presentacion-senial
```

## 💻 Uso Básico

```python
from presentacion_senial import Visualizador
from dominio_senial import Senial

# Crear una señal de ejemplo
signal = Senial()
signal.poner_valor(1.0)
signal.poner_valor(2.5)
signal.poner_valor(3.8)

# Crear un visualizador
visualizador = Visualizador()

# Mostrar la señal
visualizador.mostrar_senial(signal)

# Generar resumen estadístico
visualizador.generar_resumen(signal)
```

## 🏗️ Arquitectura

Este paquete representa la **capa de presentación** en Clean Architecture:

```
┌─────────────────┐    ┌─────────────────┐
│ presentacion_   │───▶│ dominio_senial  │
│ senial          │    │                 │
└─────────────────┘    └─────────────────┘
```

## 📈 Características

- ✅ **Visualización clara**: Formato organizado y legible en consola
- ✅ **Resúmenes estadísticos**: Información básica de las señales
- ✅ **Separación de responsabilidades**: Solo se encarga de la presentación
- ✅ **Dependencia mínima**: Solo depende del dominio

## 🔗 Dependencias

- `dominio-senial`: Entidades fundamentales del dominio

## 📝 Licencia

MIT License - Ver archivo LICENSE para detalles.

## 👥 Contribución

Este es un proyecto educativo que demuestra la aplicación de principios SOLID.
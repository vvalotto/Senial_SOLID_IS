# Lanzador - Orquestador del Sistema

Paquete orquestador que coordina todo el flujo de procesamiento de señales digitales.

## 📋 Descripción

Este paquete implementa la **responsabilidad de orquestación** en la arquitectura de procesamiento de señales, siguiendo los principios SOLID y Clean Architecture. Se encarga de coordinar el flujo completo del sistema integrando todos los componentes.

## 🎯 Responsabilidad Única (SRP)

**Una única razón para cambiar**: Modificaciones en el flujo de orquestación del sistema completo.

## 📦 Contenido

### Estructura del Paquete

```
lanzador/
├── __init__.py          # Exporta la clase Lanzador y función ejecutar
├── lanzador.py          # Módulo con la clase Lanzador
├── setup.py            # Configuración del paquete
└── tests/              # Tests unitarios
```

### Clases Principales

- **`Lanzador`** (en `lanzador.py`): Clase responsable de orquestar el proceso completo: adquisición → procesamiento → presentación.

## 🚀 Instalación

```bash
pip install lanzador
```

## 💻 Uso Básico

### Como Script

```bash
# Ejecutar con configuración por defecto (5 muestras)
lanzador

# Ejecutar con número específico de muestras
lanzador 10
```

### Como Módulo Python

```python
from lanzador import Lanzador

# Crear y ejecutar el orquestador
lanzador = Lanzador()
lanzador.ejecutar_proceso_completo()

# Configurar número de muestras
lanzador.configurar_muestras(8)
lanzador.ejecutar_proceso_completo()
```

## 🏗️ Arquitectura

Este paquete representa el **orquestador principal** en Clean Architecture:

```
┌─────────────────┐    ┌─────────────────┐
│                 │───▶│ adquisicion_    │
│                 │    │ senial          │
│                 │    └─────────────────┘
│                 │    ┌─────────────────┐
│ lanzador        │───▶│ procesamiento_  │
│                 │    │ senial          │
│                 │    └─────────────────┘
│                 │    ┌─────────────────┐
│                 │───▶│ presentacion_   │
│                 │    │ senial          │
└─────────────────┘    └─────────────────┘
```

## 📈 Características

- ✅ **Orquestación completa**: Coordina todo el flujo del sistema
- ✅ **Manejo de errores**: Gestión robusta de excepciones
- ✅ **Configuración flexible**: Permite ajustar parámetros del procesamiento
- ✅ **Interfaz amigable**: Información clara del progreso y estado

## 🔗 Dependencias

- `dominio-senial`: Entidades fundamentales del dominio
- `adquisicion-senial`: Captura de datos de entrada
- `procesamiento-senial`: Algoritmos de transformación
- `presentacion-senial`: Visualización de resultados

## 📝 Licencia

MIT License - Ver archivo LICENSE para detalles.

## 👥 Contribución

Este es un proyecto educativo que demuestra la aplicación de principios SOLID.
quie# Procesamiento Señal - Algoritmos de Transformación

Paquete especializado en el procesamiento y transformación de señales digitales.

## 📋 Descripción

Este paquete implementa la **responsabilidad de procesamiento** en la arquitectura de procesamiento de señales, siguiendo los principios SOLID y Clean Architecture. Se encarga exclusivamente de aplicar algoritmos y transformaciones sobre las señales.

## 🎯 Responsabilidad Única (SRP)

**Una única razón para cambiar**: Modificaciones en los algoritmos de procesamiento de señales.

## 📦 Contenido

### Estructura del Paquete

```
procesamiento_senial/
├── __init__.py          # Exporta la clase Procesador
├── procesador.py        # Módulo con la clase Procesador
├── setup.py            # Configuración del paquete
└── tests/              # Tests unitarios
```

### Clases Principales

- **`Procesador`** (en `procesador.py`): Clase responsable de aplicar transformaciones y algoritmos sobre señales digitales.

## 🚀 Instalación

```bash
pip install procesamiento-senial
```

## 💻 Uso Básico

```python
from procesamiento_senial import Procesador
from dominio_senial import Senial

# Crear una señal de ejemplo
signal = Senial()
signal.poner_valor(1.0)
signal.poner_valor(2.0)
signal.poner_valor(3.0)

# Crear un procesador
procesador = Procesador()

# Procesar la señal (amplificación 2x)
signal_procesada = procesador.procesar_senial(signal)

print(f"Señal procesada con {signal_procesada.obtener_tamanio()} valores")
```

## 🏗️ Arquitectura

Este paquete representa la **capa de procesamiento** en Clean Architecture:

```
┌─────────────────┐    ┌─────────────────┐
│ procesamiento_  │───▶│ dominio_senial  │
│ senial          │    │                 │
└─────────────────┘    └─────────────────┘
```

## 📈 Características

- ✅ **Algoritmos optimizados**: Implementaciones eficientes de transformaciones
- ✅ **Separación de responsabilidades**: Solo se encarga del procesamiento
- ✅ **Extensible**: Fácil agregar nuevos algoritmos de procesamiento
- ✅ **Dependencia mínima**: Solo depende del dominio

## 🔗 Dependencias

- `dominio-senial`: Entidades fundamentales del dominio

## 📝 Licencia

MIT License - Ver archivo LICENSE para detalles.

## 👥 Contribución

Este es un proyecto educativo que demuestra la aplicación de principios SOLID.
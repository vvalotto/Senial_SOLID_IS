# Adquisición Señal - Captura de Datos

Paquete independiente que contiene las clases responsables de capturar y obtener datos desde diferentes fuentes para formar señales digitales.

## 📋 Descripción

Este paquete implementa la **capa de adquisición** en la arquitectura de procesamiento de señales, siguiendo los principios SOLID. Se encarga exclusivamente de la captura de datos de entrada al sistema.

## 🎯 Responsabilidad Única (SRP)

**Una única razón para cambiar**: Modificaciones en los métodos de adquisición de datos.

## 📦 Contenido

### Estructura del Paquete

```
adquisicion_senial/
├── __init__.py          # Exporta la clase Adquisidor
├── adquisidor.py        # Módulo con la clase Adquisidor
├── setup.py            # Configuración del paquete
└── tests/              # Tests unitarios
```

### Clases Principales

- **`Adquisidor`** (en `adquisidor.py`): Captura datos desde consola para formar señales digitales.

## 🚀 Instalación

```bash
pip install adquisicion-senial
```

## 💻 Uso Básico

```python
from adquisicion_senial import Adquisidor

# Crear adquisidor para 5 muestras
adquisidor = Adquisidor(5)

# Capturar datos desde consola
adquisidor.leer_senial()

# Obtener la señal capturada
senial = adquisidor.obtener_senial_adquirida()
print(f"Señal capturada con {senial.obtener_tamanio()} muestras")
```

## 🔗 Dependencias

- `dominio-senial>=1.0.0`: Entidades del dominio

## 🏗️ Arquitectura

Este paquete representa una **capa de adaptador** en Clean Architecture:

```
┌─────────────────┐
│ dominio_senial  │ ← Entidades (núcleo del negocio)
└─────────────────┘
┌─────────────────┐
│adquisicion_senial│ ← Adaptadores de entrada
└─────────────────┘
```

## 📈 Características

- ✅ **Entrada validada**: Verificación de tipos de datos
- ✅ **Manejo de errores**: Recuperación de entradas incorrectas
- ✅ **Extensible**: Fácil agregar nuevos tipos de adquisidores
- ✅ **Independiente**: Funciona con cualquier fuente de datos

## 🔮 Extensiones Futuras

- `AdquisidorArchivo`: Lectura desde archivos CSV, JSON
- `AdquisidorSensor`: Captura desde hardware IoT
- `AdquisidorRed`: Recepción desde sockets de red

## 📝 Licencia

MIT License - Ver archivo LICENSE para detalles.
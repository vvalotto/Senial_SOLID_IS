# Configurador - Factory Centralizado

## Descripción

El paquete `configurador` implementa un **Factory Centralizado** que aplica el **Principio de Responsabilidad Única (SRP)** para la creación y configuración de objetos en la aplicación de procesamiento de señales.

## Responsabilidad Única

La clase `Configurador` tiene una **única responsabilidad**:
- **Crear y configurar** todas las instancias de clases que la aplicación necesita
- **Centralizar las decisiones** de configuración en un solo lugar
- **Separar la responsabilidad de creación** del código que usa los objetos

## Características

### Configuración Programática
- Los valores de configuración están definidos en el código
- **No requiere archivos externos** (se implementará en versiones futuras con DIP)
- **Valores por defecto** establecidos para cada tipo de objeto

### Factory Methods Disponibles

#### Creación de Componentes Principales
```python
from configurador import Configurador

# Crear adquisidor con configuración por defecto (5 muestras)
adquisidor = Configurador.crear_adquisidor()

# Crear visualizador
visualizador = Configurador.crear_visualizador()

# Crear señal vacía
senial = Configurador.crear_senial_vacia()
```

#### Creación de Procesadores
```python
# Procesadores con configuración por defecto
procesador_amp = Configurador.crear_procesador_amplificador()  # Factor 4.0
procesador_umbral = Configurador.crear_procesador_umbral()     # Umbral 8.0

# Factory dinámico con parámetros por defecto
procesador = Configurador.crear_procesador_por_tipo("amplificar")

# Factory dinámico con parámetros específicos
procesador = Configurador.crear_procesador_por_tipo("umbral", 6.5)
```

## Beneficios

### Separación de Responsabilidades
- **Lanzador**: Se enfoca en la lógica de procesamiento
- **Configurador**: Se encarga exclusivamente de crear objetos
- **Componentes**: Se enfocan en sus responsabilidades específicas

### Mantenibilidad
- **Punto único de cambio** para configuraciones
- **Fácil modificación** de valores por defecto
- **Testing simplificado** con configuraciones controladas

### Preparación para Evolución
- **Base sólida** para implementar DIP en el futuro
- **Estructura preparada** para configuración externa
- **Compatibilidad** con inyección de dependencias

## Configuración Actual

### Valores por Defecto
- **Adquisidor**: 5 muestras por señal
- **Procesador Amplificador**: Factor de amplificación 4.0
- **Procesador Umbral**: Umbral de 8.0

### Procesadores Soportados
- `"amplificar"`: Amplificación de señales
- `"umbral"`: Filtrado por umbral

## Uso en la Aplicación

```python
from configurador import Configurador

def ejemplo_uso():
    # El lanzador ya no se preocupa por la creación
    adquisidor = Configurador.crear_adquisidor()
    procesador = Configurador.crear_procesador_por_tipo("amplificar")
    visualizador = Configurador.crear_visualizador()

    # Solo se enfoca en la lógica de procesamiento
    adquisidor.leer_senial()
    senial = adquisidor.obtener_senial_adquirida()

    procesador.procesar(senial)
    resultado = procesador.obtener_senial_procesada()

    visualizador.mostrar_datos(resultado)
```

## Evolución Futura

### Versión 2.0 (Planificada - DIP)
- Configuración desde archivos externos (JSON/YAML)
- Variables de entorno para configuración
- Inyección de dependencias completa

### Versión 3.0 (Futuro)
- Plugin architecture
- Auto-discovery de componentes
- Configuración en tiempo de ejecución

## Principios SOLID Aplicados

- **SRP**: Una responsabilidad - crear objetos configurados
- **Preparación OCP**: Extensible para nuevos tipos sin modificar existentes
- **Base para DIP**: Centralización que facilita inversión de dependencias futura

## Instalación

Como parte del sistema de paquetes independientes:

```bash
pip install configurador
```

## Dependencias

- `dominio-senial >= 1.0.0`
- `adquisicion-senial >= 1.0.0`
- `procesamiento-senial >= 2.0.0`
- `presentacion-senial >= 1.0.0`
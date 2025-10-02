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

#### Creación de Contextos de Persistencia (Patrón Strategy)
```python
# Contexto de persistencia con Pickle (binario)
contexto_pickle = Configurador.definir_contexto('./datos', tipo='pickle')

# Contexto de persistencia con Archivo (texto plano)
contexto_archivo = Configurador.definir_contexto('./datos', tipo='archivo')
```

#### Creación de Repositorios (Patrón Repository + DIP)
```python
# Crear repositorio inyectando contexto (DIP)
contexto = Configurador.definir_contexto('./datos', 'pickle')
repositorio_senial = Configurador.definir_repositorio(contexto, 'senial')
repositorio_usuario = Configurador.definir_repositorio(contexto, 'usuario')

# Factory de alto nivel - Repositorio de adquisición
repo_adquisicion = Configurador.crear_repositorio_adquisicion()
# Configurado con: ContextoArchivo + './datos_persistidos/adquisicion'

# Factory de alto nivel - Repositorio de procesamiento
repo_procesamiento = Configurador.crear_repositorio_procesamiento()
# Configurado con: ContextoPickle + './datos_persistidos/procesamiento'
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

### Flujo Básico sin Persistencia
```python
from configurador import Configurador

def ejemplo_basico():
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

### Flujo Completo con Patrón Repository (v2.3.0+)
```python
from configurador import Configurador

def ejemplo_con_persistencia():
    # Crear componentes
    adquisidor = Configurador.crear_adquisidor()
    procesador = Configurador.crear_procesador_por_tipo("amplificar")
    visualizador = Configurador.crear_visualizador()

    # Crear repositorios (Patrón Repository + DIP)
    repo_adquisicion = Configurador.crear_repositorio_adquisicion()
    repo_procesamiento = Configurador.crear_repositorio_procesamiento()

    # Adquirir y guardar
    adquisidor.leer_senial()
    senial_original = adquisidor.obtener_senial_adquirida()
    senial_original.id = 1000
    repo_adquisicion.guardar(senial_original)  # API de dominio

    # Procesar y guardar
    procesador.procesar(senial_original)
    senial_procesada = procesador.obtener_senial_procesada()
    senial_procesada.id = 2000
    repo_procesamiento.guardar(senial_procesada)  # API de dominio

    # Recuperar desde repositorios
    senial_recuperada = repo_adquisicion.obtener("1000")
    senial_proc_recuperada = repo_procesamiento.obtener("2000")

    # Visualizar
    visualizador.mostrar_datos(senial_recuperada)
    visualizador.mostrar_datos(senial_proc_recuperada)
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

- **SRP**: Una responsabilidad - crear y configurar objetos
- **OCP**: Extensible para nuevos tipos sin modificar factory methods existentes
- **LSP**: Tipos intercambiables mediante polimorfismo (señales, procesadores, contextos)
- **ISP**: Interfaces específicas por tipo de entidad (señal, usuario)
- **DIP**: Inyección de dependencias en repositorios (contextos abstraídos)

## Patrones de Diseño Implementados

### Factory Method Pattern
Creación centralizada de objetos sin exponer lógica de construcción:
- `crear_adquisidor()`, `crear_procesador()`, `crear_visualizador()`
- `crear_procesador_por_tipo(tipo, parametro)`

### Strategy Pattern
Intercambio dinámico de algoritmos de persistencia:
- `ContextoPickle`: Serialización binaria
- `ContextoArchivo`: Persistencia en texto plano

### Repository Pattern (v2.3.0+)
Separación entre dominio y persistencia:
- **Repositorio**: API de dominio (`guardar()`, `obtener()`)
- **Contexto**: Implementación de infraestructura (`persistir()`, `recuperar()`)
- **DIP**: Contexto inyectado en repositorio vía constructor

## Instalación

Como parte del sistema de paquetes independientes:

```bash
pip install configurador
```

## Dependencias

- `dominio-senial >= 4.0.0`
- `adquisicion-senial >= 2.1.0`
- `procesamiento-senial >= 2.1.0`
- `presentacion-senial >= 2.0.0`
- `persistidor-senial >= 1.0.0` (v2.3.0+)

## Documentación Relacionada

- **Patrón Repository**: `docs/PATRON REPOSITORY EN PERSISTENCIA.md`
- **Solución LSP**: `docs/SOLUCION LSP CON ABSTRACCIONES.md`
- **Implementación OCP**: `docs/IMPLEMENTACION DE OCP CON ABSTRACCIONES.md`
- **SRP en Paquetes**: `docs/IMPLEMETACION DE SRP EN PAQUETES.md`
# Principios SOLID - Caso de Estudio

Este proyecto es un caso de estudio didáctico y académico que demuestra la implementación de los principios SOLID en Python.

## Principios SOLID

- **S** - Single Responsibility Principle (Principio de Responsabilidad Única)
- **O** - Open/Closed Principle (Principio Abierto/Cerrado)
- **L** - Liskov Substitution Principle (Principio de Sustitución de Liskov)
- **I** - Interface Segregation Principle (Principio de Segregación de Interfaces)
- **D** - Dependency Inversion Principle (Principio de Inversión de Dependencias)

## Caso de Estudio

### Requerimiento 1: Sistema de Procesamiento de Señales

El sistema debe implementar un procesador de señales digitales que permita:

1. **Captura de señales**: Simular el ingreso de una señal digital mediante la entrada de valores numéricos por consola, donde cada valor representa una muestra de la señal.

2. **Procesamiento**: Procesar la señal capturada aplicando una amplificación con factor de 2x a cada muestra de la señal original.

3. **Visualización**: Mostrar tanto la señal original como la señal amplificada de manera clara y organizada.

### Requerimiento 2: Extensión con Filtrado por Umbral

**Contexto**: Es necesario agregar un nuevo tipo de procesamiento ya que hay clientes que necesitan valores de la señal por debajo de un umbral específico. Los valores del umbral son entregados mediante archivo de configuración.

**Objetivos**:

1. **Mantener funcionalidad existente**: El sistema debe conservar la capacidad de amplificación (factor 2x) sin modificaciones.

2. **Agregar filtrado por umbral**: Implementar procesamiento que filtre valores por debajo de un umbral configurable.

3. **Lectura de configuración**: Cargar parámetros de umbral desde archivos externos.

4. **Compatibilidad**: Es una nueva versión del sistema que debe mantener retrocompatibilidad.

**Evolución del caso de estudio**:
- **Fase 1**: Implementación que **viola OCP** - modificando código existente
- **Fase 2**: Refactorización que **cumple OCP** - extensión sin modificación


## Metodología Didáctica

### Enfoque Progresivo de Implementación

**Objetivo**: Demostrar la aplicación progresiva de los principios SOLID, mostrando cómo cada principio mejora la estructura, mantenibilidad y extensibilidad del código.

**Estrategia**:

1. **Requerimiento 1 (SRP)**:
   - Implementación inicial con violación de SRP
   - Refactorización aplicando Single Responsibility Principle

2. **Requerimiento 2 (OCP)**:
   - Implementación que viola Open/Closed Principle
   - Refactorización aplicando extensibilidad sin modificación

3. **Evolución continua**: Aplicación de LSP, ISP y DIP según se agreguen nuevos requerimientos

### Beneficios Educativos

- **Contraste antes/después**: Comparación directa entre código que viola y cumple principios SOLID
- **Casos de uso reales**: Escenarios basados en necesidades empresariales comunes
- **Evolución arquitectónica**: Transformación gradual hacia Clean Architecture
- **Métricas de calidad**: Medición objetiva de mejoras en mantenibilidad y extensibilidad

## Instalación

```bash
pip install -r requirements.txt
```

## Ejecución de Tests

```bash
pytest tests/
```
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

**Objetivo didáctico**: Implementar este sistema aplicando progresivamente los principios SOLID, mostrando cómo cada principio mejora la estructura, mantenibilidad y extensibilidad del código.

## Instalación

```bash
pip install -r requirements.txt
```

## Ejecución de Tests

```bash
pytest tests/
```
# Principios SOLID - Caso de Estudio Avanzado

**Versión**: 5.3.0 - Violación ISP Intencional (Didáctica)
**Autor**: Victor Valotto
**Objetivo**: Demostración práctica y didáctica de principios SOLID aplicados a arquitectura de software

Este proyecto es un caso de estudio didáctico que demuestra la **evolución progresiva** de un sistema de procesamiento de señales digitales aplicando principios SOLID, desde violaciones iniciales hasta arquitectura limpia y extensible.

⚠️ **RAMA ACTUAL: NoISP** - Contiene violación INTENCIONAL de ISP para fines didácticos.

## 🎯 Estado Actual del Proyecto

### ✅ Principios SOLID Implementados

- **✅ S** - **Single Responsibility Principle**: Aplicado a nivel de clases Y paquetes
- **✅ O** - **Open/Closed Principle**: Extensibilidad sin modificación (procesamiento + adquisición)
- **✅ L** - **Liskov Substitution Principle**: Intercambiabilidad polimórfica garantizada con SenialBase
- **❌ I** - **Interface Segregation Principle**: VIOLACIÓN INTENCIONAL - BaseRepositorio con interfaz "gorda"
- **✅ D** - **Dependency Inversion Principle**: Dependencia de abstracciones, inyección de dependencias

### 🏗️ Arquitectura Actual

```
📦 Senial_SOLID_IS/
├── 🏠 dominio_senial/          # Entidades del dominio
├── 📡 adquisicion_senial/      # Adquisición (OCP aplicado)
├── ⚙️  procesamiento_senial/    # Procesamiento (OCP aplicado)
├── 📊 presentacion_senial/     # Visualización
├── 🏭 configurador/            # Factory centralizado (SRP)
└── 🚀 lanzador/               # Orquestador (SRP puro)
```

## 📚 Evolución del Caso de Estudio

### 🎯 Requerimiento 1: Sistema Base de Procesamiento

**Objetivo**: Implementar procesador de señales digitales básico
- **Adquisición**: Captura de valores numéricos (consola/archivo)
- **Procesamiento**: Amplificación con factor configurable
- **Visualización**: Mostrar señal original y procesada

### 🔄 Requerimiento 2: Extensión con Nuevos Tipos

**Contexto**: Agregar filtrado por umbral sin romper funcionalidad existente
- **Desafío OCP**: Extensión sin modificación de código existente
- **Solución**: Abstracciones + polimorfismo + Factory Pattern

### 🏭 Requerimiento 3: Factory Centralizado

**Contexto**: Separar responsabilidades de creación y orquestación
- **Desafío SRP**: Lanzador con múltiples responsabilidades
- **Solución**: Configurador centralizado con decisiones "de fábrica"

### 📚 Requerimiento 4: Manejo de Colecciones de Datos (LSP)

**Contexto**: Los valores que corresponden a la señal son manejado como una lista, los desarrolladores están viendo que se puede agregar el manejo de la colección de valores de la señal también como una pila y una cola, además de una lista.
- **Desafío LSP**: Intercambiabilidad real entre diferentes implementaciones de colecciones
- **Solución v4.0.0**: Abstracción `SenialBase` con contrato común, implementaciones `SenialLista`, `SenialPila`, `SenialCola`
- **Resultado**: ✅ LSP aplicado completamente - 100% intercambiabilidad polimórfica

### 💾 Requerimiento 5: Persistencia y Trazabilidad (ISP)

**Contexto**: Los datos adquiridos y procesados deben ser guardados. Se deben registrar los eventos de adquisición y guardado para tener una trazabilidad.
- **Desafío ISP**: Interfaces segregadas por responsabilidad específica
- **Implementación v5.3.0**: ⚠️ VIOLACIÓN INTENCIONAL implementada para fines didácticos
- **Problema Demostrado**: `BaseRepositorio` con 4 métodos abstractos (guardar, obtener, auditar, trazar)
- **Consecuencia**: `RepositorioUsuario` forzado a implementar auditar/trazar aunque no los necesita
- **Próximo Paso**: Resolver violación segregando en `IRepositorioBasico` + `IRepositorioAuditable`


## 🚀 Funcionalidades Implementadas

### 📡 Adquisición de Señales (OCP Aplicado)
- **`AdquisidorConsola`**: Entrada interactiva desde teclado
- **`AdquisidorArchivo`**: Lectura desde archivos de datos
- **Extensible**: Fácil agregar sensores, APIs, bases de datos

### ⚙️ Procesamiento de Señales (OCP Aplicado)
- **`ProcesadorAmplificador`**: Amplificación con factor configurable
- **`ProcesadorConUmbral`**: Filtrado por umbral
- **Extensible**: Fácil agregar FFT, filtros digitales, wavelets

### 🏭 Configuración Centralizada (SRP Aplicado)
- **Decisiones "de fábrica"**: Sin input del usuario
- **Configuración programática**: Valores definidos en código
- **Preparado para DIP**: Base para configuración externa

### 🚀 Orquestación Pura (SRP Aplicado)
- **Responsabilidad única**: Solo coordinar flujo
- **Sin decisiones**: Delegadas al Configurador
- **Sin interacción**: No maneja input del usuario


## ⚠️ Demostración de Violación ISP

### 🎯 Propósito Didáctico

Esta versión implementa INTENCIONALMENTE una violación de ISP para demostrar:

1. **Interfaz "Gorda"**: `BaseRepositorio` con 4 métodos abstractos obligatorios
2. **Cliente Afectado**: `RepositorioUsuario` forzado a implementar métodos innecesarios
3. **Consecuencias**: Implementaciones stub que lanzan `NotImplementedError`

### 📝 Script de Demostración

```bash
# Ejecutar demostración completa de violación ISP
python demo_violacion_isp.py
```

**Salida esperada**:
- ✅ `RepositorioSenial`: Usa los 4 métodos → Sin problemas
- ❌ `RepositorioUsuario`: Métodos auditar/trazar → Crash con `NotImplementedError`

### 🎓 Lección Aprendida

**Violación ISP**: Cuando una interfaz obliga a implementar métodos innecesarios:
- Código frágil (crashes en runtime)
- Implementaciones falsas (stubs)
- Violación de contratos
- Dificultad para mantener

**Solución**: Segregar en interfaces específicas según necesidades reales.

---

## 📖 Uso del Sistema

### 🚀 Ejecución Principal

```bash
# Ejecutar el sistema completo
python -m lanzador.lanzador

# O directamente
cd lanzador
python lanzador.py
```

### 📁 Configuración de Datos

El sistema está configurado para leer datos desde `senial.txt`:
```
# Ejemplo de archivo senial.txt
1.5
2.8
3.2
4.1
5.7
```

### ⚙️ Configuración del Sistema

```python
# El Configurador define la configuración "de fábrica"
from configurador import Configurador

# Configuración actual
adquisidor = Configurador.crear_adquisidor()        # AdquisidorArchivo('senial.txt')
procesador = Configurador.crear_procesador()        # ProcesadorAmplificador(4.0)
visualizador = Configurador.crear_visualizador()    # Visualizador()
```

## 🏗️ Arquitectura y Patrones

### 📦 Paquetes Independientes (SRP a Nivel de Paquetes)

```python
# Cada paquete tiene responsabilidad única y puede instalarse independientemente
pip install dominio-senial           # Solo entidades
pip install adquisicion-senial       # Solo adquisición
pip install procesamiento-senial     # Solo procesamiento
pip install presentacion-senial      # Solo presentación
pip install configurador            # Solo factory centralizado
pip install lanzador               # Solo orquestación
```

### 🔄 Extensibilidad (OCP Demostrado)

```python
# Agregar nuevo procesador SIN modificar código existente
class ProcesadorSuavizado(BaseProcesador):
    def procesar(self, senial):
        # Implementación específica
        pass

# Solo agregar al factory
def crear_procesador_suavizado():
    return ProcesadorSuavizado(ventana=3)
```

### 🔀 Intercambiabilidad (LSP Aplicado) ✅

```python
# ✅ LSP v4.0.0: Cualquier señal funciona polimórficamente
from dominio_senial import SenialBase, SenialLista, SenialPila, SenialCola

def procesar_cualquier_senial(senial: SenialBase):
    """Función genérica que funciona con CUALQUIER tipo de señal"""
    senial.poner_valor(42.0)
    valor = senial.sacar_valor()
    return valor

# ✅ Funciona con las 3 implementaciones
for tipo in [SenialLista, SenialPila, SenialCola]:
    resultado = procesar_cualquier_senial(tipo())
    print(f'{tipo.__name__}: {resultado}')
```

## 📚 Documentación Técnica

### 📋 Documentos Disponibles

- **`docs/IMPLEMENTACION DE OCP CON ABSTRACCIONES.md`**: Guía completa del patrón OCP aplicado
- **`docs/IMPLEMETACION DE SRP EN PAQUETES.md`**: Evolución de SRP a nivel de paquetes
- **`docs/VIOLACIONES DE LSP EN TIPOS DE SEÑAL.md`**: Análisis de violaciones LSP (versión anterior)
- **`docs/SOLUCION LSP CON ABSTRACCIONES.md`**: Solución completa LSP v4.0.0 ⭐ NUEVO
- **Cada paquete**: README.md específico con arquitectura y uso

### 🧪 Testing

```bash
# Tests por paquete
pytest dominio_senial/tests/
pytest procesamiento_senial/tests/
# ... otros paquetes

# Tests de integración
pytest lanzador/tests/
```

## 🎯 Valor Didáctico

### ✅ Lo que se Demuestra

1. **SRP Progresivo**: De clases → paquetes → responsabilidades cristalinas
2. **OCP Práctico**: Extensibilidad real sin tocar código existente
3. **LSP Aplicado**: Abstracción `SenialBase` con intercambiabilidad 100% ⭐ NUEVO
4. **DIP Implementado**: Dependencia de abstracciones, inyección de dependencias ⭐ NUEVO
5. **Factory Centralizado**: Separación total de creación y uso
6. **Polimorfismo Real**: Código cliente funciona con cualquier implementación

### 🔄 Próximo Paso

- **Corrección ISP**: Segregar `BaseRepositorio` en:
  - `IRepositorioBasico` (guardar, obtener) - Para TODOS
  - `IRepositorioAuditable` (auditar, trazar) - Solo para señales

## 🛠️ Instalación y Configuración

```bash
# Clonar repositorio
git clone <repository-url>
cd Senial_SOLID_IS

# Instalar dependencias
pip install -r requirements.txt

# Crear archivo de datos (ejemplo)
echo -e "1.5\n2.8\n3.2\n4.1\n5.7" > senial.txt

# Ejecutar
python -m lanzador.lanzador
```

---

**📖 Proyecto Didáctico - Victor Valotto**
**🎯 Objetivo**: Demostración práctica de principios SOLID aplicados progressivamente
**🔄 Estado v4.0.0**: SRP + OCP + LSP + DIP implementados - Preparado para ISP
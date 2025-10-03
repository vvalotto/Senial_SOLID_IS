# Supervisor - Interfaces Segregadas para Auditoría y Trazabilidad

**Versión**: 1.0.0
**Autor**: Victor Valotto
**Objetivo**: Demostración de ISP (Interface Segregation Principle) correctamente aplicado

## 📋 Descripción

Paquete que proporciona **interfaces segregadas** para auditoría y trazabilidad, demostrando la aplicación correcta del **Interface Segregation Principle (ISP)**.

Este paquete es la **solución** a la violación ISP presente en `BaseRepositorio`, donde se obligaba a todos los repositorios a implementar métodos de auditoría y trazabilidad innecesarios.

## 🎯 Problema que Resuelve

### ❌ Antes: Violación ISP en BaseRepositorio

```python
class BaseRepositorio(ABC):
    @abstractmethod
    def guardar(self, entidad): pass        # ✅ Todos lo necesitan

    @abstractmethod
    def obtener(self, id_entidad): pass     # ✅ Todos lo necesitan

    @abstractmethod
    def auditar(self, entidad, auditoria): pass    # ⚠️ Solo señales

    @abstractmethod
    def trazar(self, entidad, accion, mensaje): pass  # ⚠️ Solo señales

# Consecuencia: RepositorioUsuario forzado a implementar métodos innecesarios
class RepositorioUsuario(BaseRepositorio):
    def auditar(self, entidad, auditoria):
        raise NotImplementedError("No soportado")  # ❌ Stub innecesario
```

### ✅ Después: ISP Correctamente Aplicado

```python
# Interfaces segregadas en paquete supervisor
from supervisor import BaseAuditor, BaseTrazador

# Interfaz básica - TODOS la necesitan
class IRepositorioBasico(ABC):
    def guardar(self, entidad): pass
    def obtener(self, id_entidad): pass

# Composición según necesidades
class RepositorioSenial(IRepositorioBasico):
    def __init__(self, contexto, auditor: BaseAuditor, trazador: BaseTrazador):
        self._contexto = contexto
        self._auditor = auditor      # ✅ Composición
        self._trazador = trazador    # ✅ Composición

class RepositorioUsuario(IRepositorioBasico):
    """Solo persistencia - NO auditoría ni trazabilidad"""
    # ✅ Sin métodos innecesarios
```

## 🏗️ Componentes

### `BaseAuditor` - Interfaz de Auditoría

Interfaz segregada que define **solo** la responsabilidad de auditoría.

```python
from abc import ABCMeta, abstractmethod
from typing import Any

class BaseAuditor(metaclass=ABCMeta):
    """
    Abstracción para auditores.

    Aplicación de ISP: interfaz específica SOLO para auditoría.
    """

    @abstractmethod
    def auditar(self, entidad: Any, auditoria: str) -> None:
        """
        Registra un evento de auditoría sobre una entidad.

        :param entidad: Entidad sobre la cual se registra la auditoría
        :param auditoria: Descripción del evento de auditoría
        """
        pass
```

### `BaseTrazador` - Interfaz de Trazabilidad

Interfaz segregada que define **solo** la responsabilidad de trazabilidad.

```python
from abc import ABCMeta, abstractmethod
from typing import Any

class BaseTrazador(metaclass=ABCMeta):
    """
    Abstracción para trazadores.

    Aplicación de ISP: interfaz específica SOLO para trazabilidad.
    """

    @abstractmethod
    def trazar(self, entidad: Any, accion: str, mensaje: str) -> None:
        """
        Registra una traza de acción sobre una entidad.

        :param entidad: Entidad sobre la cual se registra la traza
        :param accion: Tipo de acción realizada
        :param mensaje: Mensaje descriptivo de la traza
        """
        pass
```

## 🚀 Instalación

```bash
pip install -e supervisor/
```

## 💻 Uso

### Importar Abstracciones

```python
from supervisor import BaseAuditor, BaseTrazador
```

### Implementar Auditores Concretos

```python
import datetime

class AuditorArchivo(BaseAuditor):
    """Auditor que escribe en archivo"""

    def __init__(self, ruta_archivo='auditor.log'):
        self._ruta_archivo = ruta_archivo

    def auditar(self, entidad, auditoria):
        with open(self._ruta_archivo, 'a') as f:
            f.write(f'------->\n')
            f.write(f'Entidad ID: {entidad.id}\n')
            f.write(f'Fecha: {datetime.datetime.now()}\n')
            f.write(f'Auditoría: {auditoria}\n\n')
```

### Implementar Trazadores Concretos

```python
import datetime

class TrazadorArchivo(BaseTrazador):
    """Trazador que escribe en archivo"""

    def __init__(self, ruta_archivo='logger.log'):
        self._ruta_archivo = ruta_archivo

    def trazar(self, entidad, accion, mensaje):
        with open(self._ruta_archivo, 'a') as f:
            f.write(f'------->\n')
            f.write(f'Acción: {accion}\n')
            f.write(f'Entidad ID: {entidad.id}\n')
            f.write(f'Fecha: {datetime.datetime.now()}\n')
            f.write(f'Mensaje: {mensaje}\n\n')
```

### Usar en Repositorios (Composición)

```python
from supervisor import BaseAuditor, BaseTrazador

class RepositorioSenial:
    """Repositorio con auditoría y trazabilidad"""

    def __init__(self, contexto, auditor: BaseAuditor, trazador: BaseTrazador):
        self._contexto = contexto
        self._auditor = auditor
        self._trazador = trazador

    def guardar(self, senial):
        # Guardar señal
        self._contexto.persistir(senial, str(senial.id))

        # Auditar operación
        self._auditor.auditar(senial, "Señal guardada correctamente")

        # Trazar operación
        self._trazador.trazar(senial, "PERSISTENCIA", "Guardado completado")

    def obtener(self, id_senial):
        return self._contexto.recuperar(id_senial)

class RepositorioUsuario:
    """Repositorio simple - SIN auditoría ni trazabilidad"""

    def __init__(self, contexto):
        self._contexto = contexto  # ✅ Solo lo necesario

    def guardar(self, usuario):
        self._contexto.persistir(usuario, str(usuario.id))

    def obtener(self, id_usuario):
        return self._contexto.recuperar(id_usuario)

    # ✅ NO hay métodos auditar() ni trazar() innecesarios
```

## 📊 Comparación: Antes vs Después

| Aspecto | Violación ISP | ISP Correcto |
|---------|--------------|--------------|
| **BaseRepositorio** | 4 métodos obligatorios | Interfaces segregadas |
| **RepositorioUsuario** | Stubs con `NotImplementedError` | Solo métodos necesarios |
| **RepositorioSenial** | Métodos en la clase | Composición con auditor/trazador |
| **Reutilización** | Auditoría acoplada | Auditor/Trazador reutilizable |
| **Flexibilidad** | Cambiar = modificar clase | Cambiar = inyectar implementación |
| **Testabilidad** | Difícil mockear | Fácil inyectar mocks |

## ✅ Principios SOLID Demostrados

### 1. ISP (Interface Segregation Principle) ⭐
**"Los clientes no deberían verse obligados a depender de interfaces que no utilizan"**

- ✅ `BaseAuditor` y `BaseTrazador` son interfaces **segregadas**
- ✅ Cada interfaz tiene **una responsabilidad específica**
- ✅ `RepositorioUsuario` no depende de auditoría/trazabilidad
- ✅ `RepositorioSenial` solo depende de lo que usa

### 2. SRP (Single Responsibility Principle)
- `BaseAuditor`: Una responsabilidad - Auditoría
- `BaseTrazador`: Una responsabilidad - Trazabilidad

### 3. DIP (Dependency Inversion Principle)
- Repositorios dependen de **abstracciones** (`BaseAuditor`, `BaseTrazador`)
- Implementaciones concretas se **inyectan** vía constructor

### 4. OCP (Open/Closed Principle)
- Fácil agregar nuevas implementaciones sin modificar interfaces
- Extensible: `AuditorConsola`, `TrazadorBD`, `AuditorCloud`, etc.

### 5. LSP (Liskov Substitution Principle)
- Cualquier implementación de `BaseAuditor` es intercambiable
- Cualquier implementación de `BaseTrazador` es intercambiable

## 🎓 Valor Didáctico

### Lección 1: Segregación de Interfaces
**Antes**: Una interfaz "gorda" con métodos que no todos necesitan
**Después**: Interfaces pequeñas y específicas

### Lección 2: Composición sobre Herencia
**Antes**: Herencia forzada de métodos innecesarios
**Después**: Composición flexible según necesidades

### Lección 3: Dependencias Opcionales
**Antes**: Todos dependen de todo
**Después**: Cada cliente depende solo de lo que usa

## 🔗 Integración con el Proyecto

### Estructura del Proyecto

```
Senial_SOLID_IS/
├── supervisor/              # ✅ Interfaces segregadas (ISP)
│   ├── __init__.py
│   ├── auditor.py          # BaseAuditor
│   ├── trazador.py         # BaseTrazador
│   ├── setup.py
│   └── README.md           # Este archivo
│
├── persistidor_senial/      # Repositorios que USAN supervisor
│   ├── repositorio.py      # IRepositorioBasico + composición
│   └── ...
│
└── ...
```

### Flujo de Corrección ISP

1. **Crear paquete `supervisor`** con interfaces segregadas ✅
2. **Refactorizar `repositorio.py`**:
   - Crear `IRepositorioBasico` (guardar, obtener)
   - Crear `IRepositorioAuditable` (opcional)
3. **Modificar `RepositorioSenial`**:
   - Recibir `auditor` y `trazador` por composición
4. **Simplificar `RepositorioUsuario`**:
   - Solo implementar `IRepositorioBasico`
   - Eliminar stubs de auditar/trazar

## 📚 Referencias

### Documentación del Proyecto
- **Violación ISP**: `../docs/PATRON REPOSITORY EN PERSISTENCIA.md`
- **README Principal**: `../README.md`
- **Demo Violación**: `../demo_violacion_isp.py`

### Patrón ISP
> **Martin, Robert C.** - "Agile Software Development: Principles, Patterns, and Practices"
>
> *"The Interface Segregation Principle states that clients should not be forced to depend upon interfaces that they do not use."*

## 🔄 Próximos Pasos

### Implementaciones Concretas Sugeridas

```python
# En persistidor_senial o módulo separado
from supervisor import BaseAuditor, BaseTrazador

class AuditorArchivo(BaseAuditor):
    """Implementación que escribe en archivo"""
    # ... implementación ...

class TrazadorArchivo(BaseTrazador):
    """Implementación que escribe en archivo"""
    # ... implementación ...

class AuditorNulo(BaseAuditor):
    """Null Object Pattern - Sin efecto"""
    def auditar(self, entidad, auditoria):
        pass  # No hace nada
```

### Configurador Actualizado

```python
from supervisor import BaseAuditor, BaseTrazador

class Configurador:
    @staticmethod
    def crear_auditor() -> BaseAuditor:
        return AuditorArchivo('./logs/auditor.log')

    @staticmethod
    def crear_trazador() -> BaseTrazador:
        return TrazadorArchivo('./logs/logger.log')

    @staticmethod
    def crear_repositorio_senial():
        contexto = ContextoArchivo('./datos/adquisicion')
        auditor = Configurador.crear_auditor()
        trazador = Configurador.crear_trazador()
        return RepositorioSenial(contexto, auditor, trazador)
```

## 💡 Conclusión

El paquete `supervisor` demuestra cómo **segregar interfaces** de forma correcta:

✅ **Interfaces pequeñas y cohesivas**
✅ **Clientes dependen solo de lo necesario**
✅ **Composición flexible en lugar de herencia rígida**
✅ **Código más testeable y mantenible**

Esta es la **corrección completa** de la violación ISP identificada en el proyecto, aplicando el principio de forma práctica y didáctica.

---

**📖 Paquete Didáctico - Victor Valotto**
**🎯 Objetivo**: Demostración de ISP correctamente aplicado
**🔄 Estado v1.0.0**: Interfaces segregadas - Base para corrección ISP en repositorios

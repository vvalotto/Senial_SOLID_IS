# Persistidor de Señales - Repository Pattern

**Versión**: 6.0.0
**Autor**: Victor Valotto
**Objetivo**: Demostración del Repository Pattern + ISP Correctamente Aplicado

## 📋 Descripción

Este paquete implementa el **Patrón Repository** para la persistencia de señales digitales, separando claramente la **lógica de dominio** (Repositorio) de la **infraestructura de persistencia** (Contexto).

## 🏗️ Arquitectura - Repository Pattern con ISP

```
┌──────────────────────────────────────────────────────────────────┐
│                    PAQUETE SUPERVISOR                            │
│  ┌────────────────────┐          ┌────────────────────┐          │
│  │   BaseAuditor      │          │   BaseTrazador     │          │
│  │  - auditar()       │          │  - trazar()        │          │
│  └────────────────────┘          └────────────────────┘          │
└──────────────────────────────────────────────────────────────────┘
                            │  Herencia múltiple
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                      CAPA DE DOMINIO                        │
│  ┌────────────────────────────────────────────────────┐     │
│  │  BaseRepositorio ✅ INTERFAZ BÁSICA (ISP)          │     │
│  │  - guardar(entidad) ✅                             │     │
│  │  - obtener(id_entidad) ✅                          │     │
│  └────────────────────────────────────────────────────┘     │
│                           ▲                                 │
│              ┌────────────┴────────────┐                    │
│              │                         │                    │
│  ┌───────────┴──────────────────┐  ┌──────────┴────────────┐
│  │  RepositorioSenial           │  │  RepositorioUsuario   │
│  │  (BaseAuditor +              │  │  (BaseRepositorio)    │
│  │   BaseTrazador +             │  │                       │
│  │   BaseRepositorio)           │  │  ✅ Solo 2 métodos    │
│  │  ✅ Implementa 4 métodos     │  │  ✅ Sin stubs         │
│  │  ✅ Auditoría REAL           │  │  ✅ ISP respetado     │
│  └──────────────────────────────┘  └───────────────────────┘
└─────────────────────────────────────────────────────────────┘
                            │
                            │ Inyección (DIP)
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                  CAPA DE INFRAESTRUCTURA                    │
│  ┌────────────────────────────────────────────────────┐     │
│  │  BaseContexto (Abstracción - Strategy)             │     │
│  │  - persistir(entidad, id)                          │     │
│  │  - recuperar(id, entidad) → entidad                │     │
│  └────────────────────────────────────────────────────┘     │
│                           ▲                                 │
│              ┌────────────┴────────────┐                    │
│              │                         │                    │
│  ┌───────────┴──────────┐  ┌──────────┴────────────┐       │
│  │  ContextoPickle      │  │  ContextoArchivo       │       │
│  │  (Binario .pickle)   │  │  (Texto .dat)          │       │
│  └──────────────────────┘  └───────────────────────┘       │
└─────────────────────────────────────────────────────────────┘
```

## ✅ Principios SOLID Aplicados

### 1. SRP (Single Responsibility Principle)
- **Repositorio**: Responsable de la lógica de dominio de persistencia
- **Contexto**: Responsable de la implementación técnica del almacenamiento
- **Mapeador**: Responsable de serialización/deserialización

### 2. OCP (Open/Closed Principle)
- Extensible para nuevos contextos (SQL, NoSQL, Cloud) sin modificar repositorios
- Nuevos tipos de entidades (Usuario, Config) sin modificar contextos existentes

### 3. LSP (Liskov Substitution Principle)
- Cualquier `BaseContexto` puede usarse en un `Repositorio`
- Contextos intercambiables sin afectar la lógica de dominio

### 4. ISP (Interface Segregation Principle)
✅ **CORRECTAMENTE APLICADO (v6.0.0)**:

**Solución**: Interfaces segregadas según necesidades reales:
- `BaseRepositorio`: Solo métodos básicos (guardar, obtener) ✅
- `BaseAuditor` (paquete supervisor): Auditoría segregada ✅
- `BaseTrazador` (paquete supervisor): Trazabilidad segregada ✅

**Implementación por herencia múltiple**:
```python
from supervisor import BaseAuditor, BaseTrazador

# RepositorioSenial: Necesita auditoría y trazabilidad
class RepositorioSenial(BaseAuditor, BaseTrazador, BaseRepositorio):
    def guardar(self, senial):
        # Implementación REAL con auditoría automática
        self.auditar(senial, "Antes de hacer la persistencia")
        self._contexto.persistir(senial, str(senial.id))
        self.auditar(senial, "Se realizó la persistencia")

    def auditar(self, entidad, auditoria):
        # Implementación REAL - Escribe en archivo
        with open('auditor_senial.log', 'a') as f:
            f.write(f'{entidad}\n{auditoria}\n')

    def trazar(self, entidad, accion, mensaje):
        # Implementación REAL - Escribe en archivo
        with open('logger_senial.log', 'a') as f:
            f.write(f'Acción: {accion}\n{mensaje}\n')

# RepositorioUsuario: Solo necesita persistencia básica
class RepositorioUsuario(BaseRepositorio):
    def guardar(self, usuario):
        # Sin auditoría - Solo persistencia
        self._contexto.persistir(usuario, str(usuario.id))

    # ✅ NO tiene auditar() ni trazar() - ISP respetado
```

**Resultado**:
- ✅ Cada repositorio solo implementa lo que necesita
- ✅ No hay métodos stub con NotImplementedError
- ✅ Código robusto y mantenible
- ✅ Auditoría y trazabilidad automáticas en guardar()/obtener()

### 5. DIP (Dependency Inversion Principle)
✅ **APLICADO CORRECTAMENTE**:
- Repositorio depende de abstracción `BaseContexto`, no de implementaciones concretas
- Contexto inyectado vía constructor: `RepositorioSenial(contexto)`

## 🏗️ Componentes

### Repositorios (Capa de Dominio)

#### `BaseRepositorio`
✅ **Interfaz Básica - ISP Correctamente Aplicado**

Abstracción que define la interfaz básica de dominio para persistencia, conteniendo solo los métodos que TODOS los repositorios necesitan.

```python
class BaseRepositorio(ABC):
    def __init__(self, contexto: Any):
        self._contexto = contexto

    @abstractmethod
    def guardar(self, entidad: Any) -> None:
        """Persiste la entidad"""
        pass

    @abstractmethod
    def obtener(self, id_entidad: str, entidad: Any = None) -> Any:
        """Obtiene una entidad por su identificador"""
        pass

# Interfaces segregadas en paquete supervisor:
# - BaseAuditor.auditar() ✅ Solo para repositorios que lo necesitan
# - BaseTrazador.trazar() ✅ Solo para repositorios que lo necesitan
```

#### `RepositorioSenial`
✅ **Repositorio con Auditoría y Trazabilidad** - Herencia Múltiple

Repositorio específico para gestionar señales con auditoría completa mediante herencia múltiple.

```python
from persistidor_senial import RepositorioSenial, ContextoPickle

# Crear contexto de persistencia (infraestructura)
contexto = ContextoPickle("./datos")

# Crear repositorio con contexto inyectado (DIP)
repo = RepositorioSenial(contexto)

# API de dominio - Auditoría automática
senial.id = 1000
repo.guardar(senial)  # ✅ Guardar + Auditoría automática interna
senial_recuperada = repo.obtener("1000")  # ✅ Recuperar + Auditoría automática

# La auditoría y trazabilidad ocurren AUTOMÁTICAMENTE dentro de guardar()/obtener()
# No es necesario llamar repo.auditar() o repo.trazar() explícitamente
```

**Características**:
- Herencia múltiple: `BaseAuditor + BaseTrazador + BaseRepositorio`
- Auditoría automática en cada operación guardar()/obtener()
- Trazabilidad solo en caso de excepciones
- Logs escritos en `auditor_senial.log` y `logger_senial.log`

#### `RepositorioUsuario`
✅ **Repositorio Simple** - ISP Correctamente Aplicado

Repositorio específico para gestionar usuarios (solo persistencia, sin auditoría).

```python
from persistidor_senial import RepositorioUsuario, ContextoArchivo

contexto = ContextoArchivo("./usuarios")
repo = RepositorioUsuario(contexto)

usuario.id = 500
repo.guardar(usuario)  # ✅ Funciona
usuario_recuperado = repo.obtener("500")  # ✅ Funciona

# ✅ NO tiene métodos auditar() ni trazar() - ISP respetado
# hasattr(repo, 'auditar')  # False
# hasattr(repo, 'trazar')   # False
```

**Características**:
- Solo hereda de `BaseRepositorio` (sin BaseAuditor ni BaseTrazador)
- Implementa únicamente los 2 métodos que necesita
- Sin métodos stub o NotImplementedError
- Código limpio y honesto con su contrato

### Contextos (Capa de Infraestructura - Strategy Pattern)

#### `BaseContexto`
Abstracción que define la interfaz de persistencia técnica.

```python
class BaseContexto(ABC):
    def __init__(self, recurso: str):
        self._recurso = recurso

    @abstractmethod
    def persistir(self, entidad: Any, id_entidad: str) -> None:
        """Implementa la estrategia de persistencia"""
        pass

    @abstractmethod
    def recuperar(self, id_entidad: str, entidad: Any = None) -> Any:
        """Implementa la estrategia de recuperación"""
        pass
```

#### `ContextoPickle`
Estrategia de persistencia binaria con serialización pickle.

```python
from persistidor_senial import ContextoPickle

contexto = ContextoPickle("./datos_pickle")
contexto.persistir(senial, "senial_001")
senial_recuperada = contexto.recuperar("senial_001")
```

**Características:**
- ✅ Serialización rápida y eficiente
- ✅ Preserva estructura completa del objeto
- ✅ Formato binario (.pickle)
- ✅ Reconstrucción automática (no requiere template)
- ⚠️ No human-readable

#### `ContextoArchivo`
Estrategia de persistencia en texto plano con metadatos.

```python
from persistidor_senial import ContextoArchivo

contexto = ContextoArchivo("./datos_texto")
contexto.persistir(senial, "senial_001")
senial_recuperada = contexto.recuperar("senial_001")  # Reconstrucción automática
```

**Características:**
- ✅ Formato de texto plano (.dat + .meta)
- ✅ Human-readable (debugging fácil)
- ✅ Reconstrucción automática usando metadatos
- ✅ Soporta listas y colecciones
- ⚠️ Requiere metadatos válidos

### Mapeadores

#### `MapeadorArchivo`
Convierte objetos Python a formato de texto plano y viceversa.

**Responsabilidad**: Serialización/deserialización para `ContextoArchivo`

## 📖 Uso

### Instalación

```bash
pip install -e persistidor_senial/
```

### Ejemplo Básico - Uso Directo de Contextos

```python
from persistidor_senial import ContextoPickle, ContextoArchivo
from dominio_senial import SenialLista

# ==================== USANDO CONTEXTO PICKLE ====================
contexto_pickle = ContextoPickle("./datos_pickle")

senial = SenialLista()
senial.poner_valor(1.5)
senial.poner_valor(2.8)
contexto_pickle.persistir(senial, "senial_001")

senial_recuperada = contexto_pickle.recuperar("senial_001")

# ==================== USANDO CONTEXTO ARCHIVO ====================
contexto_archivo = ContextoArchivo("./datos_texto")

senial = SenialLista()
senial.poner_valor(4.1)
senial.poner_valor(5.7)
contexto_archivo.persistir(senial, "senial_002")

# Reconstrucción automática usando metadatos
senial_recuperada = contexto_archivo.recuperar("senial_002")
```

### Ejemplo Avanzado - Repository Pattern (Recomendado)

```python
from persistidor_senial import RepositorioSenial, ContextoPickle, ContextoArchivo
from dominio_senial import SenialLista

# Crear contextos (infraestructura)
contexto_pickle = ContextoPickle("./datos_pickle")
contexto_archivo = ContextoArchivo("./datos_texto")

# Crear repositorios con inyección de dependencias (DIP)
repo_pickle = RepositorioSenial(contexto_pickle)
repo_archivo = RepositorioSenial(contexto_archivo)

# Usar API de dominio (guardar/obtener)
senial = SenialLista()
senial.poner_valor(10.5)
senial.poner_valor(20.3)
senial.id = 1000

# Guardar con repositorio
repo_pickle.guardar(senial)  # API de dominio

# Recuperar con repositorio
senial_recuperada = repo_pickle.obtener("1000")  # API de dominio

# Cambiar estrategia de persistencia (OCP aplicado)
repo_archivo.guardar(senial)  # Mismo código, diferente implementación
senial_recuperada2 = repo_archivo.obtener("1000")
```

### Uso con Configurador (Factory Pattern)

```python
from configurador import Configurador

# Factory de alto nivel - No necesitas crear contextos manualmente
repo_adquisicion = Configurador.crear_repositorio_adquisicion()
# Internamente: ContextoArchivo("./datos_persistidos/adquisicion")

repo_procesamiento = Configurador.crear_repositorio_procesamiento()
# Internamente: ContextoPickle("./datos_persistidos/procesamiento")

# Usar API de dominio
senial.id = 1000
repo_adquisicion.guardar(senial)
senial_recuperada = repo_adquisicion.obtener("1000")
```

### Compatibilidad con API Legacy

El paquete mantiene compatibilidad con la API anterior mediante aliases:

```python
# API legacy (deprecada, usar solo para compatibilidad)
from persistidor_senial import PersistidorPickle, PersistidorArchivo

persistidor = PersistidorPickle("./datos")  # Alias de ContextoPickle
persistidor.persistir(senial, "test")
```

⚠️ **Nota**: Los aliases `PersistidorPickle` y `PersistidorArchivo` están deprecados. Usar `ContextoPickle` y `ContextoArchivo` en código nuevo.

### Manejo de Errores

```python
from persistidor_senial import RepositorioSenial, ContextoPickle

contexto = ContextoPickle("./datos")
repo = RepositorioSenial(contexto)

try:
    # Validación automática de parámetros
    repo.guardar(None)  # Lanza ValueError
except ValueError as e:
    print(f"Error: {e}")

# Recuperación de archivo no existente retorna None
resultado = repo.obtener("no_existe")  # None
if resultado is None:
    print("Entidad no encontrada")
```

### Logging

El módulo utiliza el sistema estándar de `logging` de Python:

```python
import logging

# Configurar logging para ver operaciones
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Ahora verás logs de las operaciones
repo.guardar(senial)
# INFO - Directorio creado: ./datos
# INFO - Entidad persistida exitosamente: 1000
```

## 🎯 Dependencias

- **dominio-senial** >= 4.0.0 - Entidades `SenialBase` y sus implementaciones
- **supervisor** >= 1.0.0 - Interfaces segregadas (BaseAuditor, BaseTrazador)
- **Python** >= 3.8

## 📚 Casos de Uso

### 1. Persistencia de señales adquiridas (Texto plano)

```python
from configurador import Configurador

adquisidor = Configurador.crear_adquisidor()
repo_adquisicion = Configurador.crear_repositorio_adquisicion()

adquisidor.leer_senial()
senial_original = adquisidor.obtener_senial_adquirida()
senial_original.id = 1000

# Persistir en formato texto (.dat)
repo_adquisicion.guardar(senial_original)
```

### 2. Persistencia de señales procesadas (Pickle binario)

```python
from configurador import Configurador

procesador = Configurador.crear_procesador_por_tipo("amplificar")
repo_procesamiento = Configurador.crear_repositorio_procesamiento()

procesador.procesar(senial_original)
senial_procesada = procesador.obtener_senial_procesada()
senial_procesada.id = 2000

# Persistir en formato binario (.pickle)
repo_procesamiento.guardar(senial_procesada)
```

### 3. Recuperación y comparación de señales

```python
# Recuperar señales históricas
senial_historica = repo_procesamiento.obtener("2000")

if senial_historica:
    print(f"Tamaño histórico: {senial_historica.obtener_tamanio()}")
    print(f"Tamaño actual: {senial_procesada.obtener_tamanio()}")
```

### 4. Intercambio de estrategias (Strategy Pattern)

```python
from persistidor_senial import RepositorioSenial, ContextoPickle, ContextoArchivo

# Mismo repositorio, diferentes estrategias
senial.id = 3000

repo_binario = RepositorioSenial(ContextoPickle("./backup_pickle"))
repo_binario.guardar(senial)

repo_texto = RepositorioSenial(ContextoArchivo("./backup_texto"))
repo_texto.guardar(senial)

# Recuperar desde cualquier estrategia
senial_desde_pickle = repo_binario.obtener("3000")
senial_desde_texto = repo_texto.obtener("3000")
```

## ✅ ISP Correctamente Aplicado

### Solución Implementada: Interfaces Segregadas

**Principio ISP**: "Los clientes no deberían verse obligados a depender de interfaces que no utilizan"

### Arquitectura de Interfaces Segregadas

| Método | RepositorioSenial | RepositorioUsuario | Interfaz |
|--------|-------------------|---------------------|----------|
| `guardar()` | ✅ Necesita | ✅ Necesita | `BaseRepositorio` |
| `obtener()` | ✅ Necesita | ✅ Necesita | `BaseRepositorio` |
| `auditar()` | ✅ Necesita | ❌ NO necesita | `BaseAuditor` (supervisor) |
| `trazar()` | ✅ Necesita | ❌ NO necesita | `BaseTrazador` (supervisor) |

### Implementación con Herencia Múltiple

**RepositorioSenial** implementa las 3 interfaces (porque las necesita):

```python
from supervisor import BaseAuditor, BaseTrazador

class RepositorioSenial(BaseAuditor, BaseTrazador, BaseRepositorio):
    def guardar(self, senial):
        # ✅ Implementación REAL con auditoría
        self.auditar(senial, "Antes de hacer la persistencia")
        self._contexto.persistir(senial, str(senial.id))
        self.auditar(senial, "Se realizó la persistencia")

    def obtener(self, id_senial, entidad=None):
        # ✅ Implementación REAL con auditoría
        self.auditar(entidad if entidad else {'id': id_senial}, "Antes de recuperar la señal")
        resultado = self._contexto.recuperar(id_senial, entidad)
        self.auditar(resultado, "Se realizó la recuperación")
        return resultado

    def auditar(self, entidad, auditoria):
        # ✅ Implementación REAL - Escribe en archivo
        with open('auditor_senial.log', 'a') as f:
            f.write(f'------->\n{entidad}\n{datetime.now()}\n{auditoria}\n\n')

    def trazar(self, entidad, accion, mensaje):
        # ✅ Implementación REAL - Escribe en archivo
        with open('logger_senial.log', 'a') as f:
            f.write(f'------->\nAcción: {accion}\n{entidad}\n{datetime.now()}\n{mensaje}\n\n')
```

**RepositorioUsuario** solo implementa la interfaz básica:

```python
class RepositorioUsuario(BaseRepositorio):
    def guardar(self, usuario):
        # ✅ Implementación REAL - Solo persistencia
        self._contexto.persistir(usuario, str(usuario.id))

    def obtener(self, id_usuario, entidad=None):
        # ✅ Implementación REAL - Solo persistencia
        return self._contexto.recuperar(id_usuario, entidad)

    # ✅ NO tiene auditar() ni trazar() - ISP respetado
```

### Beneficios de la Corrección ISP

**✅ Clientes solo implementan lo que necesitan**:
- `RepositorioUsuario` no tiene métodos innecesarios
- No hay stubs con `NotImplementedError`
- Código honesto con su contrato

**✅ Separación de responsabilidades (SRP)**:
- `BaseRepositorio`: Persistencia básica
- `BaseAuditor`: Auditoría especializada
- `BaseTrazador`: Trazabilidad especializada

**✅ Flexibilidad y extensibilidad**:
- Fácil crear repositorios con diferentes combinaciones
- Ejemplo: `RepositorioConfig` solo con `BaseRepositorio`
- Ejemplo: `RepositorioTransaccion` con `BaseRepositorio + BaseAuditor`

**✅ Testabilidad mejorada**:
- Se pueden hacer mocks de interfaces individuales
- Tests más enfocados y específicos

**✅ Mantenibilidad**:
- Cambios en auditoría no afectan repositorios simples
- Cada interfaz evoluciona independientemente

### Demostración Interactiva

Ejecutar script de prueba de corrección ISP:

```bash
python test_correccion_isp.py
```

Este script verifica:
1. ✅ `RepositorioSenial` funciona con auditoría y trazabilidad automáticas
2. ✅ `RepositorioUsuario` funciona SIN métodos innecesarios
3. ✅ Verificación que `RepositorioUsuario` no tiene `auditar()` ni `trazar()`
4. 📝 Logs generados automáticamente en `auditor_senial.log`

## 🔄 Mejoras Futuras

- [x] ✅ Aplicar ISP: Interfaces segregadas (v6.0.0)
- [x] ✅ Sistema de auditoría y trazabilidad segregado (paquete supervisor)
- [ ] Agregar soporte para transacciones
- [ ] Implementar caché de entidades
- [ ] Agregar tests unitarios y de integración completos
- [ ] Soporte para contextos adicionales (SQL, MongoDB, Cloud Storage)
- [ ] Implementaciones concretas adicionales de BaseAuditor (consola, base de datos, cloud)

## 📖 Documentación Relacionada

- **Patrón Repository**: `docs/PATRON REPOSITORY EN PERSISTENCIA.md`
- **Solución LSP**: `docs/SOLUCION LSP CON ABSTRACCIONES.md`
- **Implementación OCP**: `docs/IMPLEMENTACION DE OCP CON ABSTRACCIONES.md`
- **Proyecto principal**: `README.md` en raíz del proyecto

---

**📖 Paquete Didáctico - Victor Valotto**
**🎯 Objetivo**: Demostración de Repository Pattern + ISP correctamente aplicado
**🔄 Estado v6.0.0**: ISP corregido con interfaces segregadas (supervisor package)

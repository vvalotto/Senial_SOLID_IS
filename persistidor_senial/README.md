# Persistidor de Señales - Repository Pattern

**Versión**: 5.3.0
**Autor**: Victor Valotto
**Objetivo**: Demostración del Repository Pattern + Violación ISP Intencional (Didáctica)

## 📋 Descripción

Este paquete implementa el **Patrón Repository** para la persistencia de señales digitales, separando claramente la **lógica de dominio** (Repositorio) de la **infraestructura de persistencia** (Contexto).

## 🏗️ Arquitectura - Repository Pattern

```
┌─────────────────────────────────────────────────────────────┐
│                      CAPA DE DOMINIO                        │
│  ┌────────────────────────────────────────────────────┐     │
│  │  BaseRepositorio ⚠️ INTERFAZ "GORDA" (ISP)         │     │
│  │  - guardar(entidad) ✅                             │     │
│  │  - obtener(id_entidad) ✅                          │     │
│  │  - auditar(entidad, auditoria) ⚠️                  │     │
│  │  - trazar(entidad, accion, mensaje) ⚠️             │     │
│  └────────────────────────────────────────────────────┘     │
│                           ▲                                 │
│              ┌────────────┴────────────┐                    │
│              │                         │                    │
│  ┌───────────┴──────────┐  ┌──────────┴────────────┐       │
│  │  RepositorioSenial   │  │  RepositorioUsuario   │       │
│  │  ✅ USA los 4 métodos │  │  ❌ Solo usa 2/4      │       │
│  │  (señales necesitan  │  │  (usuarios NO         │       │
│  │   auditoría)         │  │   necesitan auditoría)│       │
│  └──────────────────────┘  └───────────────────────┘       │
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
❌ **VIOLACIÓN INTENCIONAL CON FINES DIDÁCTICOS (v5.3.0)**:

**Problema**: `BaseRepositorio` es una interfaz "gorda" con 4 métodos abstractos:
- `guardar()` ✅ Todos los repositorios lo necesitan
- `obtener()` ✅ Todos los repositorios lo necesitan
- `auditar()` ⚠️ Solo `RepositorioSenial` lo necesita
- `trazar()` ⚠️ Solo `RepositorioSenial` lo necesita

**Consecuencia**: `RepositorioUsuario` está FORZADO a implementar `auditar()` y `trazar()`:
```python
def auditar(self, entidad, auditoria):
    raise NotImplementedError("RepositorioUsuario no soporta auditoría - Violación ISP")
```

**Resultado**: Código frágil que falla en runtime si se intenta usar auditoría en usuarios.

**Corrección planificada**: Segregar en `IRepositorioBasico` + `IRepositorioAuditable`

### 5. DIP (Dependency Inversion Principle)
✅ **APLICADO CORRECTAMENTE**:
- Repositorio depende de abstracción `BaseContexto`, no de implementaciones concretas
- Contexto inyectado vía constructor: `RepositorioSenial(contexto)`

## 🏗️ Componentes

### Repositorios (Capa de Dominio)

#### `BaseRepositorio`
⚠️ **Interfaz "Gorda" - Violación ISP Intencional**

Abstracción que define la interfaz de dominio para persistencia con métodos innecesarios para algunos clientes.

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

    @abstractmethod
    def auditar(self, entidad, auditoria):
        """⚠️ PROBLEMÁTICO - No todos los repositorios necesitan auditoría"""
        pass

    @abstractmethod
    def trazar(self, entidad, accion, mensaje):
        """⚠️ PROBLEMÁTICO - No todos los repositorios necesitan trazabilidad"""
        pass
```

#### `RepositorioSenial`
✅ **Repositorio que USA todos los métodos** - Sin problemas ISP

Repositorio específico para gestionar señales con auditoría completa.

```python
from persistidor_senial import RepositorioSenial, ContextoPickle

# Crear contexto de persistencia (infraestructura)
contexto = ContextoPickle("./datos")

# Crear repositorio con contexto inyectado (DIP)
repo = RepositorioSenial(contexto)

# API de dominio - Todos los métodos funcionan
senial.id = 1000
repo.guardar(senial)  # ✅ Guardar
senial_recuperada = repo.obtener("1000")  # ✅ Recuperar
repo.auditar(senial, "Señal procesada correctamente")  # ✅ Auditar
repo.trazar(senial, "PROCESAMIENTO", "Amplificación x4")  # ✅ Trazar
```

#### `RepositorioUsuario`
❌ **Repositorio que SUFRE violación ISP** - Métodos innecesarios

Repositorio específico para gestionar usuarios (solo persistencia, sin auditoría).

```python
from persistidor_senial import RepositorioUsuario, ContextoArchivo

contexto = ContextoArchivo("./usuarios")
repo = RepositorioUsuario(contexto)

usuario.id = 500
repo.guardar(usuario)  # ✅ Funciona
usuario_recuperado = repo.obtener("500")  # ✅ Funciona

# ❌ Estos métodos FALLAN en runtime
repo.auditar(usuario, "...")  # 💥 NotImplementedError
repo.trazar(usuario, "LOGIN", "...")  # 💥 NotImplementedError
```

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

## ⚠️ Violación ISP Intencional (Fines Didácticos)

### Problema Central: Interfaz "Gorda" en `BaseRepositorio`

**BaseRepositorio** obliga a implementar 4 métodos abstractos, pero NO todos los clientes los necesitan:

| Método | RepositorioSenial | RepositorioUsuario | ¿Problema ISP? |
|--------|-------------------|---------------------|----------------|
| `guardar()` | ✅ Necesita | ✅ Necesita | ✅ OK |
| `obtener()` | ✅ Necesita | ✅ Necesita | ✅ OK |
| `auditar()` | ✅ Necesita | ❌ NO necesita | ⚠️ **VIOLACIÓN ISP** |
| `trazar()` | ✅ Necesita | ❌ NO necesita | ⚠️ **VIOLACIÓN ISP** |

### Consecuencias de la Violación

**RepositorioUsuario** está forzado a implementar métodos innecesarios:

```python
class RepositorioUsuario(BaseRepositorio):
    def guardar(self, usuario):
        # ✅ Implementación REAL
        self._contexto.persistir(usuario, str(usuario.id))

    def obtener(self, id_usuario, entidad=None):
        # ✅ Implementación REAL
        return self._contexto.recuperar(id_usuario, entidad)

    def auditar(self, entidad, auditoria):
        # ❌ STUB - Método innecesario
        raise NotImplementedError("RepositorioUsuario no soporta auditoría")

    def trazar(self, entidad, accion, mensaje):
        # ❌ STUB - Método innecesario
        raise NotImplementedError("RepositorioUsuario no soporta trazabilidad")
```

### Impacto en Código Cliente

```python
repo_usuario = RepositorioUsuario(contexto)

# ✅ Métodos que funcionan
repo_usuario.guardar(usuario)
usuario_recuperado = repo_usuario.obtener("1")

# ❌ Métodos que FALLAN en runtime
repo_usuario.auditar(usuario, "...")  # 💥 NotImplementedError
repo_usuario.trazar(usuario, "...", "...")  # 💥 NotImplementedError
```

**Problema**: Código frágil que compila pero falla en ejecución.

### Corrección Planificada (ISP)

Segregar `BaseRepositorio` en interfaces específicas:

```python
# Interfaz básica - TODOS la necesitan
class IRepositorioBasico(ABC):
    @abstractmethod
    def guardar(self, entidad: Any) -> None:
        pass

    @abstractmethod
    def obtener(self, id_entidad: str, entidad: Any = None) -> Any:
        pass

# Interfaz especializada - SOLO para auditables
class IRepositorioAuditable(ABC):
    @abstractmethod
    def auditar(self, entidad, auditoria):
        pass

    @abstractmethod
    def trazar(self, entidad, accion, mensaje):
        pass

# Composición según necesidades reales
class RepositorioSenial(IRepositorioBasico, IRepositorioAuditable):
    # Implementa los 4 métodos - Sin problemas
    pass

class RepositorioUsuario(IRepositorioBasico):
    # Solo implementa 2 métodos - ¡Sin stubs innecesarios!
    pass
```

**Beneficios**:
- ✅ Clientes solo implementan lo que realmente necesitan
- ✅ No hay métodos stub que lancen excepciones
- ✅ Contratos honestos y respetados
- ✅ Mayor flexibilidad y mantenibilidad

### Demostración Interactiva

Ejecutar script de demostración completo:

```bash
python demo_violacion_isp.py
```

Este script muestra:
1. ✅ `RepositorioSenial` usando los 4 métodos exitosamente
2. ❌ `RepositorioUsuario` fallando al intentar auditar/trazar
3. 📚 Explicación de la solución ISP correcta

## 🔄 Próximas Mejoras

- [ ] Aplicar ISP: Segregar interfaces por responsabilidad
- [ ] Implementar sistema de trazabilidad dedicado (`IAuditable`)
- [ ] Agregar soporte para transacciones
- [ ] Implementar caché de entidades
- [ ] Agregar tests unitarios y de integración
- [ ] Soporte para contextos adicionales (SQL, MongoDB, Cloud Storage)

## 📖 Documentación Relacionada

- **Patrón Repository**: `docs/PATRON REPOSITORY EN PERSISTENCIA.md`
- **Solución LSP**: `docs/SOLUCION LSP CON ABSTRACCIONES.md`
- **Implementación OCP**: `docs/IMPLEMENTACION DE OCP CON ABSTRACCIONES.md`
- **Proyecto principal**: `README.md` en raíz del proyecto

---

**📖 Paquete Didáctico - Victor Valotto**
**🎯 Objetivo**: Demostración de Repository Pattern + violaciones ISP intencionales
**🔄 Estado v1.0.0**: Funcional con violaciones ISP para fines educativos

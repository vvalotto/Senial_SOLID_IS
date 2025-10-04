# Senial SOLID v6.0.0 - Release Distribution

Distribución completa del sistema de procesamiento de señales con principios SOLID.

## Contenido

```
packaging/release/
├── wheels/          # Paquetes wheels (instalación rápida)
├── source/          # Código fuente (tar.gz)
├── config/          # Configuración de ejemplo
├── docs/            # Documentación
└── README.md        # Este archivo
```

## Instalación Rápida

### Linux/macOS

```bash
# Desde el directorio raíz del proyecto
./packaging/install/install.sh

# O desde este directorio (packaging/release/)
../install/install.sh
```

### Windows

```cmd
REM Desde el directorio raíz del proyecto
packaging\install\install.bat

REM O desde este directorio (packaging\release\)
..\install\install.bat
```

## Instalación Manual

**IMPORTANTE**: Debes instalar TODOS los paquetes en orden porque no están publicados en PyPI.

```bash
# Opción A: Instalar todos a la vez (más simple)
pip install wheels/*.whl

# Opción B: Instalar en orden de dependencias
pip install wheels/supervisor-1.0.0-py3-none-any.whl
pip install wheels/dominio_senial-5.0.0-py3-none-any.whl
pip install wheels/adquisicion_senial-3.0.0-py3-none-any.whl
pip install wheels/procesamiento_senial-3.0.0-py3-none-any.whl
pip install wheels/presentacion_senial-2.0.0-py3-none-any.whl
pip install wheels/persistidor_senial-7.0.0-py3-none-any.whl
pip install wheels/configurador-3.0.0-py3-none-any.whl
pip install wheels/lanzador-6.0.0-py3-none-any.whl
pip install wheels/senial_solid-6.0.0-py3-none-any.whl
```

**Nota**: No puedes instalar solo `senial_solid-6.0.0-py3-none-any.whl` porque necesita los otros paquetes.

## Uso

```bash
# Comando directo (si instalado con pip)
senial-solid

# O como módulo
python -m lanzador.lanzador
```

## Componentes Incluidos

- **dominio-senial** v5.0.0 - Entidades del dominio (SenialBase, FactorySenial)
- **adquisicion-senial** v3.0.0 - Adquisidores de señales
- **procesamiento-senial** v3.0.0 - Procesadores de señales
- **presentacion-senial** v2.0.0 - Visualización de señales
- **persistidor-senial** v7.0.0 - Persistencia con patrón Repository
- **supervisor** v1.0.0 - Auditoría y trazabilidad (ISP)
- **configurador** v3.0.0 - Factory centralizado con config JSON (DIP)
- **lanzador** v6.0.0 - Orquestador principal
- **senial-solid** v6.0.0 - Meta-paquete (instala todos)

## Requisitos

- Python >= 3.8
- pip >= 21.0

## Configuración

El archivo `config/config.json` contiene la configuración de ejemplo. Para usarlo:

```bash
# Copiar a directorio de usuario
mkdir -p ~/.senial_solid
cp config/config.json ~/.senial_solid/

# O editar el config.json en el paquete configurador
```

## Documentación

Ver `docs/` para documentación completa:

- `ESTADO_Y_PROXIMOS_PASOS.md` - Estado actual del proyecto
- `APLICACION_DIP_CONFIGURACION_EXTERNA.md` - DIP con JSON
- `PLAN_PAQUETIZACION_PASO_A_PASO.md` - Proceso de build
- `PATRON REPOSITORY EN PERSISTENCIA.md` - Patrón Repository
- Y más...

## Verificación de Instalación

Después de instalar, verificar con:

```bash
python -c "import dominio_senial, adquisicion_senial, procesamiento_senial, presentacion_senial, persistidor_senial, supervisor, configurador, lanzador; print('✓ Todo instalado correctamente')"
```

## Licencia

MIT License - Ver LICENSE

## Autor

Victor Valotto - vvalotto@gmail.com

## Versión

6.0.0 - DIP Completo con Configuración Externa + Paquetización Multiplataforma

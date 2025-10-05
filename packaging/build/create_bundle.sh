#!/bin/bash
# create_bundle.sh - Crear bundle de instalación auto-contenido

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PACKAGING_DIR="$(dirname "$SCRIPT_DIR")"
RELEASE_DIR="$PACKAGING_DIR/release"
BUNDLE_NAME="senial_solid-v6.0.0"
BUNDLE_DIR="$RELEASE_DIR/$BUNDLE_NAME"

# Colores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

print_step() { echo -e "${BLUE}==>${NC} $1"; }
print_success() { echo -e "${GREEN}✓${NC} $1"; }
print_error() { echo -e "${RED}✗${NC} $1"; }

echo "================================================"
echo "  Creación de Bundle de Instalación"
echo "  Senial SOLID v6.0.0"
echo "================================================"
echo ""

# Verificar que existan los wheels
if [ ! -d "$RELEASE_DIR/wheels" ]; then
    print_error "Directorio wheels no encontrado"
    echo "Ejecuta primero: ./packaging/build/build_all.sh"
    exit 1
fi

wheel_count=$(ls -1 "$RELEASE_DIR/wheels/"*.whl 2>/dev/null | wc -l)
if [ "$wheel_count" -lt 9 ]; then
    print_error "Faltan wheels. Se esperan 9, se encontraron $wheel_count"
    echo "Ejecuta primero: ./packaging/build/build_all.sh"
    exit 1
fi

# Limpiar bundle anterior
print_step "Limpiando bundle anterior..."
rm -rf "$BUNDLE_DIR"
rm -f "$RELEASE_DIR/$BUNDLE_NAME.tar.gz"
print_success "Limpieza completada"

# Crear estructura del bundle
print_step "Creando estructura del bundle..."
mkdir -p "$BUNDLE_DIR/wheels"
print_success "Estructura creada"

# Copiar wheels
print_step "Copiando wheels..."
cp "$RELEASE_DIR/wheels/"*.whl "$BUNDLE_DIR/wheels/"
wheel_count=$(ls -1 "$BUNDLE_DIR/wheels/"*.whl | wc -l)
print_success "$wheel_count wheels copiados"

# Copiar config.json
print_step "Copiando config.json..."
if [ -f "$RELEASE_DIR/config/config.json" ]; then
    cp "$RELEASE_DIR/config/config.json" "$BUNDLE_DIR/"
    print_success "config.json copiado"
else
    print_error "config.json no encontrado en $RELEASE_DIR/config/"
    exit 1
fi

# Copiar script de instalación
print_step "Copiando script de instalación..."
if [ -f "$PACKAGING_DIR/install/install.sh" ]; then
    cp "$PACKAGING_DIR/install/install.sh" "$BUNDLE_DIR/"
    chmod +x "$BUNDLE_DIR/install.sh"
    print_success "install.sh copiado"
else
    print_error "install.sh no encontrado"
    exit 1
fi

# Crear README del bundle
print_step "Creando README del bundle..."
cat > "$BUNDLE_DIR/README.txt" << 'EOF'
SENIAL SOLID v6.0.0 - Instalación
==================================

Este paquete contiene todo lo necesario para instalar Senial SOLID.

CONTENIDO:
  - wheels/          : Paquetes Python (.whl) listos para instalar
  - config.json      : Archivo de configuración del sistema
  - install.sh       : Script de instalación automática (Linux/macOS)
  - README.txt       : Este archivo

INSTALACIÓN RÁPIDA:
-------------------

1. Descomprimir este archivo:
   tar -xzf senial_solid-v6.0.0.tar.gz
   cd senial_solid-v6.0.0

2. Ejecutar el instalador:
   ./install.sh

El script creará automáticamente:
  - Entorno virtual 'senial_env'
  - Instalará todos los paquetes
  - Configurará directorios en ~/.senial_solid/

EJECUCIÓN:
----------
Después de la instalación:

  source senial_env/bin/activate
  senial-solid

REQUISITOS:
-----------
  - Python 3.8 o superior
  - pip

SOPORTE:
--------
Para más información, consulta la documentación completa en:
https://github.com/tu-usuario/senial_solid

EOF
print_success "README creado"

# Comprimir bundle
print_step "Comprimiendo bundle..."
cd "$RELEASE_DIR"
tar -czf "$BUNDLE_NAME.tar.gz" "$BUNDLE_NAME"
bundle_size=$(du -h "$BUNDLE_NAME.tar.gz" | cut -f1)
print_success "Bundle comprimido: $bundle_size"

# Limpiar directorio temporal
print_step "Limpiando archivos temporales..."
rm -rf "$BUNDLE_DIR"
print_success "Limpieza completada"

echo ""
echo "================================================"
print_success "Bundle creado exitosamente"
echo "================================================"
echo ""
echo "📦 Archivo: $BUNDLE_NAME.tar.gz"
echo "📁 Ubicación: $RELEASE_DIR/"
echo "📊 Tamaño: $bundle_size"
echo ""
echo "DISTRIBUCIÓN:"
echo "  1. Envía el archivo: $BUNDLE_NAME.tar.gz"
echo "  2. Usuario descomprime: tar -xzf $BUNDLE_NAME.tar.gz"
echo "  3. Usuario ejecuta: cd $BUNDLE_NAME && ./install.sh"
echo ""

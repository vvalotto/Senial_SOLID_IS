#!/bin/bash
# install.sh - Instalación de Senial SOLID desde bundle

set -e

# Detectar si se ejecuta desde bundle o desde repo
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Si existe wheels/ en el directorio actual, es bundle
if [ -d "$SCRIPT_DIR/wheels" ]; then
    # Modo bundle
    WHEELS_DIR="$SCRIPT_DIR/wheels"
    CONFIG_FILE="$SCRIPT_DIR/config.json"
else
    # Modo repo
    PACKAGING_DIR="$(dirname "$SCRIPT_DIR")"
    RELEASE_DIR="$PACKAGING_DIR/release"
    WHEELS_DIR="$RELEASE_DIR/wheels"
    CONFIG_FILE="$RELEASE_DIR/config/config.json"
fi

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
NC='\033[0m'

print_step() { echo -e "${BLUE}==>${NC} $1"; }
print_success() { echo -e "${GREEN}✓${NC} $1"; }
print_warning() { echo -e "${YELLOW}⚠${NC} $1"; }
print_error() { echo -e "${RED}✗${NC} $1"; }

check_python() {
    print_step "Verificando Python..."
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 no encontrado"
        echo "Por favor instala Python 3.8 o superior"
        exit 1
    fi
    python_version=$(python3 --version | cut -d' ' -f2)
    print_success "Python $python_version detectado"
}

check_pip() {
    print_step "Verificando pip..."
    if ! python3 -m pip --version &> /dev/null; then
        print_error "pip no encontrado"
        exit 1
    fi
    print_success "pip encontrado"
}

create_venv() {
    print_step "Creando entorno virtual 'senial_env'..."
    if [ -d "senial_env" ]; then
        print_warning "El entorno virtual ya existe"
        read -p "¿Desea recrearlo? [y/N]: " choice
        case "$choice" in
            y|Y)
                rm -rf senial_env
                python3 -m venv senial_env
                ;;
            *)
                ;;
        esac
    else
        python3 -m venv senial_env
    fi
    source senial_env/bin/activate
    print_success "Entorno virtual activado"
}

install_from_wheels() {
    print_step "Instalando paquetes desde wheels..."

    if [ ! -d "$WHEELS_DIR" ]; then
        print_error "Directorio wheels no encontrado: $WHEELS_DIR"
        exit 1
    fi

    wheel_count=$(ls -1 "$WHEELS_DIR/"*.whl 2>/dev/null | wc -l)
    if [ "$wheel_count" -lt 9 ]; then
        print_error "Faltan wheels. Se esperan 9, se encontraron $wheel_count"
        exit 1
    fi

    print_step "Actualizando pip..."
    python3 -m pip install --upgrade pip --quiet

    echo ""
    print_step "Instalando componentes..."

    pip install "$WHEELS_DIR/supervisor"*.whl --quiet && echo "  ✓ supervisor"
    pip install "$WHEELS_DIR/dominio_senial"*.whl --quiet && echo "  ✓ dominio_senial"
    pip install "$WHEELS_DIR/adquisicion_senial"*.whl --quiet && echo "  ✓ adquisicion_senial"
    pip install "$WHEELS_DIR/procesamiento_senial"*.whl --quiet && echo "  ✓ procesamiento_senial"
    pip install "$WHEELS_DIR/presentacion_senial"*.whl --quiet && echo "  ✓ presentacion_senial"
    pip install "$WHEELS_DIR/persistidor_senial"*.whl --quiet && echo "  ✓ persistidor_senial"
    pip install "$WHEELS_DIR/configurador"*.whl --quiet && echo "  ✓ configurador"
    pip install "$WHEELS_DIR/lanzador"*.whl --quiet && echo "  ✓ lanzador"
    pip install "$WHEELS_DIR/senial_solid"*.whl --quiet && echo "  ✓ senial_solid"

    echo ""
    print_success "Todos los paquetes instalados"
}

setup_config() {
    print_step "Configurando directorio de trabajo..."
    mkdir -p ~/.senial_solid/tmp/datos/adquisicion
    mkdir -p ~/.senial_solid/tmp/datos/procesamiento

    if [ -f "$CONFIG_FILE" ]; then
        if [ -f ~/.senial_solid/config.json ]; then
            print_warning "Ya existe config.json en ~/.senial_solid/"
            read -p "¿Desea sobrescribirlo? [y/N]: " choice
            case "$choice" in
                y|Y)
                    cp "$CONFIG_FILE" ~/.senial_solid/config.json
                    print_success "Configuración actualizada"
                    ;;
                *)
                    print_success "Configuración existente conservada"
                    ;;
            esac
        else
            cp "$CONFIG_FILE" ~/.senial_solid/config.json
            print_success "Configuración copiada a: ~/.senial_solid/config.json"
        fi
    fi

    print_success "Directorio de trabajo configurado"
}

verify_installation() {
    print_step "Verificando instalación..."
    python3 -c "from dominio_senial import SenialBase" 2>/dev/null && echo "  ✓ dominio_senial"
    python3 -c "from configurador import Configurador" 2>/dev/null && echo "  ✓ configurador"
    python3 -c "from lanzador import Lanzador" 2>/dev/null && echo "  ✓ lanzador"
    print_success "Verificación completada"
}

cleanup_files() {
    # Solo limpiar si estamos en modo bundle (existe wheels/ en directorio actual)
    if [ -d "$SCRIPT_DIR/wheels" ]; then
        print_step "Limpiando archivos temporales..."

        # Eliminar wheels
        if [ -d "$SCRIPT_DIR/wheels" ]; then
            rm -rf "$SCRIPT_DIR/wheels"
        fi

        # Eliminar config.json de la raíz del bundle
        if [ -f "$SCRIPT_DIR/config.json" ]; then
            rm -f "$SCRIPT_DIR/config.json"
        fi

        print_success "Archivos temporales eliminados"
    fi
}

show_summary() {
    echo ""
    echo "================================================"
    print_success "Instalación completada exitosamente"
    echo "================================================"
    echo ""
    echo "Para ejecutar Senial SOLID:"
    echo ""
    echo "  1. Activar entorno virtual:"
    echo "     source senial_env/bin/activate"
    echo ""
    echo "  2. Ejecutar aplicación:"
    echo "     senial-solid"
    echo "     o"
    echo "     python -m lanzador.lanzador"
    echo ""
    echo "Configuración:"
    echo "  📁 ~/.senial_solid/config.json"
    echo "  📁 ~/.senial_solid/tmp/datos/"
    echo ""
}

main() {
    echo "================================================"
    echo "  Instalación de Senial SOLID v6.0.0"
    echo "================================================"
    echo ""

    check_python
    check_pip
    create_venv
    install_from_wheels
    setup_config
    verify_installation
    cleanup_files
    show_summary
}

main

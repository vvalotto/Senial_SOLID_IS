#!/usr/bin/env python3
"""Script de verificación de instalación"""

import sys

def verificar():
    print("=" * 60)
    print("  Verificación de Instalación - Senial SOLID v6.0.0")
    print("=" * 60)
    print()

    componentes = [
        'dominio_senial',
        'adquisicion_senial',
        'procesamiento_senial',
        'presentacion_senial',
        'persistidor_senial',
        'supervisor',
        'configurador',
        'lanzador'
    ]

    errors = 0

    for comp in componentes:
        try:
            __import__(comp)
            print(f"✓ {comp}")
        except ImportError as e:
            print(f"✗ {comp} - ERROR: {e}")
            errors += 1

    print()
    print("=" * 60)

    if errors == 0:
        print("✓ Todos los componentes instalados correctamente")
        return 0
    else:
        print(f"✗ {errors} componente(s) con errores")
        return 1

if __name__ == "__main__":
    sys.exit(verificar())

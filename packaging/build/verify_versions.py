#!/usr/bin/env python3
"""
Script de verificación de versiones de paquetes.
Verifica consistencia entre setup.py de todos los paquetes.
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Tuple

class Colors:
    GREEN = '\033[0;32m'
    BLUE = '\033[0;34m'
    YELLOW = '\033[0;33m'
    RED = '\033[0;31m'
    NC = '\033[0m'

class VersionVerifier:
    """Verificador de versiones de paquetes"""

    def __init__(self, root_dir: str = "."):
        self.root_dir = Path(root_dir).resolve()
        self.packages = [
            ("supervisor", "supervisor"),
            ("dominio_senial", "dominio-senial"),
            ("adquisicion_senial", "adquisicion-senial"),
            ("procesamiento_senial", "procesamiento-senial"),
            ("presentacion_senial", "presentacion-senial"),
            ("persistidor_senial", "persistidor-senial"),
            ("configurador", "configurador"),
            ("lanzador", "lanzador"),
        ]
        self.versions = {}
        self.dependencies = {}
        self.errors = []

    def extract_version(self, setup_path: Path) -> str:
        """Extraer versión de setup.py"""
        if not setup_path.exists():
            return None

        content = setup_path.read_text()

        # Buscar version="X.Y.Z"
        match = re.search(r'version\s*=\s*["\']([^"\']+)["\']', content)
        if match:
            return match.group(1)

        return None

    def extract_dependencies(self, setup_path: Path) -> List[str]:
        """Extraer install_requires de setup.py"""
        if not setup_path.exists():
            return []

        content = setup_path.read_text()

        # Buscar install_requires=[...]
        match = re.search(
            r'install_requires\s*=\s*\[(.*?)\]',
            content,
            re.DOTALL
        )

        if not match:
            return []

        deps_text = match.group(1)

        # Extraer cada dependencia
        deps = []
        for line in deps_text.split('\n'):
            line = line.strip().strip(',').strip('"').strip("'")
            if line and not line.startswith('#'):
                deps.append(line)

        return deps

    def verify_all_packages(self):
        """Verificar todas las versiones"""
        print(f"{Colors.BLUE}==>{Colors.NC} Verificando versiones de paquetes...\n")

        for dir_name, package_name in self.packages:
            setup_path = self.root_dir / dir_name / "setup.py"

            version = self.extract_version(setup_path)
            if version:
                self.versions[package_name] = version
                print(f"  {Colors.GREEN}✓{Colors.NC} {package_name}: v{version}")
            else:
                error = f"No se encontró versión en {setup_path}"
                self.errors.append(error)
                print(f"  {Colors.RED}✗{Colors.NC} {package_name}: {error}")

            deps = self.extract_dependencies(setup_path)
            if deps:
                self.dependencies[package_name] = deps

    def check_dependency_consistency(self):
        """Verificar consistencia de dependencias"""
        print(f"\n{Colors.BLUE}==>{Colors.NC} Verificando consistencia de dependencias...\n")

        for package, deps in self.dependencies.items():
            for dep in deps:
                # Parsear dependencia (ej: "dominio-senial>=5.0.0")
                match = re.match(r'([a-z-]+)([><=]+)([0-9.]+)', dep)
                if not match:
                    continue

                dep_name = match.group(1)
                operator = match.group(2)
                required_version = match.group(3)

                if dep_name not in self.versions:
                    continue

                actual_version = self.versions[dep_name]

                # Verificación simple (solo para >=)
                if operator == ">=":
                    if self._compare_versions(actual_version, required_version) >= 0:
                        print(f"  {Colors.GREEN}✓{Colors.NC} {package} requiere "
                              f"{dep_name}>={required_version} (actual: {actual_version})")
                    else:
                        error = (f"{package} requiere {dep_name}>={required_version} "
                                f"pero versión actual es {actual_version}")
                        self.errors.append(error)
                        print(f"  {Colors.RED}✗{Colors.NC} {error}")

    def _compare_versions(self, v1: str, v2: str) -> int:
        """Comparar versiones (v1 vs v2). Retorna: 1 si v1>v2, 0 si igual, -1 si v1<v2"""
        v1_parts = [int(x) for x in v1.split('.')]
        v2_parts = [int(x) for x in v2.split('.')]

        for i in range(max(len(v1_parts), len(v2_parts))):
            p1 = v1_parts[i] if i < len(v1_parts) else 0
            p2 = v2_parts[i] if i < len(v2_parts) else 0

            if p1 > p2:
                return 1
            elif p1 < p2:
                return -1

        return 0

    def print_report(self):
        """Imprimir reporte final"""
        print("\n" + "=" * 60)

        if self.errors:
            print(f"{Colors.RED}✗ Verificación FALLÓ{Colors.NC}")
            print(f"\n{Colors.RED}Errores encontrados:{Colors.NC}")
            for error in self.errors:
                print(f"  • {error}")
            return False
        else:
            print(f"{Colors.GREEN}✓ Todas las versiones son consistentes{Colors.NC}")
            return True

    def run(self) -> bool:
        """Ejecutar verificación completa"""
        print("=" * 60)
        print("  Verificación de Versiones - Senial SOLID v6.0.0")
        print("=" * 60)
        print()

        self.verify_all_packages()
        self.check_dependency_consistency()
        success = self.print_report()

        print("=" * 60)
        print()

        return success

if __name__ == "__main__":
    import sys
    verifier = VersionVerifier()
    success = verifier.run()
    sys.exit(0 if success else 1)

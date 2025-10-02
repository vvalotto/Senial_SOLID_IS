"""
Setup para el paquete configurador
"""
from setuptools import setup, find_packages

setup(
    name="configurador",
    version="2.3.0",
    description="Factory centralizado con Repository Pattern - SRP + OCP + LSP + DIP aplicados",
    author="Victor Valotto",
    packages=find_packages(),
    install_requires=[
        "dominio-senial>=4.0.0",
        "adquisicion-senial>=2.1.0",
        "procesamiento-senial>=2.1.0",
        "presentacion-senial>=2.0.0",
        "persistidor-senial>=1.0.0"
    ],
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
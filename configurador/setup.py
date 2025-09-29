"""
Setup para el paquete configurador
"""
from setuptools import setup, find_packages

setup(
    name="configurador",
    version="1.0.0",
    description="Factory centralizado para creación de objetos en la aplicación de procesamiento de señales",
    author="Victor Valotto",
    packages=find_packages(),
    install_requires=[
        "dominio-senial>=1.0.0",
        "adquisicion-senial>=1.0.0",
        "procesamiento-senial>=2.0.0",
        "presentacion-senial>=1.0.0"
    ],
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
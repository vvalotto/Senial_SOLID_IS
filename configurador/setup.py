"""
Setup para el paquete configurador
"""
from setuptools import setup, find_packages

setup(
    name="configurador",
    version="2.1.1",
    description="Factory centralizado con inyección de dependencias - SRP + DIP aplicados",
    author="Victor Valotto",
    packages=find_packages(),
    install_requires=[
        "dominio-senial>=4.0.0",
        "adquisicion-senial>=2.1.0",
        "procesamiento-senial>=2.1.0",
        "presentacion-senial>=2.0.0"
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
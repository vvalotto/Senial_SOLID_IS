"""
Setup para el paquete configurador

Versión 3.0.0 - DIP Completo con Configuración Externa JSON
Factory centralizado que delega en Factories especializados y lee
toda la configuración desde archivos JSON externos.
"""
from setuptools import setup, find_packages

setup(
    name="configurador",
    version="3.0.0",
    description="Factory centralizado con configuración JSON externa - DIP completo aplicado",
    long_description="Factory centralizado que implementa DIP completo mediante configuración "
                     "externa JSON y delegación a Factories especializados (FactorySenial, "
                     "FactoryAdquisidor, FactoryProcesador, FactoryContexto)",
    author="Victor Valotto",
    package_dir={'configurador': '.'},
    packages=['configurador'],
    package_data={
        'configurador': ['config.json'],
    },
    include_package_data=True,
    install_requires=[
        "dominio-senial>=5.0.0",
        "adquisicion-senial>=3.0.0",
        "procesamiento-senial>=3.0.0",
        "presentacion-senial>=2.0.0",
        "persistidor-senial>=7.0.0"
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
        "Programming Language :: Python :: 3.12",
    ],
)
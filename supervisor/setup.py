"""
Setup para el paquete supervisor
"""
from setuptools import setup, find_packages

setup(
    name="supervisor",
    version="1.0.0",
    description="Paquete de auditoría y trazabilidad - Demostración de ISP correctamente aplicado",
    long_description=open('../README.md', encoding='utf-8').read() if __name__ == '__main__' else '',
    long_description_content_type="text/markdown",
    author="Victor Valotto",
    author_email="vvalotto@gmail.com",
    url="https://github.com/vvalotto/Senial_SOLID_IS",
    license="MIT",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        # Sin dependencias externas - paquete standalone
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Education",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Logging",
    ],
    keywords="solid principles, ISP, interface segregation, audit, trace, logging, supervision, education",
    project_urls={
        "Bug Reports": "https://github.com/vvalotto/Senial_SOLID_IS/issues",
        "Source": "https://github.com/vvalotto/Senial_SOLID_IS",
        "Documentation": "https://github.com/vvalotto/Senial_SOLID_IS/blob/main/README.md",
    },
)

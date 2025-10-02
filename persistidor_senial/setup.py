"""
Setup para el paquete persistidor_senial
"""
from setuptools import setup, find_packages

setup(
    name="persistidor-senial",
    version="1.0.0",
    description="Repository Pattern con Strategy para persistencia - Demostración SOLID (SRP + OCP + LSP + DIP) + violaciones ISP intencionales",
    author="Victor Valotto",
    author_email="vvalotto@gmail.com",
    url="https://github.com/vvalotto/Senial_SOLID_IS",
    license="MIT",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "dominio-senial>=4.0.0",
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
    ],
    keywords="solid principles, repository pattern, strategy pattern, ISP, DIP, persistence, signal processing, education",
    project_urls={
        "Bug Reports": "https://github.com/vvalotto/Senial_SOLID_IS/issues",
        "Source": "https://github.com/vvalotto/Senial_SOLID_IS",
        "Documentation": "https://github.com/vvalotto/Senial_SOLID_IS/blob/main/README.md",
    },
)

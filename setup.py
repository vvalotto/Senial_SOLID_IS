from setuptools import setup, find_packages

setup(
    name="solid-principles-study",
    version="0.1.0",
    description="Caso de estudio didáctico de los principios SOLID",
    author="Tu Nombre",
    author_email="tu.email@ejemplo.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=[
        "pytest>=7.0.0",
        "pytest-cov>=4.0.0",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
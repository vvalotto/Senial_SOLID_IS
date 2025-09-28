"""
Tests para la clase Senial del dominio
"""
import pytest
from dominio_senial import Senial


class TestSenial:
    """Tests unitarios para la clase Senial"""

    def test_crear_senial_vacia(self):
        """Test: Crear una señal vacía"""
        senial = Senial()
        assert senial.obtener_tamanio() == 0
        assert senial.esta_vacia() is True

    def test_poner_valor(self):
        """Test: Agregar valores a la señal"""
        senial = Senial()
        senial.poner_valor(1.5)
        senial.poner_valor(2.0)

        assert senial.obtener_tamanio() == 2
        assert senial.esta_vacia() is False

    def test_obtener_valor(self):
        """Test: Obtener valores por índice"""
        senial = Senial()
        senial.poner_valor(1.5)
        senial.poner_valor(2.0)

        assert senial.obtener_valor(0) == 1.5
        assert senial.obtener_valor(1) == 2.0

    def test_obtener_valor_indice_invalido(self):
        """Test: Manejar índices fuera de rango"""
        senial = Senial()
        senial.poner_valor(1.0)

        # El comportamiento actual devuelve None para índices inválidos
        result = senial.obtener_valor(5)
        assert result is None

    def test_obtener_tamanio(self):
        """Test: Obtener el tamaño de la señal"""
        senial = Senial()
        assert senial.obtener_tamanio() == 0

        senial.poner_valor(1.0)
        assert senial.obtener_tamanio() == 1

        senial.poner_valor(2.0)
        assert senial.obtener_tamanio() == 2

    def test_esta_vacia(self):
        """Test: Verificar si la señal está vacía"""
        senial = Senial()
        assert senial.esta_vacia() is True

        senial.poner_valor(1.0)
        assert senial.esta_vacia() is False
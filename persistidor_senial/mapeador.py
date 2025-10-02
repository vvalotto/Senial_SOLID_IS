"""
Clases que mapean o serializan la estructura de clases en archivo de texto y viceversa
"""
from abc import ABCMeta, abstractmethod
from collections import deque
from typing import Any, List, Union


class Mapeador(metaclass=ABCMeta):
    lista_tipos_base = ['int', 'str', 'float', 'None', 'bool', 'date']

    def __init__(self):
        pass

    @staticmethod
    def tipo_dato(tipo: str, dato: str) -> Any:
        if tipo == 'int':
            return int(dato)
        elif tipo == 'str':
            return str(dato)
        elif tipo == 'float':
            return float(dato)
        elif tipo == 'bool':
            return bool(dato)
        else:
            return None

    @abstractmethod
    def ir_a_persistidor(self, entidad: Any) -> str:
        pass

    @abstractmethod
    def venir_desde_persistidor(self, entidad: Any, entidad_mapeada: str) -> Any:
        pass


class MapeadorArchivo(Mapeador):
    def __init__(self):
        super().__init__()
        self._objeto_mapeado = None

    def ir_a_persistidor(self, entidad):
        """
        Mapea la clase a una estructura para persistirla en un archivo.
        La clase es proporcionada por el argumento entidad.
        :param entidad: Objeto a persistir.
        :return: Cadena de texto que representa la entidad mapeada.
        """
        atr_lista = []
        # Inicializa la variable de mapeo serializada
        entidad_mapeada = ''

        # Si es un tipo base mapea solo el valor interno del objeto
        if entidad.__class__.__name__ in Mapeador.lista_tipos_base:
            entidad_mapeada += str(entidad) + ','
        else:
            # Recorre los miembros que son campos de la clase para el caso de una clase compleja
            # O sea una clase que contiene variables de intancia (campos)
            # Por lo tanto recorre los campos
            for atributo in entidad.__dict__.keys():
                # Si el campo es de tipo de clase base, lo mapea (lo serializa)
                if entidad.__dict__[atributo].__class__.__name__ in Mapeador.lista_tipos_base:
                    entidad_mapeada += atributo + ':' + str(entidad.__dict__[atributo]) + ','
                else:
                    # Si el clase contiene una coleccion (lista) lo agrega para procesarlo
                    # despues
                    if isinstance(entidad.__dict__[atributo], (list, deque)):
                        atr_lista.append(atributo)
                    else:
                        # Sin es un campo que corresponde a una clase compuesta
                        entidad_mapeada += atributo + ':' + self.ir_a_persistidor(atributo)
            entidad_mapeada += '\n'

            for atributo in atr_lista:
                if isinstance(entidad.__dict__[atributo], (list, deque)):
                    i = 0
                    for elemento in entidad.__dict__[atributo]:
                        # Saltar elementos None
                        if elemento is not None:
                            entidad_mapeada += atributo + '>' + str(i) + ':' + self.ir_a_persistidor(elemento)
                            i += 1
                            entidad_mapeada += '\n'
        return entidad_mapeada

    def venir_desde_persistidor(self, entidad: Any, entidad_mapeada: str) -> Any:
        """
        Desmapea la estructura persistida en un archivo a una clase.
        :param entidad: Objeto a desmapear.
        :param entidad_mapeada: Cadena de texto que representa la entidad mapeada.
        :return: Objeto desmapeado.
        """
        # separa la lineas del archivo
        sep_registros = entidad_mapeada.split('\n')
        for registro in sep_registros:
            if registro != '':
                # separa cada linea en campos(atributos)
                sep_campos = registro.split(',')
                for campo in sep_campos:
                    # separa cada campo en clave y valor
                    sep_valor = campo.split(':')
                    for atributo in entidad.__dict__.keys():
                        if atributo in sep_valor[0]:
                            if entidad.__dict__[atributo].__class__.__name__ in Mapeador.lista_tipos_base:
                                entidad.__dict__[atributo] = super().tipo_dato(
                                    entidad.__dict__[atributo].__class__.__name__,
                                    sep_valor[1]
                                )
                            elif isinstance(entidad.__dict__[atributo], (list, deque)):
                                entidad.__dict__[atributo].append(float(sep_valor[1]))
        return entidad
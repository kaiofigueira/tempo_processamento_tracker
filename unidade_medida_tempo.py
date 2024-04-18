from enum import Enum

class UnidadeMedidaTempo(Enum):
    """
    Enumeração para diferentes unidades de medida de tempo.

    Attributes:
        MILISEGUNDOS: Representa a unidade de medida de tempo em milissegundos.
        SEGUNDOS: Representa a unidade de medida de tempo em segundos.
        MINUTOS: Representa a unidade de medida de tempo em minutos.
        HORAS: Representa a unidade de medida de tempo em horas.
    
    Methods:
        None
    """

    MILISEGUNDOS = 'milisegundos'
    SEGUNDOS = 'segundos'
    MINUTOS = 'minutos'
    HORAS = 'horas'
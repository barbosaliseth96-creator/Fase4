class ClienteError(Exception):
    pass

class ServicioError(Exception):
    pass

class ReservaError(Exception):
    pass
from abc import ABC, abstractmethod

class Servicio(ABC):

    def __init__(self, nombre, precio):
        self.nombre = nombre
        self.precio = precio

    @abstractmethod
    def calcular_costo(self):
        pass

    @abstractmethod
    def descripcion(self):
        pass

import logging

logging.basicConfig(
    filename="logs.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

import logging

from cliente import Cliente
from servicio import (
    ReservaSala,
    AlquilerEquipo,
    AsesoriaEspecializada
)
from reserva import Reserva

logging.basicConfig(
    filename="logs.txt",
    level=logging.INFO
)

try:

    cliente1 = Cliente("Maria García", "maria@gmail.com")

    servicio1 = ReservaSala(3)

    reserva1 = Reserva(cliente1, servicio1)

    reserva1.confirmar()

    resultado = reserva1.procesar()

    print(resultado)

except Exception as e:

    logging.error(str(e))
    print("Error:", e)

finally:

    print("Fin de la operación")

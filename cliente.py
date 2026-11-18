
"""
Modulo de Clientes - Software FJ
Estudiante 2: Clientes y Validaciones.

Implementa encapsulamiento, atributos privados,
validaciones y excepciones personalizadas.
"""

import logging
import re


# Configuracion del registro de eventos y errores
logger = logging.getLogger("software_fj")

if not logger.handlers:
    logger.setLevel(logging.INFO)
    manejador = logging.FileHandler("logs.txt", encoding="utf-8")
    formato = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s"
    )
    manejador.setFormatter(formato)
    logger.addHandler(manejador)


# Excepciones personalizadas
class ClienteError(Exception):
    """Excepcion general del modulo de clientes."""
    pass


class CampoFaltanteError(ClienteError):
    """Error cuando falta un dato obligatorio."""
    pass


class DatoInvalidoError(ClienteError):
    """Error cuando un dato no cumple las validaciones."""
    pass


# Clase Cliente
class Cliente:

    def __init__(self, nombre, correo, identificacion=None):

        self.__nombre = self.__validar_nombre(nombre)
        self.__correo = self.__validar_correo(correo)

        # La identificacion se valida cuando se proporciona.
        self.__identificacion = (
            self.__validar_identificacion(identificacion)
            if identificacion is not None else None
        )

        logger.info("Cliente registrado: %s", self.__nombre)

    # Validacion de nombres
    @staticmethod
    def __validar_nombre(nombre):

        if not nombre or not str(nombre).strip():
            logger.error("Nombre del cliente faltante")
            raise CampoFaltanteError(
                "El nombre del cliente es obligatorio."
            )

        nombre = " ".join(str(nombre).strip().split())

        if not re.fullmatch(
            r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ ]{2,60}", nombre
        ):
            logger.error("Nombre de cliente invalido")
            raise DatoInvalidoError(
                "El nombre solo debe contener letras y espacios."
            )

        return nombre.title()

    # Validacion del correo electronico
    @staticmethod
    def __validar_correo(correo):

        if not correo or not str(correo).strip():
            logger.error("Correo del cliente faltante")
            raise CampoFaltanteError(
                "El correo electronico es obligatorio."
            )

        correo = str(correo).strip()

        patron = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

        if not re.fullmatch(patron, correo):
            logger.error("Correo electronico invalido")
            raise DatoInvalidoError(
                "El formato del correo electronico no es valido."
            )

        return correo.lower()

    # Validacion de identificacion
    @staticmethod
    def __validar_identificacion(identificacion):

        if not str(identificacion).strip():
            raise CampoFaltanteError(
                "La identificacion es obligatoria."
            )

        identificacion = str(identificacion).strip()

        if not re.fullmatch(r"\d{6,12}", identificacion):
            logger.error("Identificacion invalida")
            raise DatoInvalidoError(
                "La identificacion debe contener entre 6 y 12 digitos."
            )

        return identificacion

    # Propiedades para consultar los atributos privados
    @property
    def nombre(self):
        return self.__nombre

    @property
    def correo(self):
        return self.__correo

    @property
    def identificacion(self):
        return self.__identificacion

    # Actualizacion controlada del nombre
    @nombre.setter
    def nombre(self, nuevo_nombre):
        self.__nombre = self.__validar_nombre(nuevo_nombre)
        logger.info("Nombre del cliente actualizado")

    # Actualizacion controlada del correo
    @correo.setter
    def correo(self, nuevo_correo):
        self.__correo = self.__validar_correo(nuevo_correo)
        logger.info("Correo del cliente actualizado")

    def mostrar_informacion(self):
        return (
            f"Nombre: {self.__nombre} | "
            f"Correo: {self.__correo} | "
            f"Identificacion: "
            f"{self.__identificacion or 'No registrada'}"
        )

    def __str__(self):
        return self.mostrar_informacion()

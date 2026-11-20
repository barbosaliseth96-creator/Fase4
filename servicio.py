
"""
Modulo de Servicios - Software FJ
Estudiante 3: Herencia y Polimorfismo.

Contiene la clase abstracta Servicio y dos servicios
especializados: ReservaSala y AlquilerEquipo.
"""

import logging
from abc import ABC, abstractmethod


# Configuracion del registro de eventos
logger = logging.getLogger("software_fj")

if not logger.handlers:
    logger.setLevel(logging.INFO)

    manejador = logging.FileHandler(
        "logs.txt",
        encoding="utf-8"
    )

    formato = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s"
    )

    manejador.setFormatter(formato)
    logger.addHandler(manejador)


# Excepciones personalizadas
class ServicioError(Exception):
    """Excepcion general para errores de servicios."""
    pass


class ParametroServicioInvalidoError(ServicioError):
    """Error cuando los parametros del servicio son incorrectos."""
    pass


# Clase abstracta Servicio
class Servicio(ABC):

    def __init__(self, nombre, precio):

        if not nombre or not str(nombre).strip():
            raise ParametroServicioInvalidoError(
                "El nombre del servicio es obligatorio."
            )

        if (
            isinstance(precio, bool)
            or not isinstance(precio, (int, float))
            or precio <= 0
        ):
            raise ParametroServicioInvalidoError(
                "El precio debe ser un numero mayor que cero."
            )

        self.nombre = str(nombre).strip()
        self.precio = float(precio)

        logger.info(
            "Servicio creado: %s",
            self.nombre
        )

    @abstractmethod
    def calcular_costo(self):
        """Calcula el costo total del servicio."""
        pass

    @abstractmethod
    def descripcion(self):
        """Describe las caracteristicas del servicio."""
        pass


# Servicio especializado: Reserva de salas
class ReservaSala(Servicio):

    def __init__(
        self,
        horas,
        nombre="Reserva de sala",
        precio=50000
    ):

        if (
            isinstance(horas, bool)
            or not isinstance(horas, (int, float))
            or horas <= 0
        ):
            raise ParametroServicioInvalidoError(
                "Las horas de reserva deben ser mayores que cero."
            )

        super().__init__(nombre, precio)

        self.horas = horas

        logger.info(
            "Reserva de sala creada para %s horas.",
            self.horas
        )

    def calcular_costo(self):

        costo = self.precio * self.horas

        logger.info(
            "Costo de reserva de sala calculado: %.2f",
            costo
        )

        return round(costo, 2)

    def descripcion(self):

        return (
            f"{self.nombre}: reserva de sala por "
            f"{self.horas} horas. "
            f"Tarifa por hora: ${self.precio:,.2f}."
        )


# Servicio especializado: Alquiler de equipos
class AlquilerEquipo(Servicio):

    def __init__(
        self,
        cantidad=1,
        nombre="Alquiler de equipos",
        precio=20000
    ):

        if (
            isinstance(cantidad, bool)
            or not isinstance(cantidad, int)
            or cantidad <= 0
        ):
            raise ParametroServicioInvalidoError(
                "La cantidad de equipos debe ser mayor que cero."
            )

        super().__init__(nombre, precio)

        self.cantidad = cantidad

        logger.info(
            "Alquiler de %s equipos creado.",
            self.cantidad
        )

    def calcular_costo(self):

        costo = self.precio * self.cantidad

        logger.info(
            "Costo de alquiler de equipos calculado: %.2f",
            costo
        )

        return round(costo, 2)

    def descripcion(self):

        return (
            f"{self.nombre}: alquiler de "
            f"{self.cantidad} equipos. "
            f"Precio por equipo: ${self.precio:,.2f}."
        )
# ==============================================================================
# COMPLEMENTO ESTUDIANTE 4: Tercer servicio especializado y sobrecarga de costos
# ==============================================================================

class AsesoriaEspecializada(Servicio):
    """Servicio especializado de consultoría técnica o académica."""

    def __init__(self, sesiones=1, especialidad="Desarrollo de Software", nombre="Asesoría Especializada", precio=60000):
        super().__init__(nombre, precio)
        if not isinstance(sesiones, int) or sesiones <= 0:
            logger.error("Número de sesiones inválido: %s", sesiones)
            raise ParametroServicioInvalidoError("Las sesiones deben ser un entero mayor a cero.")
        if not especialidad or not str(especialidad).strip():
            logger.error("Especialidad vacía en AsesoriaEspecializada")
            raise ParametroServicioInvalidoError("La especialidad es obligatoria.")
        self.sesiones = sesiones
        self.especialidad = str(especialidad).strip()

    def calcular_costo(self):
        return round(self.precio * self.sesiones, 2)

    def calcular_costo_total(self, porcentaje_impuesto=0.0, descuento=0.0):
        """Método sobrecargado mediante parámetros opcionales (impuestos y descuentos)."""
        if porcentaje_impuesto < 0 or descuento < 0:
            raise ParametroServicioInvalidoError("Impuestos y descuentos no pueden ser negativos.")
        subtotal = self.calcular_costo()
        if descuento > subtotal:
            raise ParametroServicioInvalidoError("El descuento no puede superar el subtotal.")
        valor_con_descuento = subtotal - descuento
        total = valor_con_descuento * (1 + porcentaje_impuesto)
        return round(total, 2)

    def descripcion(self):
        return f"{self.nombre} ({self.especialidad}) - {self.sesiones} sesión(es) x ${self.precio:,.2f}"
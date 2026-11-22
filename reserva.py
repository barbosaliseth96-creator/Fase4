"""
Módulo de Reservas - Software FJ
Estudiante 5: Gestión de reservas, excepciones avanzadas y encadenamiento.
"""

import logging
from cliente import Cliente
from servicio import Servicio

logger = logging.getLogger("software_fj")


# Excepciones personalizadas para el módulo de reservas
class ReservaError(Exception):
    """Excepción base para errores relacionados con reservas."""
    pass


class ReservaInvalidaError(ReservaError):
    """Se lanza cuando los datos o entidades de la reserva no son válidos."""
    pass


class EstadoReservaError(ReservaError):
    """Se lanza cuando se intenta una transición de estado no permitida."""
    pass


class Reserva:
    """Integra un Cliente y un Servicio con control de estados y excepciones."""

    ESTADOS_VALIDOS = ("Pendiente", "Confirmada", "Cancelada")

    def __init__(self, codigo, cliente, servicio, fecha):
        try:
            if not codigo or not str(codigo).strip():
                raise ReservaInvalidaError("El código de la reserva es obligatorio.")
            if not isinstance(cliente, Cliente):
                raise ReservaInvalidaError("Debe asociar un objeto Cliente válido.")
            if not isinstance(servicio, Servicio):
                raise ReservaInvalidaError("Debe asociar un objeto Servicio válido.")
            if not fecha or not str(fecha).strip():
                raise ReservaInvalidaError("La fecha de la reserva es obligatoria.")
        except ReservaInvalidaError as e:
            logger.error("Fallo al crear reserva (%s): %s", codigo, e)
            raise
        else:
            self.codigo = str(codigo).strip()
            self.cliente = cliente
            self.servicio = servicio
            self.fecha = str(fecha).strip()
            self.estado = "Pendiente"
            logger.info("Reserva creada: %s | Cliente: %s | Servicio: %s",
                        self.codigo, self.cliente.nombre, self.servicio.nombre)
        finally:
            logger.info("Proceso de inicialización finalizado para reserva: %s", codigo)

    def calcular_total(self, porcentaje_iva=0.19, descuento=0.0):
        """
        Sobrecarga simulada mediante parámetros opcionales:
        Permite calcular el total solo con IVA, con descuento, o neto (iva=0, descuento=0).
        """
        try:
            if porcentaje_iva < 0 or descuento < 0:
                raise ValueError("El IVA y el descuento no pueden ser negativos.")
            base = self.servicio.calcular_costo()
            if descuento > base:
                raise ValueError("El descuento excede el valor base del servicio.")
            total = (base - descuento) * (1 + porcentaje_iva)
            return round(total, 2)
        except Exception as e:
            logger.error("Error calculando total de reserva %s: %s", self.codigo, e)
            raise ReservaError(f"No se pudo calcular el costo de la reserva {self.codigo}") from e

    def confirmar(self):
        """Confirma una reserva pendiente usando try/except/else/finally."""
        try:
            if self.estado == "Cancelada":
                raise EstadoReservaError("No se puede confirmar una reserva que ya fue cancelada.")
            if self.estado == "Confirmada":
                raise EstadoReservaError("La reserva ya se encuentra confirmada.")
        except EstadoReservaError as e:
            logger.warning("Intento inválido al confirmar %s: %s", self.codigo, e)
            raise
        else:
            self.estado = "Confirmada"
            logger.info("Reserva %s CONFIRMADA exitosamente.", self.codigo)
        finally:
            logger.info("Revisión de estado completada para reserva %s (Estado actual: %s)",
                        self.codigo, self.estado)

    def cancelar(self, motivo="Solicitado por el usuario"):
        """Cancela una reserva activa."""
        try:
            if self.estado == "Cancelada":
                raise EstadoReservaError("La reserva ya estaba cancelada previamente.")
        except EstadoReservaError as e:
            logger.warning("Intento inválido al cancelar %s: %s", self.codigo, e)
            raise
        else:
            self.estado = "Cancelada"
            logger.info("Reserva %s CANCELADA. Motivo: %s", self.codigo, motivo)
        finally:
            logger.info("Cierre de operación de cancelación en reserva %s.", self.codigo)

    def __str__(self):
        return (f"[{self.codigo}] Cliente: {self.cliente.nombre} | "
                f"Servicio: {self.servicio.descripcion()} | "
                f"Fecha: {self.fecha} | Estado: {self.estado} | "
                f"Total (IVA 19%): ${self.calcular_total():,.2f}")
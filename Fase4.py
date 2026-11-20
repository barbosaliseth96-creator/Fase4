"""
Sistema Integral de Gestión de Clientes, Servicios y Reservas - Software FJ
Archivo principal de integración y simulación de 10 operaciones (Parte 5).
"""

import logging
from cliente import Cliente, ClienteError
from servicio import (
    ServicioError,
    ReservaSala,
    AlquilerEquipo,
    AsesoriaEspecializada,
)
from reserva import Reserva, ReservaError

logger = logging.getLogger("software_fj")


class SistemaSoftwareFJ:
    """Clase gestora que administra clientes, servicios y reservas."""

    def __init__(self):
        self.clientes = []
        self.servicios = []
        self.reservas = []

    def registrar_cliente(self, nombre, correo, identificacion=None):
        try:
            nuevo_cliente = Cliente(nombre, correo, identificacion)
        except ClienteError as e:
            print(f"  [ERROR CONTROLADO - Cliente]: {e}")
            return None
        else:
            self.clientes.append(nuevo_cliente)
            print(f"  [OK] Cliente registrado: {nuevo_cliente.nombre}")
            return nuevo_cliente

    def registrar_servicio(self, servicio):
        self.servicios.append(servicio)
        print(f"  [OK] Servicio agregado: {servicio.descripcion()}")
        return servicio

    def crear_reserva(self, codigo, cliente, servicio, fecha):
        try:
            nueva_reserva = Reserva(codigo, cliente, servicio, fecha)
        except ReservaError as e:
            print(f"  [ERROR CONTROLADO - Reserva]: {e}")
            return None
        else:
            self.reservas.append(nueva_reserva)
            print(f"  [OK] Reserva creada: {nueva_reserva}")
            return nueva_reserva


def ejecutar_simulacion():
    print("=" * 75)
    print("INICIANDO SIMULACIÓN DE 10 OPERACIONES - SOFTWARE FJ")
    print("=" * 75)
    sistema = SistemaSoftwareFJ()

    # OPERACIÓN 1: Registro exitoso de cliente válido
    print("\n1. Registrando cliente válido...")
    c1 = sistema.registrar_cliente("Laura Gómez", "laura.gomez@unad.edu.co", "1085234567")

    # OPERACIÓN 2: Intento de registro de cliente con correo inválido (Excepción controlada)
    print("\n2. Intentando registrar cliente con correo inválido...")
    sistema.registrar_cliente("Carlos Pérez", "correo-sin-arroba", "1085999888")

    # OPERACIÓN 3: Intento de registro de cliente con nombre vacío (Excepción controlada)
    print("\n3. Intentando registrar cliente sin nombre...")
    sistema.registrar_cliente("   ", "sin.nombre@correo.com", "1085111222")

    # OPERACIÓN 4: Creación exitosa de tres servicios especializados (Polimorfismo)
    print("\n4. Creando catálogo de 3 servicios especializados...")
    s1 = sistema.registrar_servicio(ReservaSala(horas=3, precio=50000))
    s2 = sistema.registrar_servicio(AlquilerEquipo(cantidad=4, precio=25000))
    s3 = sistema.registrar_servicio(AsesoriaEspecializada(sesiones=2, especialidad="Arquitectura Python", precio=70000))

    # OPERACIÓN 5: Intento de crear servicio con parámetro inválido (Excepción controlada)
    print("\n5. Intentando crear servicio con sesiones negativas...")
    try:
        AsesoriaEspecializada(sesiones=-2, especialidad="Redes")
    except ServicioError as e:
        print(f"  [ERROR CONTROLADO - Servicio]: {e}")

    # OPERACIÓN 6: Creación y confirmación exitosa de reserva #1
    print("\n6. Creando y confirmando Reserva RES-001...")
    r1 = sistema.crear_reserva("RES-001", c1, s1, "2026-11-25")
    if r1:
        r1.confirmar()
        print(f"     Total neto sin IVA: ${r1.calcular_total(porcentaje_iva=0):,.2f}")
        print(f"     Total con IVA 19% y descuento $10.000: ${r1.calcular_total(0.19, 10000):,.2f}")

    # OPERACIÓN 7: Creación y cancelación de reserva #2
    print("\n7. Creando y cancelando Reserva RES-002...")
    r2 = sistema.crear_reserva("RES-002", c1, s3, "2026-11-28")
    if r2:
        r2.cancelar("Cambio de horario del cliente")

    # OPERACIÓN 8: Intento de confirmar una reserva ya cancelada (Excepción controlada)
    print("\n8. Intentando confirmar RES-002 que ya fue cancelada...")
    if r2:
        try:
            r2.confirmar()
        except ReservaError as e:
            print(f"  [ERROR CONTROLADO - Estado]: {e}")

    # OPERACIÓN 9: Intento de crear reserva con cliente inexistente/inválido (Excepción controlada)
    print("\n9. Intentando crear reserva sin un objeto Cliente válido...")
    sistema.crear_reserva("RES-003", "ClienteFalso", s2, "2026-12-01")

    # OPERACIÓN 10: Intento de calcular costo con descuento mayor al valor base (Encadenamiento de excepción)
    print("\n10. Probando encadenamiento de excepciones en cálculo de costos...")
    if r1:
        try:
            r1.calcular_total(porcentaje_iva=0.19, descuento=9999999)
        except ReservaError as e:
            print(f"  [ERROR ENCADENADO CAPTURADO]: {e} | Causa original: {e.__cause__}")

    print("\n" + "=" * 75)
    print(f"RESUMEN FINAL: {len(sistema.clientes)} cliente(s) | "
          f"{len(sistema.servicios)} servicio(s) | {len(sistema.reservas)} reserva(s)")
    print("Todos los eventos y errores quedaron registrados en 'logs.txt'.")
    print("=" * 75)


if __name__ == "__main__":
    ejecutar_simulacion()
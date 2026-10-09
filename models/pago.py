from enum import Enum
import datetime
class MetodosPago(Enum):
    EFECTIVO = "Efectivo"
    TARJETA_CREDITO = "Tarjeta de Crédito"
    TARJETA_DEBITO = "Tarjeta de Débito"
    TRANSFERENCIA_BANCARIA = "Transferencia Bancaria"
    PAYPAL = "PayPal"
    CRIPTOMONEDA = "Criptomoneda"

class Pago:
    def __init__(self, id_pago: int, fecha_pago: datetime.datetime, monto: float, metodo_pago: MetodosPago):
        self._id_pago = id_pago
        self._fecha_pago = fecha_pago
        self._monto = monto
        self._metodo_pago = metodo_pago

    @property
    def id_pago(self) -> int:
        return self._id_pago

    @property
    def fecha_pago(self) -> datetime.datetime:
        return self._fecha_pago

    @property
    def monto(self) -> float:
        return self._monto

    @monto.setter
    def monto(self, nuevo_monto: float):
        self._monto = nuevo_monto

    @property
    def metodo_pago(self) -> MetodosPago:
        return self._metodo_pago

    def pagar(self, monto: float):
        if monto <= 0:
            raise ValueError("El monto a pagar debe ser mayor que cero.")
        self.monto = monto

    def __str__(self):
        return f"Pago(id_pago={self.id_pago}, fecha_pago={self.fecha_pago}, monto={self.monto}, metodo_pago='{self.metodo_pago}')"
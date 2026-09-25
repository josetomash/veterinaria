from enum import Enum
class MetodosPago(Enum):
    EFECTIVO = "Efectivo"
    TARJETA_CREDITO = "Tarjeta de Crédito"
    TARJETA_DEBITO = "Tarjeta de Débito"
    TRANSFERENCIA_BANCARIA = "Transferencia Bancaria"
    PAYPAL = "PayPal"
    CRIPTOMONEDA = "Criptomoneda"

class Pago:
    def __init__(self, id_pago: int, fecha_pago: date, monto: float, metodo_pago: MetodosPago):
        self.id_pago = id_pago
        self.fecha_pago = fecha_pago
        self.monto = monto
        self.metodo_pago = metodo_pago


    def pagar(self, monto: float):
        if monto <= 0:
            raise ValueError("El monto a pagar debe ser mayor que cero.")
        self.monto = monto

    def __str__(self):
        return f"Pago(id_pago={self.id_pago}, fecha_pago={self.fecha_pago}, monto={self.monto}, metodo_pago='{self.metodo_pago}')"
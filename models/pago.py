from enum import Enum

class MetodosPago(Enum):
    EFECTIVO = "Efectivo"
    TARJETA_CREDITO = "Tarjeta de Crédito"
    TARJETA_DEBITO = "Tarjeta de Débito"
    TRANSFERENCIA_BANCARIA = "Transferencia Bancaria"
    PAYPAL = "PayPal"
    CRIPTOMONEDA = "Criptomoneda"
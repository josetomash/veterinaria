#Funciona igual que un exception pero con otros nombres para saber donde esta el error o cual es

class VetCareException(Exception):
    """Errores propios del sistema"""
    pass


class RutInvalidoException(VetCareException):
    """Cuando el rut no es valido"""
    pass


class TelefonoInvalidoException(VetCareException):
    """Cuando el telefono no es valido"""
    pass
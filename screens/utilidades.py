"""Funciones de apoyo para los menús (pantalla y captura de datos)."""
from datetime import date
import math
import os

MAXIMO_INTENTOS = 3
# Rango de los enteros que SQLite puede guardar (64 bits)
MAXIMO_ENTERO_SQLITE = 2**63 - 1


class DemasiadosIntentos(ValueError):
    """Se lanza cuando el usuario se equivoca 3 veces en un mismo dato.
    Hereda de ValueError para que los menús la capturen igual que los demás errores
    y vuelvan a su menú."""


def limpiar_pantalla() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def pausar() -> None:
    input("Presione Enter para continuar...")


def pedir_dato(mensaje: str, convertir=lambda texto: texto.strip()):
    """Pide un dato y lo repite solo a él si es inválido.
    `convertir` recibe el texto escrito y devuelve el valor listo para usar,
    o lanza ValueError/TypeError con el motivo del error.
    Si el usuario se equivoca 3 veces se lanza DemasiadosIntentos."""
    for intento in range(1, MAXIMO_INTENTOS + 1):
        texto = input(mensaje)
        try:
            return convertir(texto)
        except (ValueError, TypeError) as error:
            restantes = MAXIMO_INTENTOS - intento
            if restantes > 0:
                print(f"  [Dato inválido] {error} (le quedan {restantes} intento(s))")
            else:
                print(f"  [Dato inválido] {error}")
    raise DemasiadosIntentos(
        f"Se equivocó {MAXIMO_INTENTOS} veces en el mismo dato. Volviendo al menú."
    )


class _Borrador:
    """Objeto vacío donde se prueba el setter de un modelo sin crear el objeto completo."""


def validar(clase, atributo: str, valor):
    """Ejecuta el setter `atributo` de `clase` sobre un borrador.
    Así cada dato se valida con las mismas reglas del modelo apenas se escribe."""
    getattr(clase, atributo).fset(_Borrador(), valor)
    return valor


def convertir_entero(texto: str) -> int:
    try:
        numero = int(texto.strip())
    except ValueError:
        raise ValueError("Debe ingresar un número entero.") from None
    if abs(numero) > MAXIMO_ENTERO_SQLITE:
        raise ValueError("El número es demasiado grande.")
    return numero


def convertir_decimal(texto: str) -> float:
    try:
        numero = float(texto.strip().replace(",", "."))
    except ValueError:
        raise ValueError("Debe ingresar un número.") from None
    if not math.isfinite(numero):  # rechaza "nan" e "inf"
        raise ValueError("Debe ingresar un número.")
    return numero


def convertir_fecha(texto: str) -> date:
    try:
        return date.fromisoformat(texto.strip())
    except ValueError:
        raise ValueError("La fecha debe tener el formato AAAA-MM-DD.") from None


def convertir_si_no(texto: str) -> bool:
    respuesta = texto.strip().upper()
    if respuesta not in ("S", "N"):
        raise ValueError("Responda S o N.")
    return respuesta == "S"


def elegir_de_lista(mensaje: str, opciones: list, nombre: str):
    """Pide el número de una opción de la lista (empezando en 1) y devuelve el elemento."""
    def convertir(texto):
        indice = convertir_entero(texto)
        if indice < 1 or indice > len(opciones):
            raise ValueError(f"La {nombre} seleccionada no existe.")
        return opciones[indice - 1]
    return pedir_dato(mensaje, convertir)

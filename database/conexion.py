#veterinaria/database/conexion.py
import sqlite3


class Conexion:
    def __init__(self):
        pass
    @staticmethod
    def inicializar_conexion():
        conexion = sqlite3.connect('demo.db')

import sqlite3
from contextlib import contextmanager


class ConexionDB:
    def __init__(self, ruta_db: str = "database/clinica_vetcare.db"):
        self._ruta_db = ruta_db

    @contextmanager
    def obtener_conexion(self):
        conn = sqlite3.connect(self._ruta_db)
        try:
            conn.execute("PRAGMA foreign_keys = ON")
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

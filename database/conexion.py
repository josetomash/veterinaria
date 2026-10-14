import os
import sqlite3
from contextlib import contextmanager


class ConexionDB:
    def __init__(self, ruta_db: str | None = None):
        self._ruta_db = (
            ruta_db
            if ruta_db is not None
            else os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "clinica_vetcare.db",
            )
        )

    @property
    def ruta_db(self) -> str:
        return self._ruta_db

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

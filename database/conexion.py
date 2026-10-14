import os
import re
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

    def migrar_tabla_sin_autoincrement(
        self, conn: sqlite3.Connection, nombre_tabla: str
    ) -> None:
        if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", nombre_tabla):
            raise ValueError(f"Nombre de tabla no válido: {nombre_tabla!r}")

        fila = conn.execute(
            "SELECT sql FROM sqlite_master WHERE type = 'table' AND name = ?",
            (nombre_tabla,),
        ).fetchone()
        if fila is None or "AUTOINCREMENT" not in fila[0].upper():
            return

        tabla_temporal = f"{nombre_tabla}_sin_autoincrement"
        existe_temporal = conn.execute(
            "SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = ?",
            (tabla_temporal,),
        ).fetchone()
        if existe_temporal is not None:
            raise RuntimeError(
                f"No se puede migrar {nombre_tabla}: "
                f"ya existe la tabla temporal {tabla_temporal}."
            )

        ddl = re.sub(r"\bAUTOINCREMENT\b", "", fila[0], flags=re.IGNORECASE)
        patron_tabla = re.compile(
            rf"^(\s*CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?)[`\"\[]?"
            rf"{re.escape(nombre_tabla)}[`\"\]]?",
            flags=re.IGNORECASE,
        )
        ddl_temporal, reemplazos = patron_tabla.subn(
            rf"\g<1>{tabla_temporal}", ddl, count=1
        )
        if reemplazos != 1:
            raise RuntimeError(
                f"No se pudo preparar la migración de la tabla {nombre_tabla}."
            )

        foreign_keys_activas = conn.execute("PRAGMA foreign_keys").fetchone()[0]
        if foreign_keys_activas:
            conn.execute("PRAGMA foreign_keys = OFF")
        try:
            conn.execute("BEGIN IMMEDIATE")
            conn.execute(ddl_temporal)
            conn.execute(
                f'INSERT INTO "{tabla_temporal}" SELECT * FROM "{nombre_tabla}"'
            )
            conn.execute(f'DROP TABLE "{nombre_tabla}"')
            conn.execute(
                f'ALTER TABLE "{tabla_temporal}" RENAME TO "{nombre_tabla}"'
            )
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            if foreign_keys_activas:
                conn.execute("PRAGMA foreign_keys = ON")

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

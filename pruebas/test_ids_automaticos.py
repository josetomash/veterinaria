import os
import sqlite3
import tempfile
import unittest
from contextlib import closing

from dao import (
    ConsultaDAO,
    DetalleConsultaDAO,
    EspecialidadDAO,
    EspecieDAO,
    MascotaDAO,
    MedicamentoDAO,
    PropietarioDAO,
    RecetaMedicaDAO,
    VeterinarioDAO,
)
from database import ConexionDB
from models.medicamento import Medicamento


class TestIdsAutomaticos(unittest.TestCase):
    def setUp(self):
        self.directorio_temporal = tempfile.TemporaryDirectory()
        self.ruta_db = os.path.join(self.directorio_temporal.name, "prueba.db")
        self.conexion_db = ConexionDB(self.ruta_db)

    def tearDown(self):
        self.directorio_temporal.cleanup()

    def test_ruta_predeterminada_no_depende_del_directorio_de_ejecucion(self):
        directorio_actual = os.getcwd()
        try:
            os.chdir(self.directorio_temporal.name)
            conexion = ConexionDB()
            ruta_esperada = (
                os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                + os.sep
                + "database"
                + os.sep
                + "clinica_vetcare.db"
            )
            self.assertEqual(conexion.ruta_db, ruta_esperada)
        finally:
            os.chdir(directorio_actual)

    def test_todos_los_daos_crean_esquemas_sin_autoincrement(self):
        daos = (
            EspecieDAO,
            EspecialidadDAO,
            PropietarioDAO,
            MascotaDAO,
            VeterinarioDAO,
            ConsultaDAO,
            RecetaMedicaDAO,
            DetalleConsultaDAO,
            MedicamentoDAO,
        )
        for dao in daos:
            dao(self.conexion_db)

        with closing(sqlite3.connect(self.ruta_db)) as conn:
            esquemas = conn.execute(
                """
                SELECT name, sql FROM sqlite_master
                WHERE type = 'table' AND name NOT LIKE 'sqlite_%'
                """
            ).fetchall()
        esquemas_con_autoincrement = [
            nombre for nombre, ddl in esquemas if "AUTOINCREMENT" in ddl.upper()
        ]
        self.assertEqual(esquemas_con_autoincrement, [])

    def test_migra_secuencia_antigua_y_asigna_id_desde_uno(self):
        with closing(sqlite3.connect(self.ruta_db)) as conn:
            with conn:
                conn.execute(
                    """
                    CREATE TABLE medicamentos (
                        id_medicamento INTEGER PRIMARY KEY AUTOINCREMENT,
                        nombre_comercial TEXT NOT NULL UNIQUE,
                        nombre_generico TEXT NOT NULL,
                        tipo TEXT NOT NULL,
                        precio REAL NOT NULL CHECK(precio > 0),
                        stock INTEGER NOT NULL CHECK(stock >= 0)
                    )
                    """
                )
                conn.execute(
                    """
                    INSERT INTO medicamentos
                    VALUES (73, 'Prueba', 'Genérico', 'Prueba', 100, 5)
                    """
                )
                conn.execute("DELETE FROM medicamentos")

        dao = MedicamentoDAO(self.conexion_db)

        with closing(sqlite3.connect(self.ruta_db)) as conn:
            ddl = conn.execute(
                "SELECT sql FROM sqlite_master WHERE name = 'medicamentos'"
            ).fetchone()[0]
            secuencia = conn.execute(
                "SELECT seq FROM sqlite_sequence WHERE name = 'medicamentos'"
            ).fetchone()
        self.assertNotIn("AUTOINCREMENT", ddl.upper())
        self.assertIsNone(secuencia)

        primer_medicamento = Medicamento(None, "Primero", "Genérico", "Prueba", 100, 1)
        dao.insertar(primer_medicamento)
        self.assertEqual(primer_medicamento.id_medicamento, 1)

        segundo_medicamento = Medicamento(None, "Segundo", "Genérico", "Prueba", 100, 1)
        dao.insertar(segundo_medicamento)
        self.assertEqual(segundo_medicamento.id_medicamento, 2)

    def test_migracion_preserva_ids_referenciados_por_claves_foraneas(self):
        with closing(sqlite3.connect(self.ruta_db)) as conn:
            with conn:
                conn.execute("PRAGMA foreign_keys = ON")
                conn.execute(
                    """
                    CREATE TABLE propietarios (
                        id_propietario INTEGER PRIMARY KEY AUTOINCREMENT,
                        nombre TEXT NOT NULL,
                        rut TEXT NOT NULL UNIQUE,
                        telefono TEXT NOT NULL,
                        email TEXT NOT NULL
                    )
                    """
                )
                conn.execute(
                    """
                    CREATE TABLE mascotas (
                        id_mascota INTEGER PRIMARY KEY,
                        id_propietario INTEGER NOT NULL,
                        FOREIGN KEY (id_propietario)
                            REFERENCES propietarios(id_propietario)
                    )
                    """
                )
                conn.execute(
                    """
                    INSERT INTO propietarios
                    VALUES (41, 'Ana', '123', '555', 'ana@example.com')
                    """
                )
                conn.execute("INSERT INTO mascotas VALUES (9, 41)")

        PropietarioDAO(self.conexion_db)

        with closing(sqlite3.connect(self.ruta_db)) as conn:
            propietario = conn.execute(
                "SELECT id_propietario, nombre FROM propietarios"
            ).fetchone()
            mascota = conn.execute(
                "SELECT id_mascota, id_propietario FROM mascotas"
            ).fetchone()
            errores_fk = conn.execute("PRAGMA foreign_key_check").fetchall()
            ddl = conn.execute(
                "SELECT sql FROM sqlite_master WHERE name = 'propietarios'"
            ).fetchone()[0]
        self.assertEqual(propietario, (41, "Ana"))
        self.assertEqual(mascota, (9, 41))
        self.assertEqual(errores_fk, [])
        self.assertNotIn("AUTOINCREMENT", ddl.upper())


if __name__ == "__main__":
    unittest.main()

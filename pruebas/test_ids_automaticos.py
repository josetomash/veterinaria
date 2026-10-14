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

    def test_daos_usan_autoincrement_en_tablas_con_id_generado(self):
        daos = (
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
        esperadas = {
            "propietarios",
            "mascotas",
            "veterinarios",
            "consulta",
            "detalle_consulta",
            "receta_medica",
            "medicamentos",
        }
        esquemas_con_autoincrement = {
            nombre for nombre, ddl in esquemas if "AUTOINCREMENT" in ddl.upper()
        }
        self.assertEqual(esquemas_con_autoincrement, esperadas)

    def test_id_empieza_en_uno_en_db_nueva_y_no_se_reutiliza(self):
        dao = MedicamentoDAO(self.conexion_db)
        primero = Medicamento(None, "Primero", "Genérico", "Prueba", 100, 1)
        dao.insertar(primero)
        self.assertEqual(primero.id_medicamento, 1)

        dao.eliminar(primero.id_medicamento)

        segundo = Medicamento(None, "Segundo", "Genérico", "Prueba", 100, 1)
        dao.insertar(segundo)
        self.assertEqual(segundo.id_medicamento, 2)

if __name__ == "__main__":
    unittest.main()

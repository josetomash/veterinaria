import os
from config.configuracion import Configuracion

def certificar_gestion_de_secretos():
    print("=" * 65)
    print("SUITE DE VERIFICACIÓN DE SEGURIDAD — VARIABLES DE ENTORNO (.ENV)")
    print("=" * 65)

    # TEST 1: El archivo .env existe localmente
    print("\n[TEST 1] Verificando presencia de archivo .env en el disco local...")
    assert os.path.exists(".env"), "Error: El archivo .env no existe en la raíz del proyecto."
    print(" -> APROBADO: Archivo .env detectado.")

    # TEST 2: El archivo .gitignore contiene la regla para excluir .env
    print("\n[TEST 2] Verificando regla de exclusión en .gitignore...")
    assert os.path.exists(".gitignore"), "Error: El archivo .gitignore debe existir."
    with open(".gitignore", "r", encoding="utf-8") as f:
        contenido_gitignore = f.read()
    assert ".env" in contenido_gitignore, "Error: '.env' DEBE estar incluido en .gitignore."
    print(" -> APROBADO: .gitignore protege el archivo .env de subidas accidentales.")

    # TEST 3: Carga correcta de variables en la clase Configuracion
    print("\n[TEST 3] Verificando lectura de secretos en memoria...")
    assert len(Configuracion.API_KEY_CLIMA) > 0, "Error: WEATHER_API_KEY no fue cargada."
    assert Configuracion.TIMEOUT == 5, f"Error: TIMEOUT esperado 5, recibido {Configuracion.TIMEOUT}."
    print(f" -> APROBADO: Clave cargada en memoria exitosamente (Longitud: {len(Configuracion.API_KEY_CLIMA)} caracteres).")

    print("\n" + "=" * 65)
    print("GESTIÓN DE SECRETOS Y CONFIGURACIÓN CERTIFICADA CON ÉXITO")
    print("=" * 65)

if __name__ == "__main__":
    certificar_gestion_de_secretos()

import sqlite3

#Conexion con el archivo fisico
conexion = sqlite3.connect('veterinaria.db')

#Crear un cursor (el puntero de ejecucion de sentencias)
cursor = conexion.cursor()

# DDL (Data Definition Language) de la tabla MEDICAMENTO

cursor.execute("""
CREATE TABLE IF NOT EXISTS persona (
    id_persona INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    telefono TEXT NOT NULL,
    stock INTEGER NOT NULL,
    CHECK (precio > 0),
    CHECK (stock >= 0
)
""")

conexion.commit()  # Guardar los cambios en la base de datos
conexion.close()  # Cerrar la conexión a la base de datos

print("[OK] Base de datos y tabla MEDICAMENTO creadas exitosamente.")




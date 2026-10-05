CANTIDAD_MINIMA_CARACTERES_INSTRUCCIONES = 10


class RecetaMedica:
    def __init__(self, id_receta: int, nombre_comercial: str, cantidad_mg: int, instrucciones: str):
        self.id_receta = id_receta
        self.nombre_comercial = nombre_comercial
        self.cantidad_mg = cantidad_mg      
        self.instrucciones = instrucciones  

    @property
    def id_receta(self) -> int:
        return self._id_receta

    @id_receta.setter
    def id_receta(self, nuevo_id: int):
        if not isinstance(nuevo_id, int) or isinstance(nuevo_id, bool):
            raise TypeError("El ID de la receta debe ser un número entero.")
        if nuevo_id <= 0:
            raise ValueError("El ID de la receta debe ser un número positivo mayor a 0.")
        self._id_receta = nuevo_id

    @property
    def nombre_comercial(self) -> str:
        return self._nombre_comercial

    @nombre_comercial.setter
    def nombre_comercial(self, nuevo_nombre: str):
        if not isinstance(nuevo_nombre, str):
            raise TypeError("El nombre comercial debe ser una cadena de texto.")
        if not nuevo_nombre.strip():
            raise ValueError("El nombre comercial no puede estar vacío.")
        self._nombre_comercial = nuevo_nombre.strip()

    @property
    def cantidad_mg(self) -> int:
        return self._cantidad_mg

    @cantidad_mg.setter
    def cantidad_mg(self, nueva_cantidad: int):
        if not isinstance(nueva_cantidad, int) or isinstance(nueva_cantidad, bool):
            raise TypeError("La cantidad en mg debe ser un número entero.")
        if nueva_cantidad < 0:
            raise ValueError("La cantidad en mg no puede ser negativa.")
        self._cantidad_mg = nueva_cantidad

    @property
    def instrucciones(self) -> str:
        return self._instrucciones

    @instrucciones.setter
    def instrucciones(self, nuevas_instrucciones: str):
        if not isinstance(nuevas_instrucciones, str):
            raise TypeError("Las instrucciones deben ser una cadena de texto.")
        
        texto_limpio = nuevas_instrucciones.strip()
        if len(texto_limpio) < CANTIDAD_MINIMA_CARACTERES_INSTRUCCIONES:
            raise ValueError(
                f"Las instrucciones deben tener un mínimo de "
                f"{CANTIDAD_MINIMA_CARACTERES_INSTRUCCIONES} caracteres. "
                f"Ingresados: {len(texto_limpio)}."
            )
        
        self._instrucciones = texto_limpio

    def __str__(self) -> str:
        return (
            f"Receta #{self.id_receta} - {self.nombre_comercial} ({self.cantidad_mg}mg)\n"
            f"Instrucciones: {self.instrucciones}"
        )


CANTIDAD_MINIMA_CARACTERES_INSTRUCCIONES = 10

class RecetaMedica:
    def __init__(self, id_receta: int, nombre_comercial: str, cantidad_mg: int, instrucciones: str):
        self.id_receta = id_receta
        self.nombre_comercial = nombre_comercial
        self.cantidad_mg = cantidad_mg      
        self.instrucciones = instrucciones  

    @property
    def instrucciones(self):
        return self._instrucciones

    @instrucciones.setter
    def instrucciones(self, nuevas_instrucciones: str):
        if not isinstance(nuevas_instrucciones, str):
            raise TypeError("Las instrucciones deben ser una cadena de texto.")
        
        texto_limpio = nuevas_instrucciones.strip()
        if len(texto_limpio) < CANTIDAD_MINIMA_CARACTERES_INSTRUCCIONES:
            raise ValueError(
                f"Las instrucciones deben tener un mínimo de "
                f"{CANTIDAD_MINIMA_CARACTERES_INSTRUCCIONES} caracteres."
            )
        
        self._instrucciones = texto_limpio

    @property
    def cantidad_mg(self):
        return self._cantidad_mg

    @cantidad_mg.setter
    def cantidad_mg(self, nueva_cantidad: int):
        if not isinstance(nueva_cantidad, int):
            raise TypeError("La cantidad debe ser un número entero.")
        
        if nueva_cantidad < 0:
            raise ValueError("La cantidad no puede ser negativa.")
        
        self._cantidad_mg = nueva_cantidad

recetita = RecetaMedica(1, "Paracetamol", 500, "Tomar cada 8 horas")
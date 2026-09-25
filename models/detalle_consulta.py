from receta_medica import RecetaMedica

class DetalleConsulta:
    def __init__(self, id_detalle: int, diagnostico: str, tratamiento: str, receta: RecetaMedica):
        """Constructor de la clase DetalleConsulta"""


        self._id_detalle = id_detalle
        self._diagnostico = diagnostico
        self._tratamiento = tratamiento
        self._receta = receta


    @property
    def actualizar_valores(self):
        """Propiedad para obtener los atributos de la clase DetalleConsulta"""

        return self.__dict__


    @actualizar_valores.setter
    def actualizar_valores(self, valores: tuple):
        """Setter para establecer los atributos de la clase DetalleConsulta"""
        
        atributos = list(self.__dict__.keys())          
        cantidad_esperada = len(atributos)             
        nombres = [attr.lstrip('_') for attr in atributos] 
        nombres_str = ', '.join(nombres)                
        
        if not isinstance(valores, tuple):
            raise TypeError("Los valores deben ser proporcionados en una tupla.")
        elif len(valores) != cantidad_esperada:
            raise ValueError(f"Se deben proporcionar exactamente {cantidad_esperada} valores: {nombres_str}.")
        elif not isinstance(valores[3], RecetaMedica):
            raise TypeError("El cuarto valor debe ser una instancia de RecetaMedica.")
        elif not all(isinstance(valores[i], str) for i in range(1, 3)):
            raise TypeError("Los valores de diagnóstico y tratamiento deben ser cadenas de texto.")
        self._id_detalle, self._diagnostico, self._tratamiento, self._receta = valores

    def __str__(self):
        """Dunder method para mostrar la clase instanciada con atributos"""


        return (
            f"ID Detalle: {self._id_detalle}\n"
            f"Diagnóstico: {self._diagnostico}\n"
            f"Tratamiento: {self._tratamiento}\n"
            f"Receta:\n"
            f"  - ID: {self._receta.id_receta}\n"
            f"  - Nombre Comercial: {self._receta.nombre_comercial}\n"
            f"  - Cantidad: {self._receta.cantidad_mg}\n"
            f"  - Indicaciones: {self._receta.instrucciones}"
        )
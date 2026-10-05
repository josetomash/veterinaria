from .receta_medica import RecetaMedica


class DetalleConsulta:
    def __init__(
        self, 
        id_detalle: int, 
        diagnostico: str, 
        tratamiento: str, 
        receta: RecetaMedica
    ):
        """Constructor de la clase DetalleConsulta.
        Delegamos en los setters asignando directamente a self.atributo.
        """
        self.id_detalle = id_detalle
        self.diagnostico = diagnostico
        self.tratamiento = tratamiento
        self.receta = receta

    @property
    def id_detalle(self) -> int:
        return self._id_detalle

    @id_detalle.setter
    def id_detalle(self, nuevo_id: int):
        if not isinstance(nuevo_id, int) or isinstance(nuevo_id, bool):
            raise TypeError("El ID del detalle debe ser un número entero.")
        if nuevo_id <= 0:
            raise ValueError("El ID del detalle debe ser un número entero positivo.")
        self._id_detalle = nuevo_id

    @property
    def diagnostico(self) -> str:
        return self._diagnostico

    @diagnostico.setter
    def diagnostico(self, nuevo_diagnostico: str):
        if not isinstance(nuevo_diagnostico, str):
            raise TypeError("El diagnóstico debe ser una cadena de texto.")
        if not nuevo_diagnostico.strip():
            raise ValueError("El diagnóstico no puede estar vacío.")
        self._diagnostico = nuevo_diagnostico.strip()

    @property
    def tratamiento(self) -> str:
        return self._tratamiento

    @tratamiento.setter
    def tratamiento(self, nuevo_tratamiento: str):
        if not isinstance(nuevo_tratamiento, str):
            raise TypeError("El tratamiento debe ser una cadena de texto.")
        if not nuevo_tratamiento.strip():
            raise ValueError("El tratamiento no puede estar vacío.")
        self._tratamiento = nuevo_tratamiento.strip()

    @property
    def receta(self) -> RecetaMedica:
        return self._receta

    @receta.setter
    def receta(self, nueva_receta: RecetaMedica):
        if not isinstance(nueva_receta, RecetaMedica):
            raise TypeError("La receta debe ser una instancia válida de la clase RecetaMedica.")
        self._receta = nueva_receta

    def __str__(self) -> str:
        """Representación amigable para consola."""
        return (
            f"ID Detalle: {self.id_detalle}\n"
            f"Diagnóstico: {self.diagnostico}\n"
            f"Tratamiento: {self.tratamiento}\n"
            f"Receta:\n"
            f"  - ID: {self.receta.id_receta}\n"
            f"  - Nombre Comercial: {self.receta.nombre_comercial}\n"
            f"  - Cantidad: {self.receta.cantidad_mg} mg\n"
            f"  - Indicaciones: {self.receta.instrucciones}"
        )

    def __repr__(self) -> str:
        """Representación técnica para depuración."""
        return (
            f"DetalleConsulta(id={self.id_detalle}, "
            f"diagnostico='{self.diagnostico}', "
            f"tratamiento='{self.tratamiento}', "
            f"receta_id={self.receta.id_receta})"
        )


if __name__ == "__main__":
    receta = RecetaMedica(1, 'Amoxicilina', 500, 'Tomar cada 12 horas por 7 días')
    mi_consulta = DetalleConsulta(1, 'Infección leve', 'Administrar antibiótico', receta)
    
    print(mi_consulta)
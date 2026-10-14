from .receta_medica import RecetaMedica
from .consulta import Consulta


class DetalleConsulta:
    def __init__(
        self, 
        id_detalle: int, 
        diagnostico: str, 
        tratamiento: str, 
        receta: RecetaMedica,
        consulta: Consulta | None = None,
    ):
        """Constructor de la clase DetalleConsulta.
        Delegamos en los setters asignando directamente a self.atributo.
        """
        self.id_detalle = id_detalle
        self.diagnostico = diagnostico
        self.tratamiento = tratamiento
        self.receta = receta
        self.consulta = consulta

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

    @property
    def consulta(self) -> Consulta | None:
        return self._consulta

    @consulta.setter
    def consulta(self, nueva_consulta: Consulta | None):
        if nueva_consulta is not None and not isinstance(nueva_consulta, Consulta):
            raise TypeError("La consulta debe ser una instancia válida de la clase Consulta.")
        self._consulta = nueva_consulta

if __name__ == "__main__":
    receta = RecetaMedica(1, 'Amoxicilina', 500, 'Tomar cada 12 horas por 7 días')
    mi_consulta = DetalleConsulta(1, 'Infección leve', 'Administrar antibiótico', receta)
    
    print(mi_consulta)
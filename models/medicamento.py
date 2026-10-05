class Medicamento:
    def __init__(self, id_medicamento: int, nombre_comercial: str, nombre_generico: str, tipo: str, precio: float, stock: int):
        self.id_medicamento = id_medicamento
        self.nombre_comercial = nombre_comercial
        self.nombre_generico = nombre_generico
        self.tipo = tipo
        self.precio = precio
        self.stock = stock

    @property
    def id_medicamento(self) -> int:
        return self._id_medicamento

    @id_medicamento.setter
    def id_medicamento(self, nuevo_id: int):
        if not isinstance(nuevo_id, int) or isinstance(nuevo_id, bool):
            raise TypeError("El ID del medicamento debe ser un número entero.")
        if nuevo_id <= 0:
            raise ValueError("El ID del medicamento debe ser un número positivo mayor a 0.")
        self._id_medicamento = nuevo_id

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
    def nombre_generico(self) -> str:
        return self._nombre_generico

    @nombre_generico.setter
    def nombre_generico(self, nuevo_nombre: str):
        if not isinstance(nuevo_nombre, str):
            raise TypeError("El nombre genérico debe ser una cadena de texto.")
        if not nuevo_nombre.strip():
            raise ValueError("El nombre genérico no puede estar vacío.")
        self._nombre_generico = nuevo_nombre.strip()

    @property
    def tipo(self) -> str:
        return self._tipo

    @tipo.setter
    def tipo(self, nuevo_tipo: str):
        if not isinstance(nuevo_tipo, str):
            raise TypeError("El tipo de medicamento debe ser una cadena de texto.")
        if not nuevo_tipo.strip():
            raise ValueError("El tipo de medicamento no puede estar vacío.")
        self._tipo = nuevo_tipo.strip()

    @property
    def precio(self) -> float:
        return self.__precio

    @precio.setter
    def precio(self, nuevo_precio: float):
        if not isinstance(nuevo_precio, (int, float)) or isinstance(nuevo_precio, bool):
            raise TypeError(f"El precio debe ser un número. Se recibió: {type(nuevo_precio).__name__}")
        if nuevo_precio <= 0:
            raise ValueError(f"Invariante rota: el precio debe ser mayor a 0. Valor recibido {nuevo_precio}")
        # Lo convertimos a float para respetar el type hint de la función
        self.__precio = float(nuevo_precio)

    @property
    def stock(self) -> int:
        return self.__stock

    @stock.setter
    def stock(self, nuevo_stock: int):
        if not isinstance(nuevo_stock, int) or isinstance(nuevo_stock, bool):
            raise TypeError(f"El stock debe ser entero. Se recibe: {type(nuevo_stock).__name__}")
        if nuevo_stock < 0:
            raise ValueError(f"Stock negativo no permitido en VetCare. Intento asignar: {nuevo_stock}")
        self.__stock = nuevo_stock

    def __str__(self) -> str:
        return (
            f"ID: {self.id_medicamento} | {self.nombre_comercial} ({self.nombre_generico})\n"
            f"Tipo: {self.tipo} | Precio: ${self.precio} | Stock: {self.stock}"
        )
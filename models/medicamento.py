class Medicamento:
    def __init__(self, id_medicamento: int, nombre_comercial: str, nombre_generico: str, tipo: str, precio: float, stock: int):
        
        #Atributos
        self.id_medicamento = id_medicamento
        self.nombre_comercial = nombre_comercial
        self.nombre_generico = nombre_generico
        self.tipo = tipo

        #Atributos privados
        self.__precio = 0
        self.__stock = 0

        self.precio = precio
        self.stock = stock

    #Filtro de precio
    @property
    def precio(self)-> float:
        return self.__precio

    @precio.setter
    def precio(self, nuevo_precio:float):
        if not isinstance(nuevo_precio, (int, float)):
            raise TypeError(f"El precio debe ser un numero. se recidio: {type(nuevo_precio. __name__)}")
        if nuevo_precio <= 0:
            raise ValueError(f"invariante rota: el precio debe ser mayor a 0. valor recibido {nuevo_precio}")
        self.__precio = int(nuevo_precio)

    #Filtro de stock
    @property
    def stock(self)-> int:
        return self.__stock

    @stock.setter
    def stock(self, nuevo_stock: int):
        if not isinstance(nuevo_stock, int):
            raise TypeError(f"El stock debe ser entero. se recibe: {type(nuevo_stock). __name__}")
        if nuevo_stock < 0:
            raise ValueError (f"Stock negativo no permitido en VetCare. intento asignar: {nuevo_stock}")
        self.__stock = nuevo_stock 

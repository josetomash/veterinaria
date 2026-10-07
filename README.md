# Veterinaria VetCare

# models

Refactorización de consulta y detalle_consulta : 

Un setter monolitico que actualiza todos los valores de golpe es mala practica.
Se dividio en varios setters por cada atributo de clase 
Para automatizar este proceso se utilizo un agente IA.

El agente realizo: Analizo el codigo, separo el setter monolitico en varios setters para cada atributo.
Agente: Gemini 3.6 Flash

## Servicios

Debido a que ```clinica_service.py``` tenia los services de cada atributo en un mismo archivo,
el codigo empezo a volverse ilegible. Dado que el profesor argumento que hagamos
un service por cada clase, se opto por utilizar un agente para refactorizar el codigo.
Esta decision fue debido a la madurez del codigo que ya tenia conectado gran parte del programa

El agente realizo: Analizo el codigo, lo separo en responsabilidades, conservo compatiblidad
Agente: GPT-6 Luna | Copilot

## Base de datos

Se realizo la conexion de la base de datos mediante main.py el cual incializa la conexion
conexion.py se encarga de repetir el codigo que estaba en los DAO asi no va creando
varias conexiones, crea solo una y centraliza CRUD. Se uso "?" para tratar los datos del usuario
meramente como texto y asi evitar f-strings para evitar inyecciones SQL

¿Que hizo la IA?:

`main.py` crea una instancia compartida de `Conexion` y la inyecta en los DAO.
La clase centraliza la ejecución de consultas, el commit y el rollback de SQLite.

Agente: GPT-6 Luna | Copilot

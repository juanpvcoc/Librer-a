# @autor: Juan Velásquez
# @fecha: 2023/11/17
# @descripción: Conexión a la Base de Datos

# Módulo de mysql
from mysql import connector

libreria = connector.connect(
    host = "localhost",
    user = "root",
    password = "",
    database = "libreriajpva2614986"
)
from datetime import datetime
import requests
import mysql.connector
import unicodedata
from bs4 import BeautifulSoup




mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "oycobe",
    database = 'humai'
)

def get_last_id():
    '''Consigo el ultimo id de la base para insertarlo al nuevo producto'''
    mycursor = mydb.cursor()
    sql = "Select MAX(IdProducto) from productos"
    mycursor.execute(sql)
    result = mycursor.fetchall()
    for id in result:
        id = id[0]
    return id


def insertar_azucar(nombreProducto: str, precio: float, link: str, provincia: str):
    '''Se inserta en la base de datos la azucar scrapeada'''
    mycursor = mydb.cursor()
    id = get_last_id() + 1

    IdMarca = get_marca_azucar(nombreProducto)
    IdTipoAzucar = get_tipo_azucar(nombreProducto)
    IdProvincia = get_provincia(provincia)

    sql = "Insert into productos (IdProducto, Nombre, IdTipoAzucar, IdMarca, Precio, Link, FechaBajada, IdProvincia) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    values = (id, nombreProducto, IdTipoAzucar, IdMarca, precio, link, datetime.now(), IdProvincia)
    mycursor.execute(sql,values)
    mydb.commit()
    #mycursor.close()
    #mydb.close()


def normalize_accent(word: str) -> str:
    '''Normalizacion de campos como acentos o mayusculas y minusculas, utilizado comunmente para comparar cadenas de texto'''
    return ''.join(c for c in unicodedata.normalize('NFD', word)
                  if unicodedata.category(c) != 'Mn').lower()


def get_page(url: str, page_headers: dict):
    '''Devuelve una pagina formateada con beatiful soup'''
    response = requests.request("GET",url, headers=page_headers)
    page = BeautifulSoup(response.content, 'html.parser')
    return page 


def get_tipo_azucar(nombre: str) -> int:
    '''Consigue el tipo de azucar en base a cuantos matcheos tiene el nombre del producto.
    Cuando la cantidad de matches de la base es igual a la del nombre del producto entonces recien ahi se le asigna el id correspondiente.
    En caso de no encontrar se pone -1 y luego con la limpieza de datos se asigna'''
    id = -1
    mycursor = mydb.cursor()
    sql = "Select IdTipoAzucar, nombre from TiposAzucar"
    mycursor.execute(sql)
    result = mycursor.fetchall()

    nombre_normalized = normalize_accent(nombre)
    for azucar in result:
        azucar_normalized = normalize_accent(azucar[1]).split()
        total_matches = 0
        for an in azucar_normalized:
            if nombre_normalized.find(an) != -1:
                total_matches += 1
        if total_matches == len(azucar_normalized):
            id = int(azucar[0])

    return id

def get_marca_azucar(nombre: str) -> int:
    '''Consigue la marca en base a cuantos matcheos tiene el nombre del producto.
    Cuando la cantidad de matches de la base es igual a la del nombre del producto entonces recien ahi se le asigna el id correspondiente.
    En caso de no encontrar se pone -1 y luego con la limpieza de datos se asigna'''
    id = -1
    mycursor = mydb.cursor()
    sql = "Select IdMarca, Nombre from Marcas"
    mycursor.execute(sql)
    result = mycursor.fetchall()

    nombre_normalized = normalize_accent(nombre)
    for marca in result:
        marca_normalized = normalize_accent(marca[1]).split()
        total_matches = 0
        for m in marca_normalized:
            if nombre_normalized.find(m) != -1:
                total_matches += 1
        if total_matches == len(marca_normalized):
            id = int(marca[0])

    return id

def get_provincia(nombre: str) -> int:
    '''Consigue la provincia en base al nombre de provincia '''
    id = -1
    if  nombre == "":
        return id 
    else:
        mycursor = mydb.cursor()
        sql = f"Select IdProvincia from Provincias where Nombre like '{nombre}'"
        mycursor.execute(sql)
        result = mycursor.fetchall()
        for idprovincia in result:
            id = (idprovincia[0])
    return id

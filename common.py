from datetime import datetime
import unicodedata
from bs4 import BeautifulSoup
from google.cloud import bigquery
from google.oauth2 import service_account
import requests
import os
import unidecode

HERE = os.path.dirname(os.path.abspath(__file__))
KEY_PATH = os.path.join(HERE, 'key.json')
PROJECT_AND_DATASET = "alumnos-sandbox.precios_productos"

credentials = service_account.Credentials.from_service_account_file(KEY_PATH)
client = bigquery.Client(credentials=credentials, project=credentials.project_id)

def get_last_id() -> int:
    '''Consigo el ultimo id de la base para insertarlo al nuevo producto'''

    sql_query = f"SELECT MAX(IdProducto) FROM `{PROJECT_AND_DATASET}.precios_azucar`"
    query = client.query(sql_query)
    result = query.result()

    azucar_id = 0

    for row in result:
        azucar_id = row[0]
        break

    return azucar_id


def insertar_azucar(nombre_producto: str, precio: float, link: str, provincia: str) -> None:
    '''Se inserta en la base de datos la azucar scrapeada'''

    azucar_id = get_last_id() + 1

    id_marca = get_marca_azucar(nombre_producto)
    id_tipo_azucar = get_tipo_azucar(nombre_producto)
    id_azucar = get_provincia(provincia)

    nombre = unidecode.unidecode(nombre_producto)

    sql_query = f"""INSERT INTO `{PROJECT_AND_DATASET}.precios_azucar` (IdProducto, Nombre, IdTipoAzucar, IdMarca, Precio, Link, FechaBajada, IdProvincia)
    VALUES ({ azucar_id }, "{ nombre }", { id_tipo_azucar }, { id_marca }, { precio }, "{ link }", { datetime.now() }, { id_azucar })"""

    query = client.query(sql_query)
    query.result()


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
    Cuando la cantidad de matches de la base es igual a la del nombre del producto entonces
    recien ahi se le asigna el id correspondiente.
    En caso de no encontrar se pone -1 y luego con la limpieza de datos se asigna'''
    tipo_azucar_id = -1

    sql_query = f"SELECT IdTipoAzucar, Nombre FROM `{PROJECT_AND_DATASET}.tipos_azucar`"

    query = client.query(sql_query)
    result = query.result()

    nombre_normalized = normalize_accent(nombre)
    for azucar in result:
        azucar_normalized = normalize_accent(azucar[1]).split()
        total_matches = 0
        for an in azucar_normalized:
            if nombre_normalized.find(an) != -1:
                total_matches += 1
        if total_matches == len(azucar_normalized):
            tipo_azucar_id = int(azucar[0])

    return tipo_azucar_id

def get_marca_azucar(nombre: str) -> int:
    '''Consigue la marca en base a cuantos matcheos tiene el nombre del producto.
    Cuando la cantidad de matches de la base es igual a la del nombre del producto 
    entonces recien ahi se le asigna el id correspondiente.
    En caso de no encontrar se pone -1 y luego con la limpieza de datos se asigna'''
    
    marca_id = -1

    sql_query = f"SELECT IdMarca, Nombre FROM `{PROJECT_AND_DATASET}.marcas`"
    query = client.query(sql_query)
    result = query.result()

    nombre_normalized = normalize_accent(nombre)
    for marca in result:
        marca_normalized = normalize_accent(marca[1]).split()
        total_matches = 0
        for m in marca_normalized:
            if nombre_normalized.find(m) != -1:
                total_matches += 1
        if total_matches == len(marca_normalized):
            marca_id = int(marca[0])

    return marca_id

def get_provincia(nombre: str) -> int:
    '''Consigue la provincia en base al nombre de provincia '''
    provincia_id = -1

    if nombre == "":
        return provincia_id
    else:
        sql_query = f"SELECT IdProvincia FROM `{PROJECT_AND_DATASET}.provincias` WHERE Nombre LIKE '{nombre}'"
        query = client.query(sql_query)
        result = query.result()

        for idprovincia in result:
            provincia_id = (idprovincia[0])
    return provincia_id

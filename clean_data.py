import re
import os
import sys
from google.cloud import bigquery
from google.oauth2 import service_account

current = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(1,current)
import common

KEY_PATH = "/key.json"
PROJECT_AND_DATASET = "alumnos-sandbox.precios_productos"

credentials = service_account.Credentials.from_service_account_file(KEY_PATH)
client = bigquery.Client(credentials=credentials, project=credentials.project_id)

def clean_tipo_azucar():
    '''Se encarga de limpiar los campos que hayan dado erroneo en la base de datos sobre el tipo de azucar'''

    sql_query = f'SELECT IdProducto, Nombre FROM `{PROJECT_AND_DATASET}.precios_azucar` WHERE IdTipoAzucar = -1'
    query = client.query(sql_query)
    result = query.result()

    for falla_tipo_azucar in result:
        id_azucar = -1
        nombre = falla_tipo_azucar[1].lower()
        if re.search("azúcar (blanca|com(u|ú)n|light)", nombre): 
            id_azucar = 1
        elif re.search("(endulzante|hileret|azúcar en polvo light|azucar hileret)", nombre):
            id_azucar = 4
        elif re.search("(rubio|org(a|á)nica|org(a|á)nico|negra)", nombre):
            id_azucar = 2
        elif re.search("(impalpable)", nombre):
            id_azucar = 3
        elif re.search("azucar", nombre):
            id_azucar = 1

        sql_query = f"UPDATE `{PROJECT_AND_DATASET}.precios_azucar` SET IdTipoAzucar = { id_azucar } where IdProducto = { int(falla_tipo_azucar[0]) }"

        query = client.query(sql_query)
        result = query.result()

def clean_marca():
    '''Se encarga de limpiar los campos que hayan dado erroneo en la base de datos sobre la marca'''

    sql_query = 'SELECT IdProducto, Nombre FROM `{PROJECT_AND_DATASET}.precios_azucar` WHERE IdMarca = -1'
    query = client.query(sql_query)
    result = query.result()

    sql_marcas = 'SELECT IdMarca, Nombre FROM `{PROJECT_AND_DATASET}.marcas`'
    query = client.query(sql_marcas)
    result_marcas = query.result()


    for falla_marca in result:
        id_marca = -1
        nombre = falla_marca[1]
        print(nombre)

        for marcas in result_marcas:
            if re.search(f"{marcas[1].lower()}", nombre.lower()):
                id_marca = int(marcas[0])
                break
            
        sql_query = f"UPDATE `{PROJECT_AND_DATASET}.precios_azucar` SET IdMarca = { id_marca } where IdProducto = { int(falla_marca[0]) }"
        query = client.query(sql_query)
        query.result()
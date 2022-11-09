from datetime import datetime
import requests
from selenium import webdriver
import mysql.connector
import unicodedata

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "oycobe",
    database = 'humai'
)

def get_last_id():
    mycursor = mydb.cursor()
    sql = "Select MAX(IdProducto) from productos"
    mycursor.execute(sql)
    result = mycursor.fetchall()
    for id in result:
        id = id[0]
    return id


def insertar_azucar(nombreProducto: str, precio: float, link: str):
    mycursor = mydb.cursor()
    id = get_last_id() + 1
    IdProvincia = get_provincia(nombreProducto)
    IdMarca = get_marca_azucar(nombreProducto)
    IdTipoAzucar = get_tipo_azucar(nombreProducto)

    sql = "Insert into productos (IdProducto, Nombre, IdTipoAzucar, IdMarca, Precio, Link, FechaBajada, IdProvincia) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    values = (id, nombreProducto, IdTipoAzucar, IdMarca, precio, link, datetime.now(), IdProvincia)
    mycursor.execute(sql,values)
    mydb.commit()
    #mycursor.close()
    #mydb.close()

def get_project_path():
    q = "find /home -type d -name 'Tp_humai_2' -print"
    result = subprocess.getoutput(q).split("\n")
    for path in result:
        if "Training-Humai" in path:
            final_path = path
    
    return final_path


def get_file_directory(file_name):
    file_directory = os.path.join(get_project_path(), file_name)
    return file_directory

def write_csv(data):
    file_name = 'coto_' + datetime.today().strftime('%d-%m-%Y') + '.csv'
    file_directory = get_file_directory(file_name)

    if os.path.isfile(file_directory):
        with open(file_directory, 'a', encoding='UTF8') as file:
            writer = csv.writer(file, delimiter='\t')
            writer.writerow(data)
    else:
        with open(file_directory, 'w', encoding='UTF8') as file:
            writer = csv.writer(file, delimiter='\t')
            writer.writerow(["nombre", "IdTipoAzucar","IdMarca","Precio","link","FechaBajada","IdProvincia"])
            writer.writerow(data)

    return file_directory

def normalize_accent(word: str) -> str:
    return ''.join(c for c in unicodedata.normalize('NFD', word)
                  if unicodedata.category(c) != 'Mn').lower()

def get_page(url: str) -> None:
    response = requests.request("GET",url)
    print(response.text)

def get_selenium_page(url: str):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome('/home/tomi/Tp_humai_2/Training-Humai/chromedriver',options = options)
    driver.get(url)
    return driver

def get_tipo_azucar(nombre: str) -> int:
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
    
    id = 3
    return id

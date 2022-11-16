from lxml import etree
import re

import os
import sys
import logging

logging.basicConfig(
    filename='/home/grupo2/Training-Humai/scrapers/maxiconsumo.log',
    format= '%(asctime)s.%(msecs)03d %(levelname)s - : %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
    )

current = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.dirname(current)
sys.path.insert(1,parent_directory)
import common
import clean_data


localidades = {"BUENOS AIRES": "sucursal_burzaco", "CHUBUT": "sucursal_comodoro_rivadavia", "CABA": "sucursal_capital", "MENDOZA": "sucursal_mendoza", "Tierra del Fuego, Antártida e Islas del Atlántico Sur": "sucursal_rio_grande", "SAN JUAN": "sucursal_san_juan", "SAN LUIS": "sucursal_san_luis", "SANTA FE": "sucursal_santa_fe", "CHACO": "sucursal_chaco"}


def get_data() -> None:
    '''Funcion utilizada para traer todos los datos de azucar de maxiconsumos
    La idea es iterar sobre las locaciones disponibles para poder traer los datos y luego limpiar la data que pueda haber
    quedado sin matchear en la base de datos'''
    for localidad, direccion in localidades.items():
        url = f"https://maxiconsumo.com/{direccion}/almacen/endulzantes.html?product_list_limit=96"
        logging.info(f"Starting with {url}")

        page = common.get_page(url,{})
        dom = etree.HTML(str(page))

        tot_azucares = dom.xpath("//ul[@class='list']/li[contains(@class,'list-item')]")
        logging.info(f"Tot to process: {len(tot_azucares)}")
        for azucar in tot_azucares:
            try:
                titulo = azucar.xpath(".//div[contains(@class,'product-item')]/div/h2/a")[0].text.strip()
                link = azucar.xpath(".//div[contains(@class,'product-item')]/div/h2/a/@href")[0]

                try:
                    precio = azucar.xpath(".//div[contains(@class,'product-item')]/div/../div[2]/span/span/span[2]/span")[0].text.replace('.','').replace(',','.').replace('$','').strip()
                except:
                    precio = ""
            
                if precio != "":
                    precio_final = float(precio)
                    common.insertar_azucar(titulo, precio_final, link, localidad)
            except Exception as exp:
                logging.error(f"Exception found: {exp}")

    logging.info(f"Finished scraping")

    logging.info(f"Start cleaning brand")
    try:
        clean_data.clean_marca()
        logging.info(f"Finished cleaning brand")
    except Exception as exp:
        logging.info(f"Error on cleaning brand {exp}")

    logging.info(f"Start cleaning sugar")
    try:
        clean_data.clean_tipo_azucar()
        logging.info(f"Finished cleaning sugar")
    except Exception as exp:
        logging.info(f"Error on cleaning sugar {exp}")
    
get_data()
from lxml import etree
import re

import os
import csv
from datetime import datetime
import subprocess


import sys
sys.path.insert(1,'/home/tomi/Tp_humai_2/Training-Humai')
import common
import clean_data


localidades = {"BUENOS AIRES": "sucursal_burzaco", "CHUBUT": "sucursal_comodoro_rivadavia", "CABA": "sucursal_capital", "MENDOZA": "sucursal_mendoza", "Tierra del Fuego, Antártida e Islas del Atlántico Sur": "sucursal_rio_grande", "SAN JUAN": "sucursal_san_juan", "SAN LUIS": "sucursal_san_luis", "SANTA FE": "sucursal_santa_fe", "CHACO": "sucursal_chaco"}


def get_data() -> None:
    for localidad, direccion in localidades.items():
        url = f"https://maxiconsumo.com/{direccion}/almacen/endulzantes.html?product_list_limit=96"
    
        page = common.get_page(url,{})
        dom = etree.HTML(str(page))

        tot_azucares = dom.xpath("//ul[@class='list']/li[contains(@class,'list-item')]")
        for azucar in tot_azucares:
            titulo = azucar.xpath(".//div[contains(@class,'product-item')]/div/h2/a")[0].text.strip()
            link = azucar.xpath(".//div[contains(@class,'product-item')]/div/h2/a/@href")[0]

            try:
                precio = azucar.xpath(".//div[contains(@class,'product-item')]/div/../div[2]/span/span/span[2]/span")[0].text.replace('.','').replace(',','.').replace('$','').strip()
            except:
                precio = ""
            
            if precio != "":
                precio_final = float(precio)
                common.insertar_azucar(titulo, precio_final, link, localidad)
    
    print("Finalizado")
    clean_data.clean_marca()
    clean_data.clean_tipo_azucar()

get_data()
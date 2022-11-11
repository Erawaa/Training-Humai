from lxml import etree
import re


import os
import csv
from datetime import datetime
import subprocess


import sys
sys.path.insert(1,'/home/tomi/Tp_humai_2/Training-Humai')
import common

localidades = {"BUENOS AIRES": "laanonimasucursalnombre=9%20DE%20JULIO&laanonimasucursal=158", "CHUBUT": "laanonimasucursalnombre=COMODORO%20RIVADAVIA&laanonimasucursal=47", "CORDOBA": "laanonimasucursalnombre=MARCOS%20JUARES&laanonimasucursal=160", "CORRIENTES":"laanonimasucursalnombre=GOYA&laanonimasucursal=144","LA PAMPA":"laanonimasucursalnombre=GENERAL%20PICO&laanonimasucursal=105", "NEUQUEN":"laanonimasucursalnombre=CUTRAL%20CO&laanonimasucursal=154","RIO NEGRO":"laanonimasucursalnombre=ALLEN&laanonimasucursal=82","SANTA CRUZ":"laanonimasucursalnombre=RIO%20GALLEGOS&laanonimasucursal=59","SANTA FE":"laanonimasucursalnombre=ESPERANZA&laanonimasucursal=124","Tierra del Fuego, Antártida e Islas del Atlántico Sur":"laanonimasucursalnombre=RIO%20GRANDE&laanonimasucursal=70"}


def set_page_headers(susursal_nombre: str, sucursal_id: int):
    headers = {
        #'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
        #'X-XSRF-TOKEN': 'DGkGaciOhtRHqhJ9L88heRrgIs0+SQeTWM8QTRG3Zdg',
        #'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        #'Content-Type': 'application/json',
        #'Accept': 'application/json, text/plain, */*',
        #'X-Requested-With': 'XMLHttpRequest',
        #'sec-ch-ua-platform': '"Linux"',
        'cookie': f"cartelLogueado=0; laanonimaapp=0; laanonimaordenlistado=relevancia; _gcl_au=1.1.852268858.1665082108; mostrarConfSucursal=0; _hjSessionUser_2758890=eyJpZCI6IjNjNGNiZTY0LTI2ZjEtNTliMy05Zjc2LTE4ODVlYTNlMzdjYyIsImNyZWF0ZWQiOjE2NjUwODIxMDg2NDMsImV4aXN0aW5nIjp0cnVlfQ==; mostrar_ventana_sucursales=0; _ga_C7MTQBFBQN=GS1.1.1667241461.1.1.1667241906.58.0.0; _ce.s=v~c738ebf679b780b971cd0aca97b17f7530da4192~vpv~0~ir~1~v11nv~-1~v11.sla~1667241906490~v11.s~2293ede0-594c-11ed-8b12-8f65aedc919a~v11.send~1667241906444; laanonima=fa0d631e030e28fbfcdcb779cd217223; _gid=GA1.2.400910927.1668018208; laanonimadatos=YTo1OntzOjE2OiJjb2RpZ29fc2VndXJpZGFkIjtzOjY6ImM0OHp6ayI7czoxMzoibnVtZXJvY2Fycml0byI7czozMjoiYjFlNzY3OWYzOTliZjFiMzk1MTYyMGMzMzUyMzFjYjgiO3M6MTU6InRfbnVtZXJvY2Fycml0byI7czo3OiJhbm9uaW1vIjtzOjEyOiJtb250b19taW5pbW8iO2Q6MDtzOjE2OiJjYXJyaXRvX2FudGVyaW9yIjtpOjA7fQ%3D%3D; _hjSession_2758890=eyJpZCI6IjllNDRhMzYwLTk4NmQtNDdiZi04NGY5LThlNThjM2Y1MDM4MSIsImNyZWF0ZWQiOjE2NjgwMjU0Mjk5NTgsImluU2FtcGxlIjpmYWxzZX0=; _hjAbsoluteSessionInProgress=0; _hjIncludedInSessionSample=0; _ga_W3SKYF6FJF=GS1.1.1668025429.9.1.1668026961.39.0.0; _ga=GA1.2.1422790702.1665082108; laanonimasucursalnombre={susursal_nombre}; laanonimasucursal={sucursal_id}"
    }
    return headers

def get_data() -> None:
    for localidad, direccion in localidades.items():
        url = f"https://supermercado.laanonimaonline.com/almacen/endulzantes/n2_21/?{direccion}"
        
        sucursal_nombre = re.search("laanonimasucursalnombre=.*&", url).group().replace("laanonimasucursalnombre=","").replace("&","")
        sucursal_id = re.search("aanonimasucursal=.*", url).group().replace("aanonimasucursal=","")
        
        headers = set_page_headers(sucursal_nombre, sucursal_id)
        page = common.get_page(url,headers)
        dom = etree.HTML(str(page))

        tot_azucares = dom.xpath('//div[@class="maq_col_2"]//div[contains(@class,"caja1 producto")]/div[contains(@id,"prod_")]')
        for azucar in tot_azucares:
            titulo = azucar.xpath("./div[@class='col1_listado']/div/a")[0].text
            link_pre = azucar.xpath("./div[@class='col1_listado']/div/a/@href")[0]
            link = f"https://supermercado.laanonimaonline.com{link_pre}"
            precio_entero = azucar.xpath("./div[@class='col2_listado']/div/div[@class='contenedor-plus']/div/div")[0].text.replace(".","")
            precio_decimal = azucar.xpath("./div[@class='col2_listado']/div/div[@class='contenedor-plus']/div/div/span")[0].text
            precio_final = float(f"{precio_entero}{precio_decimal}".replace('$','').replace(",",".").strip())
            
            common.insertar_azucar(titulo, precio_final, link, localidad)
    
    print("Finalizado")

get_data()
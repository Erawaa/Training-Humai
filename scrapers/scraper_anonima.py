from selenium import webdriver
from selenium.webdriver.common.by import By

import os
import csv
from datetime import datetime
import subprocess


import sys
sys.path.insert(1,'/home/tomi/Tp_humai_2/Training-Humai')
import common


localidades = ['BUENOS AIRES','CHUBUT','CORDOBA','CORRIENTES','LA PAMPA','NEUQUEN','RIO NEGRO','SANTA CRUZ','SANTA FE','TIERRA DEL FUEGO','Localidad ','9 DE JULIO','AZUL','BRAGADO','CARLOS CASARES','CHACABUCO','CHIVILCOY','GENERAL VILLEGAS','JUNIN','LINCOLN','MERCEDES','PEHUAJO','TRENQUE LAUQUEN','Localidad ','COMODORO RIVADAVIA','ESQUEL','PUERTO MADRYN','RADA TILLY','TRELEW','Localidad ','MARCOS JUARES','MORTEROS','Localidad ','GOYA','Localidad ','GENERAL PICO','SANTA ROSA','Localidad ','CENTENARIO','CUTRAL CO','JUNIN DE LOS ANDES','NEUQUEN','PLOTTIER','SAN MARTIN DE LOS ANDES','VILLA LA ANGOSTURA','ZAPALA','Localidad ','ALLEN','CATRIEL','CHOELE CHOEL','CINCO SALTOS','CIPOLLETTI','EL BOLSON','GENERAL ROCA','SAN CARLOS DE BARILOCHE','VIEDMA','VILLA REGINA','Localidad ','CALETA OLIVIA','RIO GALLEGOS','Localidad ','ESPERANZA','RAFAELA','VENADO TUERTO','Localidad ','RIO GRANDE','USHUAIA','Sucursal','AV. BUSTILLO KM 13 12974','ALBARRACIN 601','Sucursal','AV. SAN JUAN 51','ANTARTIDA ARGENTINA 1111','Sucursal','ROCA 623','Sucursal','SAN JUAN 1425','Sucursal','ALVARO BARROS 1408','Sucursal','BELGRANO 292','Sucursal','CHUBUT 1400','Sucursal','ROCA 710','Sucursal','GUEMES 741','Sucursal','13 DE DICIEMBRE 150','Sucursal','AV. DEL TRABAJO 469','Sucursal','MAIPU 1332','Sucursal','AV.SAN MARTIN 1605','Sucursal','LOS ÑIRES 2237','Sucursal','AV. CIPOLLETTI 502','Sucursal','9 DE JULIO 574','Sucursal','JUAN B.JUSTO 301','Sucursal','SARMIENTO 36','Sucursal','AV. FEDERICO SOAREZ 52','Sucursal','RIVADAVIA 2070','Sucursal','RUTA 7 KM 260','Sucursal','AMEGHINO 1250','Sucursal','ITUZAINGO 147','Sucursal','TTE. GRAL. ROCA 450','Sucursal','AV. GARCIA SALINAS 1100','Sucursal','CALLE 7 1064','Sucursal','VICENTE LOPEZ 40','Sucursal','RIVAROLA 310','Sucursal','SAN MARTIN 200','Sucursal','CORONEL SUAREZ 465','Sucursal','RIVADAVIA 53','Sucursal','BELGRANO 1998','Sucursal','EL CHILCO 83','Sucursal','LUQUE 1200','Sucursal','SAN MARTIN 507','Sucursal','MONSEÑOR CANEVA 560','Sucursal','ING. EDUARDO GARRO 538','Sucursal','CALLE 40 937','Sucursal','AV. PRIMEROS CONSEJALES 256','Sucursal','AVENIDA DEL LIBERTADOR 75','Sucursal','HECTOR GIL 64','Sucursal','BV 9 DE JULIO 2339','Sucursal','MIGUEL EGUINOA 1802','Sucursal','AMEGHINO 1097','Sucursal','AGUSTIN ALVAREZ 261','Sucursal','BV. LARDIZABAL 250','Sucursal','AV.CASEY 799']


def get_data():
    pag = common.get_selenium_page("https://supermercado.laanonimaonline.com/almacen/endulzantes/n2_21/")

    azucar = pag.find_elements(By.XPATH,"//div[@id='maq_pie']")

    print(azucar)

    pagina = common.get_selenium_page("https://supermercado.laanonimaonline.com/almacen/endulzantes/n2_21/")
    azucares_disponibles = pagina.find_elements(By.XPATH,"//ul[@id='products']/li")
    
    locaciones = pagina.find_elements(By.XPATH,"")
    print(locaciones)
    for locacion in locaciones:

        print(locacion)
    
    #azucares_disponibles = driver.find_elements(By.XPATH,"//ul[@id='products']/li")
    #for azucares in azucares_disponibles:
        #titulo = azucares.find_element(By.XPATH, ".//div[@class='leftList']//a").text
        #link = azucares.find_element(By.XPATH, ".//div[@class='leftList']//a").get_attribute('href')
        #precio = azucares.find_elements(By.XPATH, ".//div[@class='info_discount']/span[contains(@class,'atg_store_productPrice')]/span[contains(@class,'atg_store_newPrice')]")
        #precio_final = ""
        #for p in precio:
            #precio_final = p.text
        #precio_final = precio_final.replace('$','').replace(",",".")       
        #if (titulo and precio_final and link):
            #common.insertar_azucar(titulo, float(precio_final), link)

    print("Finalizado")
    driver.quit()


get_data()

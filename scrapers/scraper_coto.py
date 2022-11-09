from selenium import webdriver
from selenium.webdriver.common.by import By

import os
import csv
from datetime import datetime
import subprocess


import sys
sys.path.insert(1,'/home/tomi/Tp_humai_2/Training-Humai')
import common


def get_data() -> None:
    driver = common.get_selenium_page("https://www.cotodigital3.com.ar/sitios/cdigi/browse/catalogo-almac%C3%A9n-endulzantes-az%C3%BAcar/_/N-1w1x9xa")
    azucares_disponibles = driver.find_elements(By.XPATH,"//ul[@id='products']/li")
    for azucares in azucares_disponibles:
        titulo = azucares.find_element(By.XPATH, ".//div[@class='leftList']//a").text
        link = azucares.find_element(By.XPATH, ".//div[@class='leftList']//a").get_attribute('href')
        precio = azucares.find_elements(By.XPATH, ".//div[@class='info_discount']/span[contains(@class,'atg_store_productPrice')]/span[contains(@class,'atg_store_newPrice')]")
        precio_final = ""
        for p in precio:
            precio_final = p.text
        precio_final = precio_final.replace('$','').replace(",",".")       
        if (titulo and precio_final and link):
            common.insertar_azucar(titulo, float(precio_final), link)

    print("Finalizado")
    driver.quit()


get_data()

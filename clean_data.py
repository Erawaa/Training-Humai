import re
import os
import sys

current = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(1,current)
import common

def clean_tipo_azucar():
    '''Se encarga de limpiar los campos que hayan dado erroneo en la base de datos sobre el tipo de azucar'''
    mycursor = common.mydb.cursor()
    sql = 'Select IdProducto, Nombre from productos where IdTipoAzucar = -1'
    mycursor.execute(sql)
    result = mycursor.fetchall()

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
        
        sql = "Update productos set IdTipoAzucar = %s where IdProducto = %s"
        values = (id_azucar, int(falla_tipo_azucar[0]))
        mycursor.execute(sql, values)
        common.mydb.commit()

def clean_marca():
    '''Se encarga de limpiar los campos que hayan dado erroneo en la base de datos sobre la marca'''
    mycursor = common.mydb.cursor()
    sql = 'Select IdProducto, Nombre from productos where IdMarca = -1'
    mycursor.execute(sql)
    result = mycursor.fetchall()

    sql_marcas = 'Select IdMarca, Nombre from Marcas'
    mycursor.execute(sql_marcas)
    result_marcas = mycursor.fetchall()


    for falla_marca in result:
        id_marca = -1
        nombre = falla_marca[1]
        print(nombre)

        for marcas in result_marcas:
            if re.search(f"{marcas[1].lower()}", nombre.lower()):
                id_marca = int(marcas[0])
                break
        sql = "Update productos set IdMarca = %s where IdProducto = %s"
        values = (id_marca, int(falla_marca[0]))
        mycursor.execute(sql, values)
        common.mydb.commit()
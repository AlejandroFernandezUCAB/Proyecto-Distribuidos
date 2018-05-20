# -*- coding: utf-8 -()

import time

# NOTA: se debera leer el archivo de palabras y llenar ambos diccionarios. Esta data es de prueba.
# mapa que tiene las palabras, el numero de incidencias, y las lineas en donde se encuentran
    # mapa['<palabra>'] = [  <numero de incidencias>  ,  <numero de linea de la primera incidencia>]
# (deben estar en minuscula)
mapa = {'regurgitación': [0,None], 'aurícula': [0,None], 'pericarditis': [0,None], 'insuficiencia mitral': [0,None], 'trombosis intraventricular': [0,None]}
# diccionario que tiene las palabras y sus definiciones
diccionario = {'regurgitación': '(regurgitación => Expulsar por la boca,sin vómito,sustancias sólidas o líquidas contenidas en el estómago o en el esófago)' ,
 'aurícula': '(aurícula => Cada una de las dos cavidades superiores del corazón de los anfibios, reptiles, aves y mamíferos, situadas sobre los ventrículos, que reciben la sangre de las venas)', 
 'pericarditis': '(pericarditis => Inflamación del pericardio)', 
 'insuficiencia mitral': '(insuficiencia mitral => Reflujo de sangre ocasionado por la incapacidad de la válvula mitral del corazón de cerrarse firmemente)', 
 'trombosis intraventricular': '( trombosis intraventricular => complicación frecuente en el infarto agudo del miocardio de localización anterior, asociado a discinesia ventricular.)'}

PATH_LIBRO = 'libro_medicina.txt'

# recibe: linea del libro y su indice respectivo
# devuleve: un diccionario que tiene la siguiente composicion:
def contarPalabras(linea, indice):
    # A D V E R T E C I A
    # ---------------------
    # la siguiente linea es un fume
    # tarde como media hora para resolverlo
    # muy bonito python...
    # pero una cagada el manejo de caracteres ;)
    #	Linea para version aterir de libr ---> linea = linea.decode('cp1252').encode('utf-8')
    # explicacion:
        # para obtener el archivo txt use adobe reader para convertir el PDF
        # al parecer el programa utiliza esa codificacion de caracteres por vainas de windows
        # https://marketing.adobe.com/resources/help/en_US/whitepapers/multibyte/multibyte_windows1252.html
        # https://stackoverflow.com/questions/12468179/unicodedecodeerror-utf8-codec-cant-decode-byte-0x9c?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa
    
    # print ('\nlinea: {}'.format(linea))
    # time.sleep(0.8)
    # iteramos las llaves del mapa previamente creado
    for palabra in mapa.keys():
        # busca la incidencia de la palabra en toda la linea
        incidencias = linea.count(palabra,0,len(linea))

        if incidencias != 0:

            if mapa[palabra][0] == 0: # si es la primera incidencia
                mapa[palabra][1] = indice  # guardo la linea donde la encontre

            mapa[palabra][0] += incidencias # aumenta la cuenta de la palabra


# reemplaza la primera incidencia de la palabra
def reemplazarPrimeraPalabra(lineas_libro):
    # recorremos el mapa
    for palabra in mapa.keys():
        # si se encontro la palabra
        if mapa[palabra][0] != 0:
            # ir a la linea del libro y reemplazar palabra por definicion
                # A D V E R T E C I A  2
                # ---------------------
                # este es un fume un poco mas feo
                # basicamente pasa esto:
                    # leo en codificacion cp1252, codifico a utf-8, reemplazo, decodifico utf-8, codifico en cp1252 para escribir 
            # Linea para version anterior del libro ----> lineas_libro[ mapa[palabra][1] ] = lineas_libro[ mapa[palabra][1] ].decode('cp1252').encode('utf-8').replace(palabra,diccionario[palabra]).decode('utf-8').encode('cp1252')
 	    lineas_libro[ mapa[palabra][1] ] = lineas_libro[ mapa[palabra][1] ].replace(palabra,diccionario[palabra])

            # print ('\N-----\NVOY A REEMPLAZAR\NANTES:{}\NDESPUES:{}\N-----\N')

def main():
    # F A S E  1
    # -----------
    # leer libro y contar palabras
    with open(PATH_LIBRO,'r') as libro:
        # convertimos las lineas del libro en una lista de lineas
        lineas_libro = libro.readlines()

        print ('El libro tiene {} Lineas.\nBuscando palabras y generando mapa de incidencias...'.format( str(len(lineas_libro)) ))
        
        # print(lineas_libro[:9])
        # with open('10lineas.txt','w') as target:
        #     target.writelines(lineas_libro[:9])

        for idx, linea in enumerate(lineas_libro):
            # print(idx)
            contarPalabras(linea.lower(), idx) # convertimos todas las palabras a minusculas...
        
        #imprimir cantidad de palabras
        print (mapa)


    # F A S E  2
    # -----------
    # reemplazamos las primeras incidencias
    reemplazarPrimeraPalabra(lineas_libro)

    # escribimos los cambios
    with open('libroModificado.txt','w') as target:
        target.writelines(lineas_libro)

if __name__ == '__main__':
    main()

# links
# https://stackoverflow.com/questions/11552320/correct-way-to-pause-python-program
# http://www.leccionespracticas.com/uncategorized/eliminar-tildes-con-python-solucionado
# https://www.mayoclinic.org/es-es/diseases-conditions/mitral-valve-regurgitation/symptoms-causes/syc-20350178?utm_source=Google&utm_medium=abstract&utm_content=Mitral-regurgitation&utm_campaign=Knowledge-panel
# https://www.tutorialspoint.com/python/string_replace.htm

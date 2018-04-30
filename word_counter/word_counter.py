# -*- coding: utf-8 -()

import time
# import unicodedata # necesario para funcion eliminar_tildes

# def elimina_tildes(s):
#    return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))

# NOTA: se debera leer el archivo de palabras y llenar ambos diccionarios. Esta data es de prueba.
# mapa que tiene las palabras, el numero de incidencias, y las lineas en donde se encuentran
# (deben estar en minuscula)
mapa = {'regurgitación': [0,[]], 'aurícula': [0,[]], 'pericarditis': [0,[]], 'insuficiencia mitral': [0,[]], 'trombosis intraventricular': [0,[]]}
# diccionario que tiene las palabras y sus definiciones
diccionario = {'regurgitación': '(regurgitacion => Expulsar por la boca,sin vómito,sustancias sólidas o líquidas contenidas en el estómago o en el esófago)' ,
 'aurícula': ('aurícula => Cada una de las dos cavidades superiores del corazón de los anfibios, reptiles, aves y mamíferos, situadas sobre los ventrículos, que reciben la sangre de las venas'), 
 'pericarditis': '(pericarditis => Inflamación del pericardio)', 
 'insuficiencia mitral': '(insuficiencia mitral => Reflujo de sangre ocasionado por la incapacidad de la válvula mitral del corazón de cerrarse firmemente)', 
 'trombosis intraventricular': '( trombosis intraventricular => complicación frecuente en el infarto agudo del miocardio de localización anterior, asociado a discinesia ventricular.)'}

lineas_libro = []

# recibe: linea del libro y su indice respectivo
# devuleve: un diccionario que tiene la siguiente composicion:
    # mapa['<palabra>'] = <numero de incidencias>
def contarPalabras(linea, indice):
    # iteramos las llaves del mapa previamente creado
    for palabra in mapa.keys():
        # busca la incidencia de la palabra en toda la linea
        incidencias = linea.count(palabra,0,len(linea))
        # print ('busco {}\nlinea: {} \nEncontre: {}'.format(palabra,linea,incidencias))
        # time.sleep(1)

        if incidencias != 0:
            # if mapa[palabra] == 0: # si es la primera incidencia
            #     lineas_libro[indice] = linea.replace(palabra,diccionario[palabra]) # reemplaza la palabra por su definicion...

            mapa[palabra][0] += incidencias # aumenta la cuenta de la palabra
            mapa[palabra][1].append(indice)



def main():
    # F A S E  1
    # -----------
    # leer libro y contar palabras
    with open('C:\\Users\\gian\\Documents\\Python\\word_counter\\cardiologia.txt','r') as libro:
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
        # print (mapa)
        print ('[')
        for item in mapa.values():
            print(item[0])
        print (']')

    # F A S E  2
    # -----------
    # Modificar la primera instancia de las palabras encontradas
        # iteramos por cada palabra del mapa y la modificamos accediendo a la(s) linea(s correspondiente(s)

    # with open('libroModificado.txt','w') as target:
    #     target.writelines(lineas_libro)

if __name__ == '__main__':
    main()

# links
# https://stackoverflow.com/questions/11552320/correct-way-to-pause-python-program
# http://www.leccionespracticas.com/uncategorized/eliminar-tildes-con-python-solucionado
# https://www.mayoclinic.org/es-es/diseases-conditions/mitral-valve-regurgitation/symptoms-causes/syc-20350178?utm_source=Google&utm_medium=abstract&utm_content=Mitral-regurgitation&utm_campaign=Knowledge-panel
# https://www.tutorialspoint.com/python/string_replace.htm
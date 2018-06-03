def createFile():

    #Esto crea el archivo, si ya esta creado lo sobre escribe
    #El primer argumento es para darle el nombre al archivo, el segundo
    #le dice que hara con el arhicvo, en este caso sera "Write"

    file = open("Test.txt","w")
    file.write("Hola Mundo")
    
    #Esto cierra el archivo
    file.close()

def readFile():
    #En este caso se lee el archivo y se imprime lo leido
    file = open("Test.txt","r")
    read = file.read()
    print read
    file.close()

def readFileCantidad( cantidad ):
    file = open("Test.txt","r")
    read = file.read( cantidad )
    print read
    file.close()

def readFileLine():
    #Solo se lee la primera linea del programa
    file = open("Test.txt", "r")
    read = file.readline()
    print read
    file.close()

def readFileLineMore():
    #Esto lee varias lines y las muestra como un array
    file = open("Test.txt", "r")
    read = file.readlines()
    print read
    file.close()

def readHowObject():
    #Esto lee por lineas
    file = open("Test.txt", "r")
    for line in file:
        print line
    file.close()

def splitGod():
    #ESTO NOS SALVARA EL PROYECTO
    with open("Test.txt","r") as f:
        data = f.read()
        words = data.split()
    print words

#Este es el main
if __name__ == "__main__":
    #Creando el archivo
    #createFile()
    
    #readFile()
    #readFileCantidad( input("Cantidad de caracteres a mostrar\n") )
    #readFileLine()
    readFileLineMore()
    #readHowObject()
    #splitGod()

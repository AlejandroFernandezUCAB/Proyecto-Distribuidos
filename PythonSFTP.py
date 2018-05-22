import pysftp

BEEHIVE = '192.168.25.100'
BEEHIVE_PUB = '200.2.13.226'
CARPETA_COMPARTIDA = '/home/group/distribuidos/201825_25789/13/programasMPI/ScatterManual'

# lee las credenciales del archivo de configuracion.
# Si no lo encuentra las crea...
def obtenerCredenciales():
    pkeyPass = ''
    pkeyPath = ''
    user = ''
    try:
        # leemos
        configFile = open('user.conf','r') 
        # quitamos saltos de linea
        user = configFile.readline().replace('\n','')
        pkeyPath = str(configFile.readline()).replace('\n','')
        pkeyPass = str(configFile.readline()).replace('\n','')

    except IOError:
        print 'No se encontro el archivo de configuracion...creandolo...'
        user = str(raw_input('Introduzca su usuario UCAB (sin @est.ucab.edu.ve) >> ')) + '\n'
        pkeyPath = str(raw_input('Introduzca la ruta de su llave privada >> ')) + '\n'
        pkeyPass = str(raw_input('Introduzca la clave de su llave >> '))
        configFile = open('user.conf','w')
        configFile.write(user)
        configFile.write(pkeyPath)
        configFile.write(pkeyPass)
    # print 'usuario {} \nruta {} \nclave {}'.format(user, pkeyPath, pkeyPass)
        # quitamos saltos de linea
        user = user.replace('\n','')
        pkeyPath = pkeyPath.replace('\n','')
        pkeyPass = pkeyPass.replace('\n','')
    return [user, pkeyPath, pkeyPass]

def conexionSftp(credenciales):

    return pysftp.Connection(
        BEEHIVE,
        username=str(credenciales[0]), 
        private_key=str(credenciales[1]), 
        private_key_pass=str(credenciales[2]) 
        )

    # return pysftp.Connection(
    #         '192.168.25.100',
    #         username=user, 
    #         private_key=pkeyPath, 
    #         private_key_pass=pkeyPass 
    #         )

if __name__ == '__main__':
    credenciales = obtenerCredenciales()
    print credenciales
    conexion = conexionSftp(credenciales)

    # Solo cambia el comando que quieres hacer aqui
    # conexion.mkdir('holaMundo', mode=664)

    with conexion.cd(CARPETA_COMPARTIDA):
        #Aqui hay que colocar el archivo a subir
        conexion.put('Documentos Cluster/programasMPI/scatterManual/scatterManual.py')
        conexion.put('Documentos Cluster/programasMPI/scatterManual/scatterManual.sbatch')
        for attr in conexion.listdir_attr():
            print attr.filename, attr

        # #Aqui se coloca la direccion donde se va a subir el archivo, en este caso somos el grupo 13
        # with sftp.cd('/home/group/distribuidos/201825_25789/13'):
        #     #Aqui hay que colocar el archivo a subir
        #     sftp.put('HolaMundoFTP')
        #     for attr in sftp.listdir_attr():
        #         print attr.filename, attr
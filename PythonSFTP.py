import pysftp


# lee las credenciales del archivo de configuracion.
# Si no lo encuentra las crea...
def obtenerCredenciales():
    pkeyPass = ''
    pkeyPath = ''
    user = ''
    try:
        configFile = open('user.conf','r') 
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
    return [user, pkeyPath, pkeyPass]

def conexionSftp(credenciales):

    return pysftp.Connection(
        '192.168.25.100',
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

    conexion.mkdir('holaMundo', mode=664)

import pysftp

with pysftp.Connection(
        '192.168.25.100',
        #Nombre Usuario
        username='pafernandez.14', 
        #Sitio de su clave privada
        private_key='/home/pedro/Documentos/Universidad/Sistemas Distribuidos/Pedro', 
        #Passphrase  de su clave privada
        private_key_pass='informatica.668' 
        ) as sftp:

    #Aqui se coloca la direccion donde se va a subir el archivo, en este caso somos el grupo 13
    with sftp.cd('/home/group/distribuidos/201825_25789/13'):
        #Aqui hay que colocar el archivo a subir
        sftp.put('HolaMundoFTP')
        for attr in sftp.listdir_attr():
            print attr.filename, attr

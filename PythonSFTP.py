import pysftp

with pysftp.Connection(
        '192.168.25.100',
        username='pafernandez.14', 
        private_key='/home/pedro/Documentos/Universidad/Sistemas Distribuidos/Pedro', 
        private_key_pass='informatica.668' 
        ) as sftp:
    sftp.mkdir('holaMundo', mode=664)

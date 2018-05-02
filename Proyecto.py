# Proyecto 1 de Sistemas Distribuidos
# 

#  F A S E  1 
#  - - - - - - - - - - -
# hay 2 operaciones en paralelo:
    # operacion Coordinador
        # 1 - Enviar libro y lista de palabras
        # 2 - Recibir palabras ordenadas y sus cantidades, de los trabajadores.
        #     (Recibe de 2 en 2, hace merge sort y luego guarda en archivo temporal local. De 5 a 10 archivos temporales).
    # operacion Trabajador
        # 1 - Buscar palabras y contarlas (adicionalmente se guarda la posicion de la primera linea)
        # 2 - Ordenar las palabras encontradas
        # 3 - Enviar lista de palabras y sus cantidades al coordinador

#   F A S E  2
#   - - - - - - - - - - - 
# hay 2 operaciones en paralelo:
    # Operacion Coordinador:
        # 1 - Combinar y ordenar las palabras en los archivos temporales con merge sort
        # 2 - Recibir libro modificado por los nodos del anillo
    # Operacion Trabajador:
        # 1 - si el rango del trabajador es diferente a 0 (x != 0)
            # a - recibe el libro del anterior (Nx-1  -->  Nx)
            # b - reemplaza la primera incidencia de todas sus palabras
            # c - envia  el libro al siguiente (siguiente = (rango + 1)%TamañoAnillo )
        # 2 - si el rango del trabajador es igual a 0 (x == 0)
            # a - reemplaza la primera incidencia de todas sus palabras
            # b - envia  el libro al siguiente
            # c - recibo el libro del ultimo nodo del anillo, y me bloqueo 
            #     mientras me llega el mensaje del ultimo (IMPORTANTE)
            # d - envio libro modificado por todos los trabajadores a el coordinador

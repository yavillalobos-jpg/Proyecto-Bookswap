# ORDENAMIENTO BURBUJA: seis variantes, sin clases.
# Todas reciben una lista de libros (nodos del catálogo) y devuelven:
#   [lista_ordenada, [comparaciones, intercambios, pasadas]]
# Trabajan sobre una COPIA de la lista: la lista enlazada del catálogo no cambia.
# Siempre se intercambian elementos vecinos (o a distancia "salto" en peine):
# esa es la idea de la burbuja, los valores grandes "suben" hacia el final.

# Campos por los que se puede ordenar: [clave del formulario, posición en el nodo, nombre].
CAMPOS = [['codigo', 0, 'Código'], ['titulo', 1, 'Título'], ['autor', 2, 'Autor'],
          ['precio', 6, 'Precio'], ['universidad', 4, 'Universidad'], ['carrera', 9, 'Carrera']]

# Métodos disponibles: [clave del formulario, nombre visible].
METODOS = [['clasica', 'Burbuja clásica'], ['mejorada', 'Burbuja mejorada'],
           ['bidireccional', 'Burbuja bidireccional'],
           ['par_impar', 'Burbuja par-impar'], ['peine', 'Burbuja de peine'],
           ['enlazada', 'Burbuja en lista enlazada']]


def nombre_metodo(metodo):
    for clave, nombre in METODOS:
        if clave == metodo:
            return nombre
    raise ValueError('Método de ordenamiento desconocido.')


def posicion_campo(campo):
    for clave, posicion, nombre in CAMPOS:
        if clave == campo:
            return posicion
    raise ValueError('Campo de ordenamiento desconocido.')


def valor(libro, posicion):
    # Los textos se comparan sin importar mayúsculas; los números como números.
    dato = libro[posicion]
    if isinstance(dato, str):
        return dato.strip().lower()
    return dato


def fuera_de_orden(a, b, posicion, descendente, contador):
    # Devuelve True si "a" debe ir después de "b". Cuenta cada comparación.
    contador[0] += 1
    if descendente:
        return valor(a, posicion) < valor(b, posicion)
    return valor(a, posicion) > valor(b, posicion)


def intercambiar(lista, i, j, contador):
    lista[i], lista[j] = lista[j], lista[i]
    contador[1] += 1


def burbuja_clasica(libros, posicion, descendente=False):
    # Recorre la lista n-1 veces completas, aunque ya esté ordenada.
    lista = libros[:]
    contador = [0, 0, 0]
    n = len(lista)
    for pasada in range(n - 1):
        contador[2] += 1
        for i in range(n - 1):
            if fuera_de_orden(lista[i], lista[i + 1], posicion, descendente, contador):
                intercambiar(lista, i, i + 1, contador)
    return [lista, contador]


def burbuja_mejorada(libros, posicion, descendente=False):
    # Dos mejoras: 1) después de cada pasada el último elemento ya está en su
    # lugar, así que el límite se reduce; 2) si una pasada no hizo intercambios
    # (bandera en False), la lista ya está ordenada y se termina antes.
    lista = libros[:]
    contador = [0, 0, 0]
    limite = len(lista) - 1
    hubo_cambio = True
    while hubo_cambio and limite > 0:
        hubo_cambio = False
        contador[2] += 1
        for i in range(limite):
            if fuera_de_orden(lista[i], lista[i + 1], posicion, descendente, contador):
                intercambiar(lista, i, i + 1, contador)
                hubo_cambio = True
        limite -= 1
    return [lista, contador]


def burbuja_bidireccional(libros, posicion, descendente=False):
    # También llamada "sacudida" o cocktail sort: una pasada va de izquierda a
    # derecha (sube el mayor) y la siguiente de derecha a izquierda (baja el menor).
    lista = libros[:]
    contador = [0, 0, 0]
    inicio = 0
    fin = len(lista) - 1
    hubo_cambio = True
    while hubo_cambio and inicio < fin:
        hubo_cambio = False
        contador[2] += 1
        for i in range(inicio, fin):
            if fuera_de_orden(lista[i], lista[i + 1], posicion, descendente, contador):
                intercambiar(lista, i, i + 1, contador)
                hubo_cambio = True
        fin -= 1
        if not hubo_cambio:
            break
        hubo_cambio = False
        contador[2] += 1
        for i in range(fin, inicio, -1):
            if fuera_de_orden(lista[i - 1], lista[i], posicion, descendente, contador):
                intercambiar(lista, i - 1, i, contador)
                hubo_cambio = True
        inicio += 1
    return [lista, contador]


def burbuja_par_impar(libros, posicion, descendente=False):
    # Alterna dos fases: compara pares (0,1), (2,3)... y luego (1,2), (3,4)...
    # Termina cuando ninguna de las dos fases hizo intercambios.
    lista = libros[:]
    contador = [0, 0, 0]
    n = len(lista)
    ordenada = False
    while not ordenada:
        ordenada = True
        for primero in [0, 1]:
            contador[2] += 1
            for i in range(primero, n - 1, 2):
                if fuera_de_orden(lista[i], lista[i + 1], posicion, descendente, contador):
                    intercambiar(lista, i, i + 1, contador)
                    ordenada = False
    return [lista, contador]


def burbuja_peine(libros, posicion, descendente=False):
    # Comb sort: como la burbuja, pero al principio compara elementos separados
    # por un "salto" grande. El salto se divide entre 1.3 en cada pasada hasta
    # llegar a 1; desde ahí es una burbuja mejorada normal.
    lista = libros[:]
    contador = [0, 0, 0]
    n = len(lista)
    salto = n
    hubo_cambio = True
    while salto > 1 or hubo_cambio:
        salto = int(salto / 1.3)
        if salto < 1:
            salto = 1
        hubo_cambio = False
        contador[2] += 1
        for i in range(n - salto):
            if fuera_de_orden(lista[i], lista[i + salto], posicion, descendente, contador):
                intercambiar(lista, i, i + salto, contador)
                hubo_cambio = True
    return [lista, contador]


def burbuja_lista_enlazada(libros, posicion, descendente=False):
    # Burbuja recorriendo NODOS en lugar de posiciones de una lista.
    # Se arma una lista enlazada auxiliar: cada nodo es [libro, siguiente],
    # igual que el catálogo usa nodo[15] para apuntar al siguiente.
    # No se cambian los enlaces: se intercambia el libro guardado en dos nodos
    # vecinos. Así el catálogo guardado en datos.json no cambia de orden.
    cabeza = None
    for i in range(len(libros) - 1, -1, -1):
        cabeza = [libros[i], cabeza]
    contador = [0, 0, 0]
    fin = None  # Desde este nodo hasta el final, todo ya está ordenado.
    hubo_cambio = True
    while hubo_cambio and cabeza is not None and cabeza[1] is not fin:
        hubo_cambio = False
        contador[2] += 1
        actual = cabeza
        while actual[1] is not fin:
            siguiente = actual[1]
            if fuera_de_orden(actual[0], siguiente[0], posicion, descendente, contador):
                actual[0], siguiente[0] = siguiente[0], actual[0]
                contador[1] += 1
                hubo_cambio = True
            actual = siguiente
        # El último nodo revisado ya tiene el valor mayor: queda fijo.
        fin = actual
    # Se recorre la lista enlazada para devolverla como lista y mostrarla.
    lista = []
    actual = cabeza
    while actual is not None:
        lista.append(actual[0])
        actual = actual[1]
    return [lista, contador]


def ordenar(libros, metodo, campo, descendente=False):
    # Punto de entrada usado por la página web.
    posicion = posicion_campo(campo)
    if metodo == 'clasica':
        return burbuja_clasica(libros, posicion, descendente)
    if metodo == 'mejorada':
        return burbuja_mejorada(libros, posicion, descendente)
    if metodo == 'bidireccional':
        return burbuja_bidireccional(libros, posicion, descendente)
    if metodo == 'par_impar':
        return burbuja_par_impar(libros, posicion, descendente)
    if metodo == 'peine':
        return burbuja_peine(libros, posicion, descendente)
    if metodo == 'enlazada':
        return burbuja_lista_enlazada(libros, posicion, descendente)
    raise ValueError('Método de ordenamiento desconocido.')


def comparar_metodos(libros, campo, descendente=False):
    # Ejecuta todos los métodos sobre los mismos datos para comparar su trabajo.
    resultado = []
    for clave, nombre in METODOS:
        contador = ordenar(libros, clave, campo, descendente)[1]
        resultado.append([nombre, contador[0], contador[1], contador[2]])
    return resultado

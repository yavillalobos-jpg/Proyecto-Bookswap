# LISTA ENLAZADA SIMPLE: cada nodo representa un libro.
# Los nodos son listas de Python; las operaciones son funciones.


# Cada nodo es una lista con estas posiciones:
# 0 código, 1 título, 2 autor, 3 propietario, 4 universidad,
# 5 modalidad, 6 precio, 7 prestatario, 8 universidad del prestatario,
# 9 carrera, 10 estado, 11 destinatario, 12 universidad del destinatario,
# 13 código del libro intercambiado, 14 cola, 15 enlace al siguiente nodo.
# La cabeza apunta al primer nodo; None indica el final.
# IMPORTANTE: nodo[15] guarda el siguiente nodo, no su código.
def crear_nodo(codigo, titulo, autor, propietario, universidad,
               modalidad, precio, carrera="Sin especificar"):
    return [codigo, titulo, autor, propietario, universidad,
            modalidad, precio, "", "", carrera, "Disponible", "", "", 0, [], None]


def agregar_libro(cabeza, nuevo):
    if cabeza is None:
        return nuevo
    actual = cabeza
    while actual[15] is not None:
        actual = actual[15]
    actual[15] = nuevo
    return cabeza


def buscar_codigo(cabeza, codigo):
    actual = cabeza
    while actual is not None:
        if actual[0] == codigo:
            return actual
        actual = actual[15]
    return None


def quitar_libro(cabeza, codigo):
    anterior = None
    actual = cabeza
    while actual is not None:
        if actual[0] == codigo:
            if anterior is None:
                return actual[15]
            anterior[15] = actual[15]
            return cabeza
        anterior = actual
        actual = actual[15]
    return cabeza


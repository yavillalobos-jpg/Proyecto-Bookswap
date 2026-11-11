# Árbol binario de búsqueda: [libro, hijo_izquierdo, hijo_derecho].
# Comparamos el código del libro. No usamos clases.
def insertar(raiz, libro):
    nuevo = [libro, None, None]
    if raiz is None:
        return nuevo
    actual = raiz
    while True:
        if libro[0] == actual[0][0]:
            return raiz
        lado = 1 if libro[0] < actual[0][0] else 2
        if actual[lado] is None:
            actual[lado] = nuevo
            return raiz
        actual = actual[lado]


def construir(cabeza):
    raiz = None
    actual = cabeza
    while actual is not None:
        raiz = insertar(raiz, actual)
        actual = actual[15]
    return raiz


def buscar(raiz, codigo):
    recorrido = []
    while raiz is not None:
        recorrido.append(raiz[0][0])
        if codigo == raiz[0][0]:
            return raiz[0], recorrido
        raiz = raiz[1] if codigo < raiz[0][0] else raiz[2]
    return None, recorrido

# Grafo no dirigido como listas de adyacencia: [[universidad, [vecinos]], ...].
# Cada intercambio confirmado agrega una conexión entre universidades distintas.
def normalizar(nombre):
    return nombre.strip().upper()


def agregar_vertice(grafo, nombre):
    nombre = normalizar(nombre)
    for vertice in grafo:
        if vertice[0] == nombre:
            return vertice
    nuevo = [nombre, []]
    grafo.append(nuevo)
    return nuevo


def conectar(grafo, a, b):
    primero = agregar_vertice(grafo, a)
    segundo = agregar_vertice(grafo, b)
    if primero[0] == segundo[0]:
        return
    if segundo[0] not in primero[1]:
        primero[1].append(segundo[0])
    if primero[0] not in segundo[1]:
        segundo[1].append(primero[0])


def construir(cabeza, conexiones):
    grafo = []
    actual = cabeza
    while actual is not None:
        agregar_vertice(grafo, actual[4])
        actual = actual[15]
    for a, b in conexiones:
        conectar(grafo, a, b)
    return grafo


def camino(grafo, origen, destino):
    # Recorrido en anchura (BFS), usando una cola de caminos.
    origen, destino = normalizar(origen), normalizar(destino)
    nombres = [v[0] for v in grafo]
    if origen not in nombres or destino not in nombres:
        return []
    cola = [[origen]]
    visitados = [origen]
    while cola:
        ruta = cola.pop(0)
        ultimo = ruta[-1]
        if ultimo == destino:
            return ruta
        for nombre, vecinos in grafo:
            if nombre == ultimo:
                for vecino in vecinos:
                    if vecino not in visitados:
                        visitados.append(vecino)
                        cola.append(ruta + [vecino])
    return []

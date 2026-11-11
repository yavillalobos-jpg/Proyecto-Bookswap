# Lista doblemente enlazada: [evento, anterior, siguiente].
# La estructura completa contiene [primero, ultimo].
def agregar(extremos, evento):
    nuevo = [evento, extremos[1], None]
    if extremos[1] is None:
        extremos[0] = nuevo
    else:
        extremos[1][2] = nuevo
    extremos[1] = nuevo


def construir(eventos):
    extremos = [None, None]
    for evento in eventos:
        agregar(extremos, evento)
    return extremos


def recorrer(extremos, inverso=False):
    resultado = []
    actual = extremos[1] if inverso else extremos[0]
    while actual is not None:
        resultado.append(actual[0])
        actual = actual[1] if inverso else actual[2]
    return resultado

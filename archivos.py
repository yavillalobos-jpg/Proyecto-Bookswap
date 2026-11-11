# JSON almacena datos, no referencias entre nodos.
# Reconstruimos los enlaces al cargar. Guardamos todo en una sola operación.
import json
import os
from catalogo import agregar_libro

ARCHIVO = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'datos.json')


def validar_libro(libro):
    if not isinstance(libro, list) or len(libro) != 15:
        raise ValueError('Registro de libro inválido.')
    if type(libro[0]) is not int or libro[0] <= 0:
        raise ValueError('Código inválido en JSON.')
    for posicion in [1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 12]:
        if not isinstance(libro[posicion], str):
            raise ValueError('Texto inválido en JSON.')
    if any(not libro[i].strip() for i in [1, 2, 3, 4, 9]):
        raise ValueError('Datos incompletos en JSON.')
    if libro[5] not in ['Venta', 'Intercambio', 'Préstamo']:
        raise ValueError('Modalidad inválida en JSON.')
    if type(libro[6]) is not int or libro[6] < 0 or (libro[5] == 'Venta' and libro[6] == 0):
        raise ValueError('Precio inválido en JSON.')
    if libro[10] not in ['Disponible', 'Vendido', 'Intercambiado']:
        raise ValueError('Estado inválido en JSON.')
    if type(libro[13]) is not int or libro[13] < 0:
        raise ValueError('Código de intercambio inválido.')
    if not isinstance(libro[14], list):
        raise ValueError('Cola inválida.')
    for solicitud in libro[14]:
        if not isinstance(solicitud, list) or len(solicitud) != 2 or not all(isinstance(s, str) and s.strip() for s in solicitud):
            raise ValueError('Solicitud inválida.')


def cargar_datos():
    try:
        with open(ARCHIVO, encoding='utf-8') as archivo:
            datos = json.load(archivo)
    except FileNotFoundError:
        return None, [], [], []
    if not isinstance(datos, dict) or datos.get('version') != 1:
        raise ValueError('Formato JSON desconocido.')
    for clave in ['libros', 'historial', 'pila', 'conexiones']:
        if not isinstance(datos.get(clave), list):
            raise ValueError('Falta la lista ' + clave + '.')
    cabeza = None
    codigos = []
    for registro in datos['libros']:
        validar_libro(registro)
        if registro[0] in codigos:
            raise ValueError('Hay códigos duplicados en JSON.')
        codigos.append(registro[0])
        cabeza = agregar_libro(cabeza, registro + [None])
    for registro in datos['pila']:
        validar_libro(registro)
    for evento in datos['historial']:
        if not isinstance(evento, str):
            raise ValueError('Historial inválido.')
    for conexion in datos['conexiones']:
        if not isinstance(conexion, list) or len(conexion) != 2 or not all(isinstance(s, str) and s.strip() for s in conexion):
            raise ValueError('Conexión inválida.')
    return cabeza, datos['historial'], datos['pila'], datos['conexiones']


def guardar_datos(cabeza, eventos, pila, conexiones):
    libros = []
    actual = cabeza
    while actual is not None:
        libros.append(actual[:15])
        actual = actual[15]
    datos = {'version': 1, 'libros': libros, 'historial': eventos,
             'pila': pila, 'conexiones': conexiones}
    temporal = ARCHIVO + '.tmp'
    try:
        with open(temporal, 'w', encoding='utf-8') as archivo:
            json.dump(datos, archivo, ensure_ascii=False, indent=2)
        os.replace(temporal, ARCHIVO)
    finally:
        if os.path.exists(temporal):
            os.remove(temporal)

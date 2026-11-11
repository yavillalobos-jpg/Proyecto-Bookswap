# Funciones para procesar datos de formularios, sin input() ni print().
# Las operaciones trabajan sobre la lista enlazada del catálogo.
from catalogo import crear_nodo, agregar_libro, buscar_codigo, quitar_libro
from entradas import texto, entero
from prestamos import operar_prestamo

def disponible(libro):
    return libro[10] == "Disponible" and not libro[7] and not libro[14]



def buscar(cabeza, datos, campo='codigo'):
    libro = buscar_codigo(cabeza, entero(datos, campo))
    if libro is None:
        raise ValueError('No existe el libro indicado en ' + campo + '.')
    return libro


def misma_persona(nombre, universidad, otro_nombre, otra_universidad):
    return (nombre.lower() == otro_nombre.lower()
            and universidad.lower() == otra_universidad.lower())


def listar_libros(cabeza, consulta=''):
    # La lista enlazada sigue siendo el catálogo; esta lista permite mostrarlo.
    resultado = []
    actual = cabeza
    consulta = consulta.strip().lower()
    while actual is not None:
        if (not consulta or consulta in actual[1].lower()
                or consulta in actual[2].lower() or consulta in actual[4].lower()
                or consulta in actual[9].lower() or consulta == str(actual[0])):
            resultado.append(actual)
        actual = actual[15]
    return resultado


def revisar(cabeza, accion, datos):
    # Se verifica de nuevo al confirmar: no se confía en los campos ocultos.
    if accion == 'comprar':
        libro = buscar(cabeza, datos)
        if libro[5] != 'Venta' or not disponible(libro):
            raise ValueError('El libro no está disponible para venta.')
        nombre = texto(datos, 'comprador')
        universidad = texto(datos, 'universidad')
        if misma_persona(nombre, universidad, libro[3], libro[4]):
            raise ValueError('El propietario no puede comprar su propio libro.')
        return 'Comprar ' + libro[1] + ' por C$ ' + str(libro[6]) + ' a ' + libro[3] + '.'
    if accion == 'intercambiar':
        a = buscar(cabeza, datos, 'codigo_deseado')
        b = buscar(cabeza, datos, 'codigo_ofrecido')
        if a[0] == b[0]:
            raise ValueError('Seleccione dos libros distintos.')
        if (a[5] != 'Intercambio' or b[5] != 'Intercambio'
                or not disponible(a) or not disponible(b)):
            raise ValueError('Ambos libros deben estar disponibles para intercambio.')
        if misma_persona(a[3], a[4], b[3], b[4]):
            raise ValueError('Los libros deben pertenecer a personas distintas.')
        return (a[3] + ' recibirá ' + b[1] + '. ' + b[3] + ' recibirá ' + a[1] + '.')
    if accion == 'eliminar':
        libro = buscar(cabeza, datos)
        if libro[7] or libro[14]:
            raise ValueError('No se puede eliminar un libro prestado o con solicitudes.')
        return 'Eliminar la publicación: ' + libro[1] + '.'
    raise ValueError('Operación desconocida.')


def ejecutar(cabeza, accion, datos):
    if accion == 'publicar':
        codigo = entero(datos, 'codigo')
        if buscar_codigo(cabeza, codigo) is not None:
            raise ValueError('Ese código ya existe.')
        modalidad = texto(datos, 'modalidad')
        if modalidad not in ['Venta', 'Intercambio', 'Préstamo']:
            raise ValueError('Seleccione una modalidad válida.')
        precio = entero(datos, 'precio') if modalidad == 'Venta' else 0
        nuevo = crear_nodo(codigo, texto(datos, 'titulo'), texto(datos, 'autor'),
                           texto(datos, 'propietario'), texto(datos, 'universidad'),
                           modalidad, precio, texto(datos, 'carrera'))
        return agregar_libro(cabeza, nuevo), 'Libro publicado.'

    if accion in ['comprar', 'intercambiar', 'eliminar']:
        revisar(cabeza, accion, datos)
        if accion == 'comprar':
            libro = buscar(cabeza, datos)
            libro[10] = 'Vendido'
            libro[11] = texto(datos, 'comprador')
            libro[12] = texto(datos, 'universidad')
            return cabeza, 'Compra registrada. El pago y la entrega se acuerdan fuera del programa.'
        if accion == 'intercambiar':
            a = buscar(cabeza, datos, 'codigo_deseado')
            b = buscar(cabeza, datos, 'codigo_ofrecido')
            a[10], a[11], a[12], a[13] = 'Intercambiado', b[3], b[4], b[0]
            b[10], b[11], b[12], b[13] = 'Intercambiado', a[3], a[4], a[0]
            return cabeza, 'Intercambio registrado. Ambas publicaciones quedan cerradas.'
        return quitar_libro(cabeza, entero(datos, 'codigo')), 'Publicación eliminada.'

    return operar_prestamo(cabeza, accion, datos)

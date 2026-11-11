# COLAS FIFO: append() agrega al final y pop(0) retira la primera solicitud.
from catalogo import buscar_codigo
from entradas import texto, entero


def misma_persona(nombre, universidad, otro_nombre, otra_universidad):
    return nombre.lower() == otro_nombre.lower() and universidad.lower() == otra_universidad.lower()


def operar_prestamo(cabeza, accion, datos):
    libro = buscar_codigo(cabeza, entero(datos, "codigo"))
    if libro is None:
        raise ValueError("No existe ese libro.")
    if libro[5] != 'Préstamo' or libro[10] != 'Disponible':
        raise ValueError('El libro no está habilitado para préstamo.')
    if accion == 'solicitar-prestamo':
        nombre = texto(datos, 'solicitante')
        universidad = texto(datos, 'universidad')
        if misma_persona(nombre, universidad, libro[3], libro[4]):
            raise ValueError('No puede solicitar su propio libro.')
        if misma_persona(nombre, universidad, libro[7], libro[8]):
            raise ValueError('Esa persona ya tiene el libro prestado.')
        for solicitud in libro[14]:
            if misma_persona(nombre, universidad, solicitud[0], solicitud[1]):
                raise ValueError('Esa persona ya está en la cola.')
        libro[14].append([nombre, universidad])
        return cabeza, 'Solicitud registrada. Posición: ' + str(len(libro[14])) + '.'
    if accion == 'atender-prestamo':
        if libro[7]:
            raise ValueError('Primero debe registrar la devolución del libro.')
        if not libro[14]:
            raise ValueError('No hay solicitudes pendientes para ese libro.')
        solicitud = libro[14].pop(0)
        libro[7], libro[8] = solicitud[0], solicitud[1]
        return cabeza, 'Libro prestado a ' + libro[7] + '.'
    if accion == 'devolver':
        if not libro[7]:
            raise ValueError('Ese libro no está prestado.')
        libro[7], libro[8] = '', ''
        return cabeza, 'Devolución registrada. Puede atender la siguiente solicitud.'
    raise ValueError('Operación desconocida.')

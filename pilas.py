# Pila LIFO: la última publicación eliminada es la primera que se recupera.
from catalogo import buscar_codigo, agregar_libro


def apilar(pila, libro):
    # Copiamos los datos, sin el enlace al resto del catálogo.
    pila.append(libro[:14] + [[solicitud[:] for solicitud in libro[14]]])


def restaurar(cabeza, pila):
    if not pila:
        raise ValueError('No hay publicaciones eliminadas para recuperar.')
    if buscar_codigo(cabeza, pila[-1][0]) is not None:
        raise ValueError('El código ya está ocupado. La pila permanece intacta.')
    libro = pila.pop() + [None]
    return agregar_libro(cabeza, libro), libro[0]

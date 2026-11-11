# Validaciones para los formularios.
def texto(datos, campo):
    valor = datos.get(campo, '').strip()
    if not valor or any(c in valor for c in ['|', '\n', '\r']):
        raise ValueError('Complete ' + campo + ' sin barras | ni saltos de línea.')
    return valor


def entero(datos, campo):
    try:
        numero = int(datos.get(campo, ''))
    except (ValueError, TypeError):
        raise ValueError(campo + ': escriba un número entero positivo.')
    if numero <= 0:
        raise ValueError(campo + ': debe ser mayor que cero.')
    return numero



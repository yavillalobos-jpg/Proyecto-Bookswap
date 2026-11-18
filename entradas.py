# Validaciones para los formularios.
def texto(datos, campo):
    valor = datos.get(campo, '').strip()
    if not valor or any(c in valor for c in ['|', '\n', '\r']):
        raise ValueError('Complete ' + campo + ' sin barras | ni saltos de línea.')
    if len(valor) > 120:
        raise ValueError(campo + ': máximo 120 caracteres.')
    return valor


def entero(datos, campo):
    try:
        numero = int(datos.get(campo, ''))
    except (ValueError, TypeError):
        raise ValueError(campo + ': escriba un número entero positivo.')
    if numero <= 0:
        raise ValueError(campo + ': debe ser mayor que cero.')
    return numero


def misma_persona(nombre, universidad, otro_nombre, otra_universidad):
    # Compara nombre y universidad sin importar mayúsculas ni espacios extra.
    return (nombre.strip().lower() == otro_nombre.strip().lower()
            and universidad.strip().lower() == otra_universidad.strip().lower())



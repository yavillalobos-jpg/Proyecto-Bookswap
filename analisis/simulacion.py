# SIMULACIÓN PASO A PASO DE LA BURBUJA MEJORADA (la misma idea que usa la página).
# Ejecutar desde la carpeta principal del proyecto:
#   py analisis\simulacion.py
#   py analisis\simulacion.py 9 3 7 1 5
# Muestra la entrada, cada comparación, cada intercambio, cada pasada y la salida.
import sys

# Se agrega la carpeta principal para poder usar burbujas.py y catalogo.py.
sys.path.append('.')
import burbujas
from catalogo import crear_nodo


def simular(numeros):
    lista = numeros[:]
    comparaciones = 0
    intercambios = 0
    pasadas = 0
    limite = len(lista) - 1
    hubo_cambio = True
    print('ENTRADA:', lista)
    print()
    while hubo_cambio and limite > 0:
        hubo_cambio = False
        pasadas = pasadas + 1
        print('--- Pasada', pasadas, '(revisa posiciones 0 a', str(limite) + ')')
        for i in range(limite):
            comparaciones = comparaciones + 1
            a = lista[i]
            b = lista[i + 1]
            if a > b:
                lista[i] = b
                lista[i + 1] = a
                intercambios = intercambios + 1
                hubo_cambio = True
                print('  Compara', a, 'y', b, '-> intercambia ->', lista)
            else:
                print('  Compara', a, 'y', b, '-> se quedan   ->', lista)
        print('  Queda fijo al final:', lista[limite])
        if not hubo_cambio:
            print('  No hubo intercambios: la lista ya está ordenada, se termina antes.')
        limite = limite - 1
        print()
    print('SALIDA:', lista)
    print('Comparaciones:', comparaciones, '| Intercambios:', intercambios, '| Pasadas:', pasadas)
    return [lista, [comparaciones, intercambios, pasadas]]


def comprobar_con_el_proyecto(numeros, resultado, contador):
    # Se ordena lo mismo con burbujas.py (sobre nodos) para verificar que coincide.
    nodos = []
    for n in numeros:
        nodos.append(crear_nodo(n, 'Libro', 'Autor', 'P', 'U', 'Venta', 1))
    respuesta = burbujas.ordenar(nodos, 'mejorada', 'codigo')
    ordenados = respuesta[0]
    contador_proyecto = respuesta[1]
    codigos = []
    for nodo in ordenados:
        codigos.append(nodo[0])
    if codigos == resultado and contador_proyecto == contador:
        print('Verificación con burbujas.py: coincide')
    else:
        print('Verificación con burbujas.py: NO coincide')


if __name__ == '__main__':
    entrada = [5, 1, 4, 2, 8]
    if len(sys.argv) > 1:
        entrada = []
        for texto in sys.argv[1:]:
            entrada.append(int(texto))
    respuesta = simular(entrada)
    comprobar_con_el_proyecto(entrada, respuesta[0], respuesta[1])
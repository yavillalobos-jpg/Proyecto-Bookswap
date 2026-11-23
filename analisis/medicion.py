# ANÁLISIS A POSTERIORI: mide las 6 variantes de burbuja de burbujas.py.
# Ejecutar desde la carpeta principal del proyecto, poniendo un nombre al entorno:
#   py analisis\medicion.py entorno1
# En la otra computadora (segundo entorno):
#   py analisis\medicion.py entorno2
# Guarda analisis\resultados_<nombre>.csv y analisis\entorno_<nombre>.txt
import platform
import random
import sys
import time

# Se agrega la carpeta principal para poder usar burbujas.py y catalogo.py.
sys.path.append('.')
import burbujas
from catalogo import crear_nodo

TAMANOS = [100, 500, 1000, 2000]
DISTRIBUCIONES = ['aleatoria', 'ordenada', 'invertida']
# Se repite cada medición y se reporta el MENOR tiempo: así se descartan las
# interrupciones del sistema operativo (otros programas usando el procesador).
REPETICIONES = 5
SEMILLA = 2026     # misma semilla = mismos datos en los dos entornos


def crear_datos(n, distribucion):
    codigos = list(range(1, n + 1))
    if distribucion == 'aleatoria':
        random.seed(SEMILLA + n)
        random.shuffle(codigos)
    elif distribucion == 'invertida':
        codigos.reverse()
    libros = []
    for codigo in codigos:
        libros.append(crear_nodo(codigo, 'Libro', 'Autor', 'P', 'U', 'Venta', 1))
    return libros


def esta_ordenada(libros):
    for i in range(len(libros)):
        if libros[i][0] != i + 1:
            return False
    return True


def medir(nombre_entorno):
    # Lista de casos a medir: [distribución, n, clave del método, nombre, datos].
    casos = []
    for distribucion in DISTRIBUCIONES:
        for n in TAMANOS:
            datos = crear_datos(n, distribucion)
            for metodo, nombre in burbujas.METODOS:
                casos.append([distribucion, n, metodo, nombre, datos])
    tiempos = []
    contadores = []
    for caso in casos:
        tiempos.append([])
        contadores.append(None)
    # Se mide por rondas: en cada ronda se ejecutan TODOS los casos una vez.
    # Así, si el equipo se pone lento un momento, afecta a todos por igual.
    for ronda in range(REPETICIONES):
        print('Ronda', ronda + 1, 'de', REPETICIONES, '...')
        for i in range(len(casos)):
            distribucion, n, metodo, nombre, datos = casos[i]
            inicio = time.perf_counter()
            respuesta = burbujas.ordenar(datos, metodo, 'codigo')
            fin = time.perf_counter()
            if not esta_ordenada(respuesta[0]):
                print('ERROR: el método', nombre, 'no ordenó bien')
            tiempos[i].append(fin - inicio)
            contadores[i] = respuesta[1]
    filas = []
    print()
    for i in range(len(casos)):
        distribucion, n, metodo, nombre, datos = casos[i]
        contador = contadores[i]
        milisegundos = round(min(tiempos[i]) * 1000, 2)
        filas.append([nombre_entorno, distribucion, n, nombre, contador[0],
                      contador[1], contador[2], milisegundos])
        print(distribucion, '| n =', n, '|', nombre, '|', contador[0], 'comparaciones |',
              contador[1], 'intercambios |', contador[2], 'pasadas |', milisegundos, 'ms')
    return filas


def guardar(nombre_entorno, filas):
    ruta = 'analisis/resultados_' + nombre_entorno + '.csv'
    archivo = open(ruta, 'w', encoding='utf-8')
    archivo.write('entorno,distribucion,n,metodo,comparaciones,intercambios,pasadas,tiempo_ms\n')
    for fila in filas:
        textos = []
        for dato in fila:
            textos.append(str(dato))
        archivo.write(','.join(textos) + '\n')
    archivo.close()
    archivo = open('analisis/entorno_' + nombre_entorno + '.txt', 'w', encoding='utf-8')
    archivo.write('Python ' + platform.python_version() + '\n')
    archivo.write(platform.platform() + '\n')
    archivo.write(platform.processor() + '\n')
    archivo.close()
    print()
    print('Guardado en', ruta)


if __name__ == '__main__':
    nombre = 'entorno1'
    if len(sys.argv) > 1:
        nombre = sys.argv[1]
    print('Entorno:', nombre, '| Python', platform.python_version(), '|', platform.platform())
    print()
    guardar(nombre, medir(nombre))
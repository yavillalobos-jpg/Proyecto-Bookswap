# Pruebas sobre un JSON temporal: NO modifican datos.json del proyecto.
# Ejecutar: python pruebas.py
import ast
import json
import os
import tempfile
from pathlib import Path
import app
import archivos
import arboles
import grafos
import historial
import burbujas
from catalogo import buscar_codigo, crear_nodo


def libro_fijo(codigo, titulo, autor, propietario, universidad, modalidad, precio,
               carrera, estado='Disponible', destinatario='', universidad_destino=''):
    return [codigo, titulo, autor, propietario, universidad, modalidad, precio, '', '',
            carrera, estado, destinatario, universidad_destino, 0, []]


# Datos fijos de prueba: así las pruebas no dependen de lo que tenga datos.json.
DATOS_PRUEBA = {
    'version': 1,
    'libros': [
        libro_fijo(402, 'Diseño de espacios', 'Autor A', 'Estudiante 10', 'UAM', 'Intercambio', 0, 'Arquitectura'),
        libro_fijo(801, 'Psicología social', 'Autor B', 'Estudiante 19', 'UCN', 'Intercambio', 0, 'Psicología'),
        libro_fijo(112, 'Fundamentos de programación', 'Pepe', 'litzy', 'UAM', 'Venta', 700, 'Ingeniería'),
        libro_fijo(1056, 'Don Quijote', 'Cervantes', 'Camila', 'UAM', 'Venta', 800, 'Comunicación',
                   'Vendido', 'Yader', 'UAM'),
    ],
    'historial': [], 'pila': [], 'conexiones': [],
}


def probar_burbujas():
    metodos = [clave for clave, nombre in burbujas.METODOS]
    titulos = ['Química', 'álgebra', 'Biología', 'cálculo', 'Física', 'Arte', 'Biología', 'Zoología']
    libros = []
    for i in range(len(titulos)):
        libros.append(crear_nodo((i * 37) % 11 + 1, titulos[i], 'Autor', 'P', 'UNI',
                                 'Venta', (i * 53) % 17 + 1))
    for clave, posicion, nombre in burbujas.CAMPOS:
        esperado = sorted(burbujas.valor(l, posicion) for l in libros)
        for metodo in metodos:
            for descendente in [False, True]:
                ordenados, contador = burbujas.ordenar(libros, metodo, clave, descendente)
                obtenido = [burbujas.valor(l, posicion) for l in ordenados]
                assert obtenido == (esperado[::-1] if descendente else esperado), (metodo, clave)
                assert contador[0] >= contador[1] and contador[2] >= 1
    # No modifica la lista original.
    copia = libros[:]
    burbujas.ordenar(libros, 'clasica', 'titulo')
    assert libros == copia
    # Casos borde: lista vacía y de un elemento.
    for metodo in metodos:
        assert burbujas.ordenar([], metodo, 'codigo')[0] == []
        assert burbujas.ordenar(libros[:1], metodo, 'codigo')[0] == libros[:1]
    # Sobre una lista ya ordenada, la mejorada se detiene en una sola pasada.
    ordenada = burbujas.ordenar(libros, 'clasica', 'codigo')[0]
    assert burbujas.ordenar(ordenada, 'mejorada', 'codigo')[1] == [len(libros) - 1, 0, 1]
    assert burbujas.ordenar(ordenada, 'clasica', 'codigo')[1][2] == len(libros) - 1
    # La versión con nodos hace el mismo trabajo que la mejorada.
    for campo in ['titulo', 'precio', 'codigo']:
        mejorada = burbujas.ordenar(libros, 'mejorada', campo)
        assert burbujas.ordenar(libros, 'enlazada', campo) == mejorada
    # La burbuja clásica siempre hace (n-1)*(n-1) comparaciones.
    assert burbujas.ordenar(libros, 'clasica', 'precio')[1][0] == (len(libros) - 1) ** 2
    for metodo, campo in [['metodo_falso', 'titulo'], ['clasica', 'campo_falso']]:
        try:
            burbujas.ordenar(libros, metodo, campo)
            assert False, 'debía rechazar ' + metodo + ' / ' + campo
        except ValueError:
            pass
    assert len(burbujas.comparar_metodos(libros, 'titulo')) == len(metodos)


def probar():
    probar_burbujas()
    original = archivos.ARCHIVO
    contenido = Path(original).read_bytes()
    with tempfile.TemporaryDirectory() as carpeta:
        archivos.ARCHIVO = os.path.join(carpeta, 'datos.json')
        Path(archivos.ARCHIVO).write_text(json.dumps(DATOS_PRUEBA, ensure_ascii=False), encoding='utf-8')
        app.app.config['TESTING'] = True
        cliente = app.app.test_client()
        assert cliente.get('/').status_code == 200
        with cliente.session_transaction() as sesion:
            token = sesion['token']

        def enviar(ruta, datos, estado=303):
            respuesta = cliente.post('/' + ruta, data=dict(datos, token=token))
            assert respuesta.status_code == estado, (ruta, respuesta.status_code, respuesta.data[:300])
            return respuesta

        def libro(codigo):
            return buscar_codigo(archivos.cargar_datos()[0], codigo)

        def publicar(codigo, modalidad='Préstamo', uni='UNI'):
            enviar('publicar', dict(codigo=codigo, titulo='Libro prueba', autor='Autor',
                   propietario='Persona ' + str(codigo), universidad=uni,
                   carrera='Medicina', modalidad=modalidad, precio=100))

        assert libro(1056)[10] == 'Vendido' and libro(1056)[11] == 'Yader'
        assert cliente.post('/publicar', data={}).status_code == 400
        enviar('comprar',dict(codigo=112, comprador='Cliente', universidad='UNI'),200)
        assert libro(112)[10] == 'Disponible'
        enviar('comprar',dict(codigo=112, comprador='litzy', universidad='uam', confirmado='si'),400)
        enviar('comprar',dict(codigo=112, comprador='Cliente', universidad='UNI', confirmado='si'))
        assert libro(112)[10] == 'Vendido'
        enviar('comprar',dict(codigo=112, comprador='Otro', universidad='UNI', confirmado='si'),400)
        publicar(90001)
        enviar('publicar',dict(codigo=-1),400)
        enviar('publicar',dict(codigo=90001),400)
        for nombre in ['Ana','Luis']:
            enviar('solicitar-prestamo',dict(codigo=90001, solicitante=nombre, universidad='UAM'))
        enviar('solicitar-prestamo',dict(codigo=90001, solicitante='ana', universidad='uam'),400)
        enviar('eliminar',dict(codigo=90001, confirmado='si'),400)
        enviar('atender-prestamo',dict(codigo=90001))
        assert libro(90001)[7] == 'Ana'
        enviar('atender-prestamo',dict(codigo=90001),400)
        enviar('devolver',dict(codigo=90001))
        enviar('atender-prestamo',dict(codigo=90001))
        assert libro(90001)[7] == 'Luis'
        enviar('devolver',dict(codigo=90001))
        enviar('devolver',dict(codigo=90001),400)
        publicar(90002)
        for codigo in [90001,90002]:
            enviar('eliminar',dict(codigo=codigo),200)
            assert libro(codigo) is not None
            enviar('eliminar',dict(codigo=codigo, confirmado='si'))
        assert libro(90001) is None and libro(90002) is None
        enviar('deshacer',{})
        assert libro(90002) is not None and libro(90001) is None
        # Conflicto de código no consume la pila.
        publicar(90001)
        antes = Path(archivos.ARCHIVO).read_bytes()
        enviar('deshacer',{},400)
        assert Path(archivos.ARCHIVO).read_bytes() == antes
        # Árbol: raíces, izquierda, derecha, encontrado/no encontrado y cambios.
        cabeza,eventos,pila,conexiones = archivos.cargar_datos()
        raiz = arboles.construir(cabeza)
        for codigo in [402,112,801,90002]:
            hallado,pasos = arboles.buscar(raiz,codigo)
            assert hallado[0] == codigo and pasos[-1] == codigo
        assert arboles.buscar(raiz,999999)[0] is None
        assert cliente.get('/?codigo_arbol=90002').status_code == 200
        assert cliente.get('/?codigo_arbol=abc').status_code == 400
        # Historial usa ambos enlaces y persiste tras cargar el JSON.
        extremos = historial.construir(eventos)
        assert historial.recorrer(extremos) == eventos
        assert historial.recorrer(extremos,True) == list(reversed(eventos))
        assert extremos[0][1] is None and extremos[1][2] is None
        assert extremos[0][2][1] is extremos[0]
        # Intercambio real crea arista, no en la previsualización.
        enviar('intercambiar',dict(codigo_deseado=402,codigo_ofrecido=801),200)
        assert archivos.cargar_datos()[3] == []
        enviar('intercambiar',dict(codigo_deseado=402,codigo_ofrecido=801,confirmado='si'))
        assert libro(402)[13] == 801 and libro(801)[13] == 402
        cabeza,_,_,conexiones = archivos.cargar_datos()
        grafo=grafos.construir(cabeza,conexiones)
        assert grafos.camino(grafo,'uam','ucn') == ['UAM','UCN']
        assert grafos.camino(grafo,'UNI','UCN') == []
        grafos.conectar(grafo,'UCN','UNI')
        assert grafos.camino(grafo,'UAM','UNI') == ['UAM','UCN','UNI']
        assert grafos.camino(grafo,'NO EXISTE','UNI') == []
        assert cliente.get('/?origen=UAM&destino=UCN').status_code == 200
        assert cliente.get('/?orden=reciente').status_code == 200
        # La interfaz usa Tailwind compilado dentro de la página, sin JavaScript.
        assert b'tailwindcss' in cliente.get('/').data
        assert b'<script' not in cliente.get('/').data
        # Ordenar desde la página usa la burbuja, pero no muestra términos técnicos.
        pagina = cliente.get('/?ordenar=precio-desc')
        assert pagina.status_code == 200
        texto_pagina = pagina.data.decode('utf-8')
        assert 'urbuja' not in texto_pagina and 'comparaciones' not in texto_pagina
        assert texto_pagina.index('Don Quijote') < texto_pagina.index('Fundamentos de programación')
        pagina = cliente.get('/?ordenar=titulo').data.decode('utf-8')
        assert pagina.index('Don Quijote') < pagina.index('Psicología social')
        assert cliente.get('/?q=uam&ordenar=autor').status_code == 200
        antes = Path(archivos.ARCHIVO).read_bytes()
        assert cliente.get('/?ordenar=titulo-desc').status_code == 200
        assert Path(archivos.ARCHIVO).read_bytes() == antes  # Ordenar no guarda nada.
        assert cliente.get('/?ordenar=nada').status_code == 400
        assert cliente.get('/?ordenar=precio-nada').status_code == 400
        # Entrada HTML se muestra como texto, no se ejecuta.
        enviar('publicar',dict(codigo=90003,titulo='<script>x</script>',autor='A',
               propietario='P',universidad='UNI',carrera='Arte',modalidad='Préstamo'))
        assert b'&lt;script&gt;' in cliente.get('/?q=Arte').data
        # Archivo corrupto: no arranca vacío ni sobrescribe los datos.
        Path(archivos.ARCHIVO).write_text('{invalido',encoding='utf-8')
        assert cliente.get('/').status_code == 500
        enviar('deshacer',{},500)
        assert Path(archivos.ARCHIVO).read_text() == '{invalido'
        archivos.ARCHIVO = original
    assert Path(original).read_bytes() == contenido
    for archivo in Path(__file__).parent.glob('*.py'):
        assert not any(isinstance(n,ast.ClassDef) for n in ast.walk(ast.parse(archivo.read_text(encoding='utf-8'))))
    print('OK: operaciones, FIFO, LIFO, árbol, doble enlace, grafo/BFS, 6 burbujas, JSON, validaciones y formularios. Datos originales intactos.')


if __name__ == '__main__':
    probar()

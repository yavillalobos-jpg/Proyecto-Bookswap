# Flask conecta los formularios HTML con funciones de Python.
import secrets
from flask import Flask, render_template, request, redirect, url_for, session, flash
from archivos import cargar_datos, guardar_datos
from operaciones import listar_libros, revisar, ejecutar
from catalogo import buscar_codigo
from entradas import entero
import arboles
import historial
import pilas
import grafos

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)
app.config['MAX_CONTENT_LENGTH'] = 64 * 1024


@app.before_request
def proteger_formularios():
    # No es una cuenta de usuario. Identifica formularios de esta sesión.
    if 'token' not in session:
        session['token'] = secrets.token_hex(24)
    if request.method == 'POST' and request.form.get('token') != session['token']:
        return aviso('Formulario vencido. Vuelva al inicio y recargue.', 400)


def aviso(mensaje, estado=400):
    return render_template('index.html', pagina='mensaje', mensaje=mensaje), estado


# El POST al inicio solo muestra la vista previa del formulario.
@app.route('/', defaults={'pagina': 'catalogo'}, methods=['GET', 'POST'])
@app.route('/vista/<pagina>', methods=['GET', 'POST'])
def index(pagina):
    paginas = ['catalogo', 'publicar', 'comprar', 'intercambiar', 'prestamos',
               'atender', 'devoluciones', 'eliminar', 'historial', 'red']
    if pagina not in paginas:
        return aviso('Página desconocida.', 404)
    if request.method == 'POST' and pagina == 'catalogo':
        pagina = 'publicar'
    try:
        cabeza, eventos, pila, conexiones = cargar_datos()
    except (OSError, ValueError, IndexError, TypeError):
        return aviso('No se pudo leer datos.json. Revise su formato. No se guardaron cambios.', 500)
    consulta = request.args.get('q', '')
    libros = listar_libros(cabeza, consulta)
    recorrido = []
    busqueda = request.args.get('codigo_arbol', '').strip()
    if busqueda:
        try:
            codigo = entero(request.args, 'codigo_arbol')
        except ValueError as error:
            return aviso(str(error))
        # El árbol se reconstruye con el catálogo actual, sin índices obsoletos.
        raiz = arboles.construir(cabeza)
        libro, recorrido = arboles.buscar(raiz, codigo)
        libros = [libro] if libro is not None else []
    extremos = historial.construir(eventos)
    inverso = request.args.get('orden') == 'reciente'
    registro = historial.recorrer(extremos, inverso)
    grafo = grafos.construir(cabeza, conexiones)
    origen = request.args.get('origen', '').strip()
    destino = request.args.get('destino', '').strip()
    ruta = grafos.camino(grafo, origen, destino) if origen and destino else []
    return render_template('index.html', pagina=pagina, libros=libros, consulta=consulta,
                           busqueda=busqueda, recorrido=recorrido, registro=registro,
                           inverso=inverso, pila=pila, grafo=grafo, ruta=ruta,
                           origen=origen, destino=destino)


@app.route('/publicar', methods=['POST'])
@app.route('/comprar', methods=['POST'])
@app.route('/intercambiar', methods=['POST'])
@app.route('/solicitar-prestamo', methods=['POST'])
@app.route('/atender-prestamo', methods=['POST'])
@app.route('/devolver', methods=['POST'])
@app.route('/eliminar', methods=['POST'])
@app.route('/deshacer', methods=['POST'])
def procesar():
    accion = request.path[1:]
    try:
        cabeza, eventos, pila, conexiones = cargar_datos()
    except (OSError, ValueError, IndexError, TypeError):
        return aviso('No se pudo leer datos.json. No se guardaron cambios.', 500)
    try:
        if accion in ['comprar', 'intercambiar', 'eliminar']:
            resumen = revisar(cabeza, accion, request.form)
            if request.form.get('confirmado') != 'si':
                return render_template('index.html', pagina='confirmar', resumen=resumen,
                                       accion=accion, datos=request.form)
        if accion == 'deshacer':
            cabeza, codigo = pilas.restaurar(cabeza, pila)
            mensaje = 'Publicación recuperada: código ' + str(codigo) + '.'
        else:
            if accion == 'eliminar':
                # revisar() ya comprobó que no está prestado ni tiene cola.
                libro = buscar_codigo(cabeza, entero(request.form, 'codigo'))
                pilas.apilar(pila, libro)
            if accion == 'intercambiar':
                a = buscar_codigo(cabeza, entero(request.form, 'codigo_deseado'))
                b = buscar_codigo(cabeza, entero(request.form, 'codigo_ofrecido'))
                universidad_a = grafos.normalizar(a[4])
                universidad_b = grafos.normalizar(b[4])
            cabeza, mensaje = ejecutar(cabeza, accion, request.form)
            if accion == 'intercambiar' and universidad_a != universidad_b:
                par = sorted([universidad_a, universidad_b])
                if par not in conexiones:
                    conexiones.append(par)
        # El historial real se agrega mediante enlaces anterior/siguiente.
        extremos = historial.construir(eventos)
        detalle = accion + ': ' + mensaje
        if accion != 'deshacer':
            codigos = request.form.get('codigo', '') or (request.form.get('codigo_deseado', '') + ' / ' + request.form.get('codigo_ofrecido', ''))
            detalle += ' Código(s): ' + codigos
        historial.agregar(extremos, detalle)
        guardar_datos(cabeza, historial.recorrer(extremos), pila, conexiones)
    except ValueError as error:
        return aviso(str(error))
    except OSError:
        return aviso('No se pudo guardar datos.json. Revise los permisos.', 500)
    flash(mensaje)
    return redirect(url_for('index'), code=303)


if __name__ == '__main__':
    # Demostración local: evitamos escrituras simultáneas al archivo JSON.
    app.run(host='127.0.0.1', port=5000, debug=False, threaded=False)

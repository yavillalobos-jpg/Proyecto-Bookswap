# BookSwap

Página web para que estudiantes de distintas universidades vendan, intercambien y presten libros. Proyecto final de **Programación Estructurada** — Universidad Americana (UAM).

## Integrantes
- Litzy Mendoza
- Camila Vallejos
- Yader Villalobos

Docente: Jose Duran Garcia

## Tecnologías
- Python con Flask
- HTML con Tailwind CSS
- Almacenamiento en JSON (`datos.json`)
- Programación estructurada: solo funciones y listas

## Estructuras de datos
| Estructura | Archivo | Uso en la página |
|---|---|---|
| Lista enlazada | `catalogo.py` | Catálogo de libros |
| Lista doblemente enlazada | `historial.py` | Historial de operaciones |
| Árbol binario de búsqueda | `arboles.py` | Búsqueda por código |
| Grafo y búsqueda en anchura (BFS) | `grafos.py` | Red de universidades |
| Ordenamiento burbuja (6 variantes) | `burbujas.py` | Selector "Ordenar por" |
| Pila (LIFO) | `pilas.py` | Deshacer eliminación |
| Cola (FIFO) | `prestamos.py` | Solicitudes de préstamo |

## Cómo ejecutar
1. Crear el entorno virtual e instalar dependencias:
   python -m venv .venv
   .venv\Scripts\python.exe -m pip install -r requirements.txt
2. Iniciar la página:
   .venv\Scripts\python.exe app.py
3. Abrir http://127.0.0.1:5000 en el navegador.

## Pruebas
   .venv\Scripts\python.exe pruebas.py

## Análisis de eficiencia
- Simulación paso a paso: `python analisis\simulacion.py`
- Medición de tiempos: `python analisis\medicion.py entorno1`
- Resultados e informe: carpeta `analisis/`

import random
from itertools import permutations
import tkinter as tk

# Definimos las ciudades (nodos del grafo)
ciudades = ['A', 'B', 'C', 'D', 'E', 'F']
cantciudades = len(ciudades) #nodos

# Matriz de costos del grafo (pesos los arcos)
matrizcostos = [
    # A   B   C   D   E   F
    [ 0, 15,  0,  8,  0, 12],  # A
    [15,  0, 13,  7,  9, 13],  # B
    [ 0, 13,  0,  0,  9, 16],  # C
    [ 8,  7,  0,  0,  8,  7],  # D
    [ 0,  9,  9,  8,  0,  7],  # E
    [12, 13, 16,  7,  7,  0]   # F
]

# Función para calcular el costo total de una ruta
def CalcularCostos(ruta):
    costototal = 0
    for i in range(len(ruta) - 1):
        costo = matrizcostos[ruta[i]][ruta[i + 1]]
        if costo == 0:
            return float('inf')  # No hay conexión
        costototal += costo

    # Agregar costo de regreso al inicio
    retorno = matrizcostos[ruta[-1]][ruta[0]]
    if retorno == 0:
        return float('inf')
    costototal += retorno
    return costototal

# Generar vecinos invirtiendo segmentos de la ruta
def ObtenerVecinos(camino):
    vecinos = []
    n = len(camino)
    for inicio in range(1, n - 2):
        for fin in range(inicio + 1, n - 1):
            # Invertimos el segmento desde inicio hasta fin
            segmento = camino[inicio:fin + 1]
            invertido = list(reversed(segmento))
            nuevo_camino = camino[:inicio] + invertido + camino[fin + 1:]
            vecinos.append((inicio, fin, nuevo_camino))
    return vecinos

# Crear una ruta inicial completamente válida (todas las conexiones existen)
def CrearRutaInicial():
    for secuencia in permutations(range(cantciudades)):
        conexiones_ok = all(matrizcostos[secuencia[i]][secuencia[i + 1]] > 0 for i in range(cantciudades - 1))
        retorno_ok = matrizcostos[secuencia[-1]][secuencia[0]] > 0
        if conexiones_ok and retorno_ok:
            return list(secuencia)
    return None


def BusquedaTabu(cadena_base, max_pasos=100):
    actual = cadena_base[:]
    mejorcamino = actual[:]
    menorcosto = CalcularCostos(actual)

    memoriatabu = []
    sinnovedad = 0
    paso = 0
    resultados = [("Paso", "Camino", "Costo")]

    while paso < max_pasos and sinnovedad < 3:
        alternativas = ObtenerVecinos(actual)
        topvecino = None
        topcosto = float('inf')
        movrestringido = None

        for (i, j, posible) in alternativas:
            # Verificar si el movimiento está en la lista tabú
            arcos_eliminados = ((actual[i - 1], actual[i]), (actual[j], actual[j + 1]))
            if arcos_eliminados in memoriatabu:
                continue

            costo = CalcularCostos(posible)
            if costo == float('inf'):
                continue

            if costo < topcosto:
                topcosto = costo
                topvecino = posible
                movrestringido = arcos_eliminados

        if topvecino is None:
            break  # No hay vecinos válidos

        actual = topvecino[:]
        if topcosto < menorcosto:
            mejorcamino = topvecino[:]
            menorcosto = topcosto
            sinnovedad = 0
        else:
            sinnovedad += 1

        memoriatabu.append(movrestringido)
        if len(memoriatabu) > 4:
            memoriatabu.pop(0)

        paso += 1
        texto_camino = '-'.join([ciudades[i] for i in actual])
        resultados.append((paso, texto_camino, topcosto))

    camino_final = [ciudades[i] for i in mejorcamino]
    return camino_final, menorcosto, resultados

# Clase para mostrar tabla en Tkinter
class Tabla:
    def __init__(self, ventana, datos):
        self.ventana = ventana
        self.datos = datos
        filas = len(datos)
        columnas = len(datos[0]) if filas > 0 else 0

        for i in range(filas):
            for j in range(columnas):
                # Crear cada celda
                celda = tk.Entry(ventana, width=20, fg='black', font=('Arial', 12))
                celda.grid(row=i, column=j)
                celda.insert(tk.END, str(datos[i][j]))

# Crear ruta inicial válida
inicio = CrearRutaInicial()
if not inicio:
    print("No fue posible construir una ruta válida.")
    exit()

# Ejecutar búsqueda tabú
mejorcamino, costooptimo, resultados = BusquedaTabu(inicio)

# Mostrar resultados en ventana Tkinter
ventana = tk.Tk()
ventana.title("Resultado de Búsqueda Tabú - Problema del Agente Viajero")

tabla = Tabla(ventana, resultados)

# Mostrar resumen con el mejor camino encontrado
texto_resumen = "Camino óptimo: " + '-'.join(mejorcamino) + "\nCosto total: " + str(costooptimo)
etiqueta_resumen = tk.Label(ventana, text=texto_resumen, font=('Arial', 12, 'bold'), fg='blue', pady=10)
etiqueta_resumen.grid(row=len(resultados) + 1, column=0, columnspan=3)

ventana.mainloop()


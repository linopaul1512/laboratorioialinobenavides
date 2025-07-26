import random
import math
import tkinter as tk

# Lista de ciudades
ciudades = ['A', 'B', 'C', 'D', 'E', 'F']
cantciudades = len(ciudades) #nodos

# Matriz de costos
matrizcostos = [
    # A   B   C   D   E   F
    [ 0, 15,  0,  8,  0, 12],  # A
    [15,  0, 13,  7,  9,  7],  # B
    [ 0, 13,  0,  0,  9, 16],  # C
    [ 8,  7,  0,  0,  8,  7],  # D
    [ 0,  9,  9,  8,  0,  7],  # E
    [12,  7, 16,  7,  7,  0]   # F
]
 
def CalcularCosto(ruta):
    costototal = 0
    for i in range(len(ruta) - 1):
        costo = matrizcostos[ruta[i]][ruta[i + 1]]
        if costo == 0:
            return float('inf')
        costototal += costo
    retorno = matrizcostos[ruta[-1]][ruta[0]]
    if retorno == 0:
        return float('inf')
    return costototal + retorno

def RutaInicialValida():
    from itertools import permutations
    for perm in permutations(range(cantciudades)):
        if CalcularCosto(perm) != float('inf'):
            return list(perm)
    return None

def EscogerIndicesPorRuleta(nodosdisponibles):
    prob = 1 / len(nodosdisponibles)
    ruleta = []
    acumulado = 0
    for nodo in nodosdisponibles:
        ruleta.append((acumulado, acumulado + prob, nodo))
        acumulado += prob
    r = random.random()
    for (ini, fin, nodo) in ruleta:
        if ini <= r < fin:
            return nodo
    return nodosdisponibles[-1]

def ObtenerVecino(ruta):
    for intento in range(10):
        nodosvalidos = ruta[1:-1]
        nodoini = EscogerIndicesPorRuleta(nodosvalidos)
        idxini = ruta.index(nodoini)

        posiblesfinales = ruta[idxini + 1:-1]
        if not posiblesfinales:
            continue
        nodo_fin = EscogerIndicesPorRuleta(posiblesfinales)
        idx_fin = ruta.index(nodo_fin)

        if idxini >= idx_fin:
            continue

        subruta = ruta[idxini:idx_fin + 1][::-1]
        nueva = ruta[:idxini] + subruta + ruta[idx_fin + 1:]

        if nueva != ruta and CalcularCosto(nueva) != float('inf'):
            return nueva
    return ruta

# Algoritmo de Recocido Simulado
def RecocidoSimulado():
    rutaactual = RutaInicialValida()
    if rutaactual is None:
        print("No se encontró una ruta inicial válida.")
        return [], float('inf'), []

    zc = CalcularCosto(rutaactual)
    mejorruta = rutaactual[:]
    mejorcosto = zc

    t1 = 0.2 * zc
    T = [t1]
    for _ in range(4):
        T.append(0.5 * T[-1])

    resultados = [("Iteración", "Ruta actual", "Costo", "T", "Δ", "Prob. aceptación", "r", "Acción")]

    for i, temp in enumerate(T):
        vecino = ObtenerVecino(rutaactual)
        zn = CalcularCosto(vecino)

        delta = zc - zn
        probacept = round(math.exp(delta / temp), 3) if delta < 0 else 1.0
        r = round(random.random(), 3)
        accion = ""

        if zn < zc:
            accion = "Mejor vecino"
            rutaactual = vecino
            zc = zn
            if zn < mejorcosto:
                mejorruta = vecino
                mejorcosto = zn
        else:
            if r < probacept:
                accion = "Acepta peor"
                rutaactual = vecino
                zc = zn
            else:
                accion = "Rechaza"

        resultados.append((
            i + 1,
            '-'.join([ciudades[j] for j in rutaactual]),
            zc,
            round(temp, 2),
            round(delta, 2),
            probacept,
            r, #random
            accion
        ))

    return [ciudades[i] for i in mejorruta], mejorcosto, resultados

# Tkinter: tabla de resultados
class Tabla:
    def __init__(self, ventana, datos):
        self.filas = len(datos)
        self.columnas = len(datos[0]) if self.filas > 0 else 0

        for i in range(self.filas):
            for j in range(self.columnas):
                e = tk.Entry(ventana, width=18, fg='black',
                             font=('Arial', 10))
                e.grid(row=i, column=j)
                e.insert(tk.END, str(datos[i][j]))


mejorruta, mejorcosto, datos_tabla = RecocidoSimulado()

# Interfaz
ventana = tk.Tk()
ventana.title("Recocido Simulado - Agente Viajero")

tabla = Tabla(ventana, datos_tabla)

etiqueta = tk.Label(
    ventana,
    text=f"\nMejor ruta: {'-'.join(mejorruta)}\nCosto total: {mejorcosto}",
    font=('Arial', 12, 'bold'),
    fg='blue'
)
etiqueta.grid(row=len(datos_tabla) + 1, column=0, columnspan=8)

ventana.mainloop()
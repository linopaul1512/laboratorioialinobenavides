import random
import math

# Lista de ciudades o nodos
ciudades = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
cantciudades = len(ciudades)

# Matriz de costos
matrizcostos = [
    [0, 12, 0, 10, 0, 12, 0],
    [12, 0, 12, 8, 0, 0, 0],
    [0, 12, 0, 11, 11, 0, 10],
    [10, 8, 11, 0, 3, 9, 0],
    [0, 0, 11, 3, 0, 7, 6],
    [12, 0, 0, 9, 7, 0, 9],
    [0, 0, 10, 0, 6, 9, 0]
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

# Escoge nodo inicial y final usando ruleta
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
    for intento in range(10):  # Hasta 10 intentos para generar un vecino distinto
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

        subruta = ruta[idxini:idx_fin + 1]
        subruta_invertida = subruta[::-1]

        nueva = ruta[:idxini] + subruta_invertida + ruta[idx_fin + 1:]

        if nueva != ruta and CalcularCosto(nueva) != float('inf'):
            return nueva
    return ruta 

def Recocido():
    rutaactual = RutaInicialValida()
    if rutaactual is None:
        print("No se encontró una ruta inicial válida.")
        return

    zc = CalcularCosto(rutaactual)
    mejorruta = rutaactual[:]
    mejorcosto = zc

    # Temperaturas
    t1 = 0.2 * zc
    T = [t1]
    for _ in range(4):
        T.append(0.5 * T[-1])

    print("*** Ruta inicial:", [ciudades[i] for i in rutaactual], "Costo:", zc)
        
    for i, temp in enumerate(T):
        print(f"\n*** Iteración {i + 1} con T = {round(temp, 2)}")
        vecino = ObtenerVecino(rutaactual)
        zn = CalcularCosto(vecino)

        print("*** Ruta candidata:", [ciudades[i] for i in vecino], "Costo:", zn)

        if zn < zc:
            print("*** Mejor vecino encontrado (mejor costo):", zn)
            rutaactual = vecino
            zc = zn
            if zn < mejorcosto:
                mejorruta = vecino
                mejorcosto = zn
        else:
            delta = zc - zn
            probacept = math.exp(delta / temp)
            r = random.random()
            print(f" Zn > Zc. Δ={delta:.2f}, Probabilidad de aceptación={round(probacept, 3)}, r={round(r, 3)}")
            if r < probacept:
                print(" *** Se acepta solución peor por probabilidad. ***")
                ruta_actual = vecino
                zc = zn
            else:
                print(" *** Rechazada. Se mantiene la anterior. ***")

        print("*** Ruta actual:", [ciudades[i] for i in ruta_actual], "Costo:", zc)

    print("\n*** Mejor ruta encontrada:", [ciudades[i] for i in mejorruta])
    print("*** Costo total:", mejorcosto)

solucion = Recocido()
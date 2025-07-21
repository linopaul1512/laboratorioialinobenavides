import random
import pandas as pd

# Parámetros
nreinas = 4
tampoblacion = 6
nmax = 5
probmutacion = 0.1

# Generar individuo aleatoriamente como permutación
def GenerarIndividuo():
    ind = list(range(1, nreinas + 1))
    random.shuffle(ind)
    return ind

# Calcular colisiones diagonales (fitness)
def CalcularFitness(ind):
    colisiones = 0
    for i in range(len(ind)):
        for j in range(i + 1, len(ind)):
            if abs(ind[i] - ind[j]) == abs(i - j):
                colisiones += 1
    return colisiones

# Selección por ruleta con impresión didáctica del número aleatorio
def SeleccionRuleta(poblacion, fitnesses):
    invfitness = [1 / (f + 1) for f in fitnesses]
    total = sum(invfitness)
    probs = [f / total for f in invfitness]
    probacum = []
    acum = 0
    for p in probs:
        acum += p
        probacum.append(acum)

    r = random.random()
    print(f"  → Número aleatorio r = {round(r, 3)}")

    for i, p in enumerate(probacum):
        if r < p:
            print(f"  → Individuo seleccionado: {poblacion[i]} (índice {i})")
            return poblacion[i]

    print("  → Selección por defecto: último individuo")
    return poblacion[-1]

# Cruce alternado sin repetición
def Cruzar(p1, p2):
    def crear_hijo(orden):
        hijo, usados = [], set()
        for gen in orden:
            if gen not in usados:
                hijo.append(gen)
                usados.add(gen)
        return hijo

    orden_h1 = [p1[0], p2[0], p1[1], p2[1], p1[2], p2[2], p1[3], p2[3]]
    orden_h2 = [p2[0], p1[0], p2[1], p1[1], p1[2], p2[2], p1[3], p2[3]]
    return crear_hijo(orden_h1), crear_hijo(orden_h2)

# Mutación por intercambio de dos posiciones
def Mutar(ind):
    a, b = random.sample(range(nreinas), 2)
    original = ind.copy()
    ind[a], ind[b] = ind[b], ind[a]
    print(f"Mutación aplicada: {original} → {ind} (índices intercambiados: {a}, {b})")
    return ind

# Imprimir el tablero de ajedrez de un individuo
def ImprimirTablero(individuo):
    N = len(individuo)
    for fila in range(1, N + 1):
        linea = ""
        for col in range(1, N + 1):
            if individuo[col - 1] == fila:
                linea += "♕ "
            else:
                linea += ". "
        print(linea)
    print()

# Algoritmo genético principal
def AlgoritmoGeneticoNReinas():
    poblacion = [GenerarIndividuo() for _ in range(tampoblacion)]

    print("\n Población inicial (posiciones de las reinas):")
    tablainicial = pd.DataFrame(poblacion, columns=[f"R{i+1}" for i in range(nreinas)])
    print(tablainicial)

    print("\n Tableros de ajedrez de la población inicial:")
    for i, ind in enumerate(poblacion):
        print(f"Individuo {i + 1}: {ind}")
        ImprimirTablero(ind)

    for generacion in range(nreinas):
        print(f"\n***************Generación {generacion} *************")
        fitnesses = [CalcularFitness(ind) for ind in poblacion]

        # Mostrar tabla con fitness y ruleta
        tabla = pd.DataFrame(poblacion, columns=[f"R{i+1}" for i in range(nreinas)])
        tabla["Fitness"] = fitnesses
        invfit = [1 / (f + 1) for f in fitnesses]
        totalinv = sum(invfit)
        tabla["Prob"] = [round(f / totalinv, 3) for f in invfit]
        tabla["Prob Acum"] = tabla["Prob"].cumsum().round(3)
        print(tabla)

        # Verificar si hay solución perfecta (fitness 0)
        if 0 in fitnesses:
            solucion = poblacion[fitnesses.index(0)]
            print("\n ¡Solución encontrada!", solucion)
            print("\n Tablero de la solución:")
            ImprimirTablero(solucion)
            return solucion

        nuevapoblacion = []

        while len(nuevapoblacion) < tampoblacion:
            randomIII = random.random()
            print(f"randomIII: {randomIII}")
            if randomIII < probmutacion:
                # MUTACIÓN
                padre = SeleccionRuleta(poblacion, fitnesses)
                hijo = Mutar(padre.copy())
                nuevapoblacion.append(hijo)
            else:
                # CRUCE
                padre1 = SeleccionRuleta(poblacion, fitnesses)
                padre2 = SeleccionRuleta(poblacion, fitnesses)
                hijo1, hijo2 = Cruzar(padre1, padre2)
                print(f"Cruce aplicado: {padre1} + {padre2} → {hijo1}, {hijo2}")
                nuevapoblacion.append(hijo1)
                if len(nuevapoblacion) < tampoblacion:
                    nuevapoblacion.append(hijo2)


        poblacion = nuevapoblacion

    print("\n No se encontró solución en Nmax generaciones.")
    return None

solucion = AlgoritmoGeneticoNReinas()
print("\n  Solución final:", solucion)
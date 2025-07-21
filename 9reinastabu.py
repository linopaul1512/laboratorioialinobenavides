import random
import tkinter as tk

nreinas = 4
nmax = 6
tamtabu = 2

# Generar solución inicial válida
def GenerarIndividuo():
    ind = list(range(1, nreinas + 1))
    random.shuffle(ind)
    return ind

# Fitness: colisiones diagonales
def CalcularFitness(ind):
    colisiones = 0
    for i in range(len(ind)):
        for j in range(i + 1, len(ind)):
            if abs(ind[i] - ind[j]) == abs(i - j):
                colisiones += 1
    return colisiones

# Imprimir tablero
def ImprimirTablero(ind):
    for fila in range(1, nreinas + 1):
        linea = ""
        for col in range(1, nreinas + 1):
            if ind[col - 1] == fila:
                linea += "♕ "
            else:
                linea += ". "
        print(linea)
    print()

# Generar todos los vecinos (intercambios de 2 posiciones)
def GenerarVecindario(solucion_actual):
    vecinos = []
    for i in range(nreinas):
        for j in range(i + 1, nreinas):
            vecino = solucion_actual.copy()
            vecino[i], vecino[j] = vecino[j], vecino[i]
            vecinos.append((vecino, (i, j)))
    return vecinos

# Algoritmo búsqueda tabú
def BusquedaTabu():
    actual = GenerarIndividuo()
    mejorsol = actual
    mejorfit = CalcularFitness(actual)
    tabu = []

    print("\n Solución inicial:", actual)
    ImprimirTablero(actual)

    # Para la tabla
    resultados = [("Iteración", "Movimiento", "Solución", "Colisiones")]

    for iteracion in range(nmax):
        print(f"*************** Iteración {iteracion}**************")
        vecinos = GenerarVecindario(actual)
        candidatos = []

        for vecino, movimiento in vecinos:
            fit = CalcularFitness(vecino)
            if movimiento not in tabu:
                candidatos.append((vecino, fit, movimiento))

        if not candidatos:
            print(" Todos los movimientos están en la lista tabú. Se selecciona al azar.")
            vecino, fit, movimiento = random.choice(vecinos)
        else:
            vecino, fit, movimiento = min(candidatos, key=lambda x: x[1])

        print(f"Mejor movimiento: intercambio {movimiento}, fitness = {fit}")
        print(f"Nueva solución: {vecino}")
        ImprimirTablero(vecino)

        actual = vecino
        tabu.append(movimiento)
        if len(tabu) > tamtabu:
            tabu.pop(0)

        if fit < mejorfit:
            mejorfit = fit
            mejorsol = vecino

        # Guardar resultado para tabla
        resultados.append((iteracion, str(movimiento), str(vecino), fit))

    print("\nBúsqueda finalizada.")
    print("Mejor solución encontrada:", mejorsol, "con", mejorfit, "colisiones")
    ImprimirTablero(mejorsol)

    return mejorsol, mejorfit, resultados

# Mostrar tabla Tkinter
def MostrarTabla(resultados, mejorfit, mejor):
    ventana = tk.Tk()
    ventana.title("Resultados Búsqueda Tabú - N Reinas")

    for i, fila in enumerate(resultados):
        for j, valor in enumerate(fila):
            entrada = tk.Entry(ventana, width=20, fg='black', font=('Arial', 12))
            entrada.grid(row=i, column=j)
            entrada.insert(tk.END, str(valor))

    resumen = tk.Label(
        ventana,
        text=f"\nMejor solución: {mejor}\nColisiones: {mejorfit}",
        font=('Arial', 12, 'bold'), fg='blue', pady=10
    )
    resumen.grid(row=len(resultados) + 1, column=0, columnspan=4)

    ventana.mainloop()

# Ejecutar
solucion, fitness, resultados = BusquedaTabu()
MostrarTabla(resultados, fitness, solucion)

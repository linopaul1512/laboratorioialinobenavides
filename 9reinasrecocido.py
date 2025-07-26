import random
import math
import tkinter as tk
import sys

n = 9
nmax = 6  # Iteraciones por temperatura


sys.stdout = open("iteraciones_recocido_9reinas.txt", "w", encoding="utf-8")

# Generar una solución válida (permuta de 1 a 9)
def generarIndividuo():
    ind = list(range(1, n + 1))
    random.shuffle(ind)
    return ind

# Contar colisiones diagonales
def calcularColisiones(ind):
    colisiones = 0
    for i in range(len(ind)):
        for j in range(i + 1, len(ind)):
            if abs(ind[i] - ind[j]) == abs(i - j):
                colisiones += 1
    return colisiones

# Imprimir tablero visual
def imprimirTablero(sol):
    for fila in range(1, n + 1):
        linea = ""
        for col in range(1, n + 1):
            if sol[col - 1] == fila:
                linea += "♕ "
            else:
                linea += ". "
        print(linea)
    print()

# Algoritmo de recocido simulado
def recocidoSimulado():
    actual = generarIndividuo()
    zc = calcularColisiones(actual)
    mejor = actual[:]
    mejorZ = zc

    print("****** RECOSIDO SIMULADO - PROBLEMA DE LAS 9 REINAS ****\n")
    print("Solución inicial:", actual, "Colisiones:", zc)
    imprimirTablero(actual)

    # temperaturas
    T1 = 0.2 
    T2 = 0.5 
    T3 = 0.5
    T4 = 0.5 
    T5 = 0.5 
    temperaturas = [T1, T2, T3, T4, T5]

    for etapa, T in enumerate(temperaturas):
        print(f"************ ETAPA {etapa + 1} | Temperatura: {round(T, 4)} ************\n")
        for iter in range(nmax):
            vecino = actual[:]
            i, j = random.sample(range(n), 2)
            vecino[i], vecino[j] = vecino[j], vecino[i]

            zn = calcularColisiones(vecino)

            if zn < zc:
                actual = vecino
                zc = zn
                print(f"[Iteración {iter}] ACEPTADO DIRECTO → Zn = {zn} < Zc = {zc}")
            else:
                delta = zc - zn
                prob = math.exp(delta / T)
                r = random.random()

                print(f"[Iteración {iter}] Zn = {zn}, Zc = {zc}, Prob = {round(prob, 4)}, Rand = {round(r, 4)}")
                if r < prob:
                    actual = vecino
                    zc = zn
                    print("ACEPTADO por probabilidad\n")
                else:
                    print("RECHAZADO\n")

            if zc < mejorZ:
                mejor = actual[:]
                mejorZ = zc

            if mejorZ == 0:
                print("\n✓ Solución óptima encontrada en etapa", etapa + 1)
                break
        if mejorZ == 0:
            break

    print("*********** RESULTADO FINAL ***********")
    print(" Mejor solución encontrada:", mejor)
    print(f" Colisiones: {mejorZ}")
    imprimirTablero(mejor)
    return mejor, mejorZ

# Mostrar la mejor solución con interfaz gráfica
def mostrarTkinter(sol, colisiones):
    ventana = tk.Tk()
    ventana.title("Recocido Simulado - N Reinas")
    colores = ["white", "gray"]

    for fila in range(n):
        for col in range(n):
            color = colores[(fila + col) % 2]
            reina = "♕" if sol[col] == fila + 1 else ""
            etiqueta = tk.Label(
                ventana,
                text=reina,
                width=4,
                height=2,
                font=("Arial", 18),
                bg=color,
                fg="black" if reina else color,
                relief="ridge",
                borderwidth=1
            )
            etiqueta.grid(row=fila, column=col)

    resumen = tk.Label(
        ventana,
        text=f"Colisiones: {colisiones}",
        font=('Arial', 12, 'bold'),
        fg='blue',
        pady=10
    )
    resumen.grid(row=n, column=0, columnspan=n)
    ventana.mainloop()

# Ejecutar el algoritmo y mostrar tablero si es solución óptima
mejorSol, mejorCol = recocidoSimulado()
sys.stdout.close()  

if mejorCol == 0:
    mostrarTkinter(mejorSol, mejorCol)
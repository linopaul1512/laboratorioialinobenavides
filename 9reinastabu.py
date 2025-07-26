import random
import tkinter as tk
import sys

nreinas = 9 
nmax = 6
tamtabu = 2

# Redirigir salida a archivo de texto
sys.stdout = open("iteraciones_tabu_9reinas.txt", "w", encoding="utf-8")

# Generar solución inicial válida
def GenerarIndividuo():
    ind = list(range(1, nreinas + 1))  
    random.shuffle(ind)  #Se desordena para obtener una permutación aleatoria sin conflictos de fila ni columna
    return ind

# Fitness: colisiones diagonales
def CalcularFitness(ind):
    colisiones = 0
    for i in range(len(ind)):
        for j in range(i + 1, len(ind)):
            # si la distancia en fila = distancia en columna ... colisión diagonal
            if abs(ind[i] - ind[j]) == abs(i - j):
                colisiones += 1
    return colisiones  # colisiones en diagonal

# Imprimir tablero visual
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
            # genera vecino intercambiando posiciones (columnas)
            vecino[i], vecino[j] = vecino[j], vecino[i] 
            vecinos.append((vecino, (i, j)))            
    return vecinos

# Algoritmo de búsqueda tabú
def BusquedaTabu():
    # estado inicial aleatorio en el espacio de soluciones
    actual = GenerarIndividuo()                   
    mejorsol = actual
    # Se evalúa el número de colisiones iniciales
    mejorfit = CalcularFitness(actual)          
    # vector de tabú
    tabu = []                                      

    print("\n Solución inicial:", actual)
    ImprimirTablero(actual)

    resultados = [("Iteración", "Movimiento", "Solución", "Colisiones")]

    for iteracion in range(nmax):
        print(f"*************** Iteración {iteracion} ***************")
        # Se generan todos los vecinos por movimiento válido
        vecinos = GenerarVecindario(actual)   
        candidatos = []

        for vecino, movimiento in vecinos:
            fit = CalcularFitness(vecino)
            if movimiento not in tabu:    # movimiento no prohibido por la lista tabú
                candidatos.append((vecino, fit, movimiento))

        if not candidatos:
            print(" Todos los movimientos están en la lista tabú. Se selecciona al azar.")
            vecino, fit, movimiento = random.choice(vecinos)  # Escape si no hay movimiento disponible
        else:
            # Se elige el vecino con menor número de colisiones
            vecino, fit, movimiento = min(candidatos, key=lambda x: x[1])

        print(f"Mejor movimiento: intercambio {movimiento}, fitness = {fit}")
        print(f"Nueva solución: {vecino}")
        ImprimirTablero(vecino)

        actual = vecino
        # Se agrega el movimiento a la lista tabú 
        tabu.append(movimiento)                      
        if len(tabu) > tamtabu: 
            # Se mantiene el tamaño fijo de la lista tabú
            tabu.pop(0)                           

        # Si se mejora el fitness, se actualiza la mejor solución
        if fit < mejorfit:                           
            mejorfit = fit
            mejorsol = vecino

        resultados.append((iteracion, str(movimiento), str(vecino), fit))

        if mejorfit == 0:
            break

    print("\nBúsqueda finalizada.")
    print("Mejor solución encontrada:", mejorsol, "con", mejorfit, "colisiones")
    ImprimirTablero(mejorsol)

    return mejorsol, mejorfit, resultados



mejorsolucion, mejor_fit, resultados = BusquedaTabu()

sys.stdout.close()

# Tablero con tinker
def MostrarTableroTkinter(solucion):
    ventana = tk.Tk()
    ventana.title("Tablero de N Reinas - Mejor Solución")
    
    colores = ["white", "gray"]

    for fila in range(nreinas):
        for col in range(nreinas):
            color = colores[(fila + col) % 2]
            reina = "♕" if solucion[col] == fila + 1 else ""
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
        text=f"Colisiones: {mejor_fit}",
        font=('Arial', 12, 'bold'),
        fg='blue',
        pady=10
    )
    resumen.grid(row=nreinas, column=0, columnspan=nreinas)
    ventana.mainloop()

MostrarTableroTkinter(mejorsolucion)

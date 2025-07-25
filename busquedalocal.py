import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

# f(x) = x⁴ - 4x³ + 7x
def funcionObjetivo(x):
    return x**4 - 4*x**3 + 7*x

# Función para centrar una ventana tkinter
def centrarVentana(ventana, ancho, alto):
    pantallaAncho = ventana.winfo_screenwidth()
    pantallaAlto = ventana.winfo_screenheight()
    x = (pantallaAncho // 2) - (ancho // 2)
    y = (pantallaAlto // 2) - (alto // 2)
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

#Función principal: interfaz de búsqueda local
def interfazBusquedaLocal():
    ventana = tk.Tk()
    ventana.title("Búsqueda Local - f(x)")
    ventana.configure(bg="white")
    centrarVentana(ventana, 750, 650)

    #Entrada: valor inicial x0
    tk.Label(ventana, text="Ingrese x₀ (entre -2 y 4):", bg="white", font=("Arial", 12)).pack(pady=5)
    entradaX0 = tk.Entry(ventana, font=("Arial", 12))
    entradaX0.pack(pady=5)

    # Entrada: delta (pequeño desplazamiento)
    tk.Label(ventana, text="Ingrese delta (> 0):", bg="white", font=("Arial", 12)).pack(pady=5)
    entradaDelta = tk.Entry(ventana, font=("Arial", 12))
    entradaDelta.pack(pady=5)

    #Tipo de búsqueda: mínimo o máximo
    tipoBusqueda = tk.StringVar(value="min")
    frameTipo = tk.Frame(ventana, bg="white")
    tk.Label(frameTipo, text="Buscar:", font=("Arial", 12), bg="white").pack(side="left", padx=10)
    tk.Radiobutton(frameTipo, text="Mínimo", variable=tipoBusqueda, value="min", bg="white").pack(side="left")
    tk.Radiobutton(frameTipo, text="Máximo", variable=tipoBusqueda, value="max", bg="white").pack(side="left")
    frameTipo.pack(pady=10)

    def EjecutarBusqueda():
        try:
            x = float(entradaX0.get())
            delta = float(entradaDelta.get())

            if not (-2 <= x <= 4) or delta <= 0:
                raise ValueError

            intervalo = (-2, 4)
            iterMax = 50
            modoMinimo = tipoBusqueda.get() == "min"
            trayectoria = [x]

            for _ in range(iterMax):
                # Cálculo de vecinos izquierdo y derecho
                xIzq = max(intervalo[0], x - delta)
                xDer = min(intervalo[1], x + delta)

                fx = funcionObjetivo(x)
                fxIzq = funcionObjetivo(xIzq)
                fxDer = funcionObjetivo(xDer)

                #comparar valores vecinos
                if modoMinimo:
                    if fxIzq < fx and fxIzq < fxDer:
                        x = xIzq
                    elif fxDer < fx:
                        x = xDer
                    else:
                        break 
                else:
                    if fxIzq > fx and fxIzq > fxDer:
                        x = xIzq
                    elif fxDer > fx:
                        x = xDer
                    else:
                        break

                trayectoria.append(x)

        
            xRango = np.linspace(intervalo[0], intervalo[1], 400)
            yRango = funcionObjetivo(xRango)

            #Interfaz de tinker
            fig, ax = plt.subplots(figsize=(6, 4))
            ax.plot(xRango, yRango, color="gray", label="f(x)")
            ax.set_title("Trayectoria de búsqueda", fontsize=12)
            ax.set_xlabel("x")
            ax.set_ylabel("f(x)")
            ax.grid(True)

            xHist = np.array(trayectoria)
            yHist = funcionObjetivo(xHist)
            ax.plot(xHist, yHist, 'ro--', label="Pasos")

            xOpt = xHist[-1]
            yOpt = yHist[-1]
            ax.plot(xOpt, yOpt, 'go', label=f"Óptimo: x = {xOpt:.4f}")
            ax.legend()

            canvas = FigureCanvasTkAgg(fig, master=ventana)
            canvas.draw()
            canvas.get_tk_widget().pack(pady=10)

            tipo = "mínimo" if modoMinimo else "máximo"
            messagebox.showinfo("Resultado", f"Se encontró el {tipo}:\nx = {xOpt:.4f}\nf(x) = {yOpt:.4f}")

        except:
            messagebox.showerror("Error", "Verificar datos")

    tk.Button(ventana, text="Ejecutar búsqueda", font=("Arial", 12, "bold"), command=EjecutarBusqueda, bg="#cccccc").pack(pady=10)

    ventana.mainloop()

interfazBusquedaLocal()

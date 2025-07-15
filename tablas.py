import tkinter as tk

class Tabla:
    def __init__(self, ventana, datos):
        self.ventana = ventana
        self.datos = datos
        self.filas = len(datos)
        self.columnas = len(datos[0]) if self.filas > 0 else 0

        for i in range(self.filas):
            for j in range(self.columnas):
                self.e = tk.Entry(ventana, width=20, fg='blue',
                                 font=('Arial',16,'bold'))
                self.e.grid(row=i, column=j)
                self.e.insert(tk.END, datos[i][j])

ventana = tk.Tk()
ventana.title("Tabla en Tkinter")

# Datos de ejemplo
datos_tabla = [
    ("ID", "Nombre", "Ciudad"),
    (1, "Juan", "Caracas"),
    (2, "Maria", "Maracay"),
    (3, "Pedro", "Valencia")
]

tabla = Tabla(ventana, datos_tabla)
ventana.mainloop()
import numpy as np


def EncontrarMinimoLocal(funcion, limiteizq, limiteder, pasos):
    # Generar puntos equidistantes en el rango especificado
    puntos = np.linspace(limiteizq, limiteder, pasos + 1)
    
    # Evaluar la función en cada punto
    resultados = [funcion(p) for p in puntos]
    
    # Determinar la posición del menor valor
    posmin = np.argmin(resultados)
    
    # Recuperar x y f(x) correspondientes al mínimo encontrado
    mejorx = puntos[posmin]
    mejorfx = resultados[posmin]
    
    return mejorx, mejorfx

# Definir la función que se desea minimizar
def EvaluarFuncionObjetivo(x):

    return x**4 - 4 * x**3 + 7* x
    #función f(x)=x4-4x3+7x 


# Establecer los límites del dominio y la cantidad de particiones
iniciointervalo = -2
finintervalo = 4
divisiones = 100

# Ejecutar la búsqueda del valor mínimo
puntooptimo, valorminimo = EncontrarMinimoLocal(EvaluarFuncionObjetivo, iniciointervalo, finintervalo, divisiones)

# Mostrar resultados obtenidos
print(f"El mínimo estimado está en x = {puntooptimo}, con f(x) = {valorminimo}")
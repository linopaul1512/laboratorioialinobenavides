import random
import pandas as pd

# Parámetros del Algoritmo genético
poblaciontamano = 10    # tamaño de población
generaciones = 20       # número de generaciones
tasa_mut = 0.1          # probabilidad de mutación

def binario_nbits(n, bits=5):
    if n < 0:
        n = (1 << bits) + n  # Representación en complemento a dos
    return f"{n:0{bits}b}"

def decodificar(binario):
    n = int(binario, 2)
    if binario[0] == '1':  # Bit de signo en complemento a dos
        n -= 1 << len(binario)
    return n

def mutar_binario(binario):
    idx = random.randrange(len(binario))
    lista = list(binario)
    lista[idx] = '1' if lista[idx] == '0' else '0'
    return ''.join(lista), idx

def cruzar_binario(p, m):
    punto = random.randrange(1, len(p) - 1)  # Corte entre 1 y 3 (evita extremos)
    h1 = p[:punto] + m[punto:]
    h2 = m[:punto] + p[punto:]
    return h1, h2, punto

def algoritmo_genetico():
    # 1) Inicializar población aleatoria [-1, 5]
    bits = 5
    poblacion = [random.randint(-1, 5) for _ in range(poblaciontamano)]


    for gen in range(1, generaciones + 1):
        print(f"\n==== Generación {gen} ====")

        #Evaluar fitness
        fitness_vals = [x**3 - 2*x + 3 for x in poblacion]
        total_f = sum(fitness_vals)

        #Calcular probabilidades individuales y acumuladas
        probs = [f / total_f if total_f > 0 else 0 for f in fitness_vals]
        probsacum = []
        acum = 0

        for p in probs:
            acum += p
            probsacum.append(acum)

        #Mostrar tabla con pandas
        df = pd.DataFrame({
            'Valor': poblacion,
            'Fitness': fitness_vals,
            'P_ind': [round(p, 5) for p in probs],
            'P_acum': [round(p, 5) for p in probsacum],
        })
        print(df)

        #Generar nueva población
        nueva = []
        while len(nueva) < poblaciontamano:
            # Selección por ruleta
            r1 = random.random()
            i1 = next(i for i, p in enumerate(probsacum) if r1 <= p)
            padre = poblacion[i1]
            pad_bin = binario_nbits(padre, bits)

            # Asegurar que madre sea distinta del padre
            while True:
                r2 = random.random()
                i2 = next(i for i, p in enumerate(probsacum) if r2 <= p)
                if i2 != i1:
                    break

            madre = poblacion[i2]
            mad_bin = binario_nbits(madre, bits)

            if random.random() < tasa_mut:
                # MUTACIÓN
                hijo_bin, bit = mutar_binario(pad_bin)
                hijo = decodificar(hijo_bin)
                print(f"Mutación: padre={padre} ({pad_bin}), bit invertido={bit} -> hijo={hijo} ({hijo_bin})")

                if -1 <= hijo <= 5:
                    nueva.append(hijo)
                else:
                    nueva.append(random.randint(-1, 5))
            else:
                # CRUCE
                h1_bin, h2_bin, pt = cruzar_binario(pad_bin, mad_bin)
                hijo1 = decodificar(h1_bin)
                hijo2 = decodificar(h2_bin)
                print(f"Cruce pto={pt}: {padre} ({pad_bin}) × {madre} ({mad_bin}) -> hijo1={hijo1} ({h1_bin}), hijo2={hijo2} ({h2_bin})")

                for hijo in (hijo1, hijo2):
                    if len(nueva) < poblaciontamano:
                        if -1 <= hijo <= 5:
                            nueva.append(hijo)
                        else:
                            nueva.append(random.randint(-1, 5))

        #Reemplazar población
        poblacion = nueva

if __name__ == "__main__":
    algoritmo_genetico()
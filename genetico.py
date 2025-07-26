import random
import pandas as pd
import sys

# Parámetros del Algoritmo Genético
poblaciontamano = 40
generaciones = 1000
tasa_mut = 0.1
bits = 6  # Permite representar valores entre -32 y 31 (suficiente para [-2, 4])

# Redirigir salida a archivo de texto
sys.stdout = open("genetico_funcion_x4.txt", "w", encoding="utf-8")

# Codificación binaria en complemento a dos
def BinarioNbits(n, bits=6):
    if n < 0:
        n = (1 << bits) + n
    return f"{n:0{bits}b}"

def Decodificar(binario):
    n = int(binario, 2)
    if binario[0] == '1':
        n -= 1 << len(binario)
    return n

def MutarBinario(binario):
    idx = random.randrange(len(binario))
    lista = list(binario)
    lista[idx] = '1' if lista[idx] == '0' else '0'
    return ''.join(lista), idx

def CruzarBinario(p, m):
    punto = random.randrange(1, len(p) - 1)
    h1 = p[:punto] + m[punto:]
    h2 = m[:punto] + p[punto:]
    return h1, h2, punto

def Fitness(x):
    return x**4 - 4*x**3 + 7*x

def AlgoritmoGenetico():
    # 1) Inicializar población aleatoria en [-2, 4]
    poblacion = [random.randint(-2, 4) for _ in range(poblaciontamano)]

    for gen in range(1, generaciones + 1):
        print(f"\n==== Generación {gen} ====")

        fitness_vals = [Fitness(x) for x in poblacion]
        total_f = sum(fitness_vals)

        # Probabilidades y acumuladas
        probs = [f / total_f if total_f > 0 else 0 for f in fitness_vals]
        probsacum = []
        acum = 0
        for p in probs:
            acum += p
            probsacum.append(acum)

        df = pd.DataFrame({
            'Valor': poblacion,
            'Fitness': [round(f, 4) for f in fitness_vals],
            'P_ind': [round(p, 5) for p in probs],
            'P_acum': [round(p, 5) for p in probsacum],
        })
        print(df.to_string(index=False))

        nueva = []
        while len(nueva) < poblaciontamano:
            r1 = random.random()
            i1 = next(i for i, p in enumerate(probsacum) if r1 <= p)
            padre = poblacion[i1]
            pad_bin = BinarioNbits(padre, bits)

            while True:
                r2 = random.random()
                i2 = next(i for i, p in enumerate(probsacum) if r2 <= p)
                if i2 != i1:
                    break

            madre = poblacion[i2]
            mad_bin = BinarioNbits(madre, bits)

            if random.random() < tasa_mut:
                hijo_bin, bit = MutarBinario(pad_bin)
                hijo = Decodificar(hijo_bin)
                print(f"Mutación: padre={padre} ({pad_bin}), bit invertido={bit} -> hijo={hijo} ({hijo_bin})")
                if -2 <= hijo <= 4:
                    nueva.append(hijo)
                else:
                    nueva.append(random.randint(-2, 4))
            else:
                h1_bin, h2_bin, pt = CruzarBinario(pad_bin, mad_bin)
                hijo1 = Decodificar(h1_bin)
                hijo2 = Decodificar(h2_bin)
                print(f"Cruce pto={pt}: {padre} ({pad_bin}) × {madre} ({mad_bin}) -> hijo1={hijo1} ({h1_bin}), hijo2={hijo2} ({h2_bin})")
                for hijo in (hijo1, hijo2):
                    if len(nueva) < poblaciontamano:
                        if -2 <= hijo <= 4:
                            nueva.append(hijo)
                        else:
                            nueva.append(random.randint(-2, 4))

        poblacion = nueva

if __name__ == "__main__":
    AlgoritmoGenetico()
    sys.stdout.close()

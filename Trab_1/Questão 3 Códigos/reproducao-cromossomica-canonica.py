import numpy as np
import matplotlib.pyplot as plt

T = 100  # número de iterações de reprodução/seleção (gerações)
N = 50   # número de indivíduos na população
nd = 12  # número de bits que representam cada dimensão
P = 20   # quantidade de dimensões (variáveis) de cada indivíduo
limits = [-10, 10]  
rep_tax, mut_tax = 0.85, 0.01  

#converte uma string binária (x) em um valor real no intervalo [inf, sup]
def binario(x, nd, inf, sup):
    s = 0
    for l in range(len(x)):
        s += x[nd-1-l] * 2**l
    return inf + (sup - inf) / (2**nd - 1) * s

def log(ind):
    return (np.log(10) / np.log(f(ind)))**30

#função de rastrigin
def f(x):
    A = 10
    soma = 0
    for i in range(P):
        start = nd * i
        final = start + nd
        #fazer a conversao de binario para um valor real dentro dos limites, pulando de acordo com a qntd de bits correspondente
        xi = binario(x[start:final], nd, *limits)
        soma += xi**2 - A * np.cos(2 * np.pi * xi)
    return A * P + soma + 1 # soma + 1 para  Ψ(x) = f(x) + 1

#calcula as aptidões (probabilidades) para cada indivíduo da população
def Aptabilities(pop):
    p = []
    s = 0
    for ind in pop:
        s += log(ind)
    for ind in pop:
        p.append(log(ind) / s)
    return np.array(p)

#seleção baseada em roleta
def Selection(pop, prob):
    s = []
    for _ in range(len(pop)):
        i = 0
        p = prob[i]
        r = np.random.uniform()
        while p < r:
            i += 1
            p += prob[i]
        s.append(pop[i])
    return np.array(s)

def Cruz_Mut(x1, x2):
    a1 = np.random.randint(0, 2, len(x1))
    a2 = list(zip(x1, x2))
    c1, c2 = [], []
    for i in range(len(a2)):
        c1.append(a2[i][a1[i]])
        c2.append(a2[i][not a1[i]])
    for i in range(len(a2)):
        rnd_1 = np.random.uniform()
        rnd_2 = np.random.uniform()
        if rnd_1 < mut_tax:
            c1[i] = not c1[i]
        if rnd_2 < mut_tax:
            c2[i] = not c2[i]
    return np.array(c1), np.array(c2)

def Reproduce(pop):
    p = []
    for i in range(0, len(pop), 2):
        if np.random.uniform() < rep_tax:
            c1, c2 = Cruz_Mut(pop[i], pop[i+1])
            p.extend([c1, c2])
        else:
            p.extend([pop[i], pop[i+1]])
    return np.array(p)


Pop = np.random.randint(0, 2, size=(N, nd * P)) #inicializa a população aleatória (binária) de N indivíduos, cada um com nd * P bits
Chamadas = 100  

for chamada in range(Chamadas):
    for t in range(T):  
        aptabilities = Aptabilities(Pop)  
        selection = Selection(Pop, aptabilities)  
        Pop = Reproduce(Selection(Pop, aptabilities))  
    
    #calcula as aptidões da última população
    fitness_values = [f(ind) for ind in Pop]

    menor_aptidao = np.min(fitness_values)
    maior_aptidao = np.max(fitness_values)
    media_aptidao = np.mean(fitness_values)
    desvio_padrao_aptidao = np.std(fitness_values)

    print(f"Chamada {chamada + 1}:")
    print(f"Menor aptidão: {menor_aptidao}")
    print(f"Maior aptidão: {maior_aptidao}")
    print(f"Média aptidão: {media_aptidao}")
    print(f"Desvio padrão aptidão: {desvio_padrao_aptidao}")
    print("-" * 40)

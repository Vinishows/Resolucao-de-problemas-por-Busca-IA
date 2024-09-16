import numpy as np
import matplotlib.pyplot as plt

T = 100  # número de iterações de reprodução/seleção (gerações)
N = 50   # número de indivíduos na população
nd = 12  # número de bits que representam cada dimensão
P = 20   # quantidade de dimensões (variáveis) de cada indivíduo
limits = [-10, 10]  
rep_tax, mut_tax = 0.90, 0.01  

# def log(ind):
#     return (np.log(10) / np.log(f(ind)))**30

#função de rastrigin
def f(x):
    A = 10
    soma = np.sum(x**2 - A * np.cos(2 * np.pi * x))
    return A * len(x) + soma + 1 # soma + 1 para  Ψ(x) = f(x) + 1

#calcula as aptidões (probabilidades) para cada indivíduo da população
# def Aptabilities(pop):
#     p = []
#     s = 0
#     for ind in pop:
#         s += log(ind)
#     for ind in pop:
#         p.append(log(ind) / s)
#     return np.array(p)

#seleção baseada em torneio
def Selection(pop, k=3):
    selecionados = []
    for _ in range(len(pop)):
        competidores = np.random.choice(pop, k)
        melhor = min(competidores, key=f)
        selecionados.append(melhor)
    return np.array(selecionados)

def SBX(p1, p2, eta=2):
    u = np.random.rand(len(p1))  
    gamma = np.empty(len(p1))  
    
    for i in range(len(p1)):  
        if u[i] <= 0.5:
            gamma[i] = (2 * u[i]) ** (1 / (eta + 1)) 
        else:
            gamma[i] = (1 / (2 * (1 - u[i]))) ** (1 / (eta + 1))  

    c1 = 0.5 * ((1 + gamma) * p1 + (1 - gamma) * p2)
    c2 = 0.5 * ((1 - gamma) * p1 + (1 + gamma) * p2)
    
    return np.clip(c1, *limits), np.clip(c2, *limits)

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


Pop = np.random.uniform(low=limits[0], high=limits[1], size=(N, P)) #inicializa a população aleatória (binária) de N indivíduos, cada um com nd * P bits
Chamadas = 100  

for chamada in range(Chamadas):
    for t in range(T):  
        #aptabilities = Aptabilities(Pop)  
        #selection = Selection(Pop, aptabilities)  
        #Pop = Reproduce(Selection(Pop, aptabilities))  
    
    #calcula as aptidões da última população
    #fitness_values = [f(ind) for ind in Pop]

    # menor_aptidao = np.min(fitness_values)
    # maior_aptidao = np.max(fitness_values)
    # media_aptidao = np.mean(fitness_values)
    # desvio_padrao_aptidao = np.std(fitness_values)

    # print(f"Chamada {chamada + 1}:")
    # print(f"Menor aptidão: {menor_aptidao}")
    # print(f"Maior aptidão: {maior_aptidao}")
    # print(f"Média aptidão: {media_aptidao}")
    # print(f"Desvio padrão aptidão: {desvio_padrao_aptidao}")
        print("-" * 40)
    
    
    
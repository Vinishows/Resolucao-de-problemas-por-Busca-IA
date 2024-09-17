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

#seleção baseada em torneio
def Selection(pop, aptabilities, k=3):
    competidores_idx = np.random.choice(len(pop), k, replace=False)  
    melhor = competidores_idx[np.argmin(np.array(aptabilities)[competidores_idx])]
    return pop[melhor]

def SBX(p1, p2, eta=2):
    u = np.random.uniform(size=len(p1))
    gamma = np.empty(len(p1))  
    
    for i in range(P):  
        if u[i] <= 0.5:
            gamma[i] = (2 * u[i]) ** (1 / (eta + 1)) 
        else:
            gamma[i] = (1 / (2 * (1 - u[i]))) ** (1 / (eta + 1))  

    c1 = 0.5 * ((1 + gamma) * p1 + (1 - gamma) * p2)
    c2 = 0.5 * ((1 - gamma) * p1 + (1 + gamma) * p2)
    
    return np.clip(c1, *limits), np.clip(c2, *limits)

def Cruz_Mut(indv):
    perturbacoes = np.random.normal(0, .1, size=20)
    for index in range(len(indv)) :
        chance = np.random.rand()
        if chance <= mut_tax:
            indv[index] += perturbacoes[index]
            indv[index] = np.clip(indv[index], limits[0], limits[1])  
    return indv

def Reproduce(pop, aptabilities):
    p = []
    for i in range(len(pop) // 2):
        daddy = Selection(pop, aptabilities)
        issues = Selection(pop, aptabilities)
        
        if np.random.rand() < rep_tax:
            fih1, fih2 = SBX(daddy, issues)
        else:
            fih1, fih2 = np.copy(daddy), np.copy(issues)
        
        fih1 = Cruz_Mut(fih1)
        fih2 = Cruz_Mut(fih2)
        
        p.extend([fih1, fih2])
        
    return np.array(p)



# Pop = np.random.uniform(low=limits[0], high=limits[1], size=(P)) #inicializa a população aleatória (binária) de N indivíduos, cada um com nd * P bits
# gerar inidividuo
def inidvi():
    return np.random.uniform(low=limits[0], high=limits[1], size=(P))

Pop = np.array([inidvi() for _ in range(100)])

Chamadas = 100

count = 0
for chamada in range(Chamadas):
    for t in range(T):  
        aptabilities = np.array([f(ind) for ind in Pop])
        Pop = Reproduce(Pop, aptabilities)

        if count == 15:
            if np.abs(last_value - min(aptabilities)) < 10e-9:
                break
            else:
                count = 0
        last_value = min(aptabilities)
        count += 1


    menor_aptidao = np.min(aptabilities)
    maior_aptidao = np.max(aptabilities)
    media_aptidao = np.mean(aptabilities)
    desvio_padrao_aptidao = np.std(aptabilities)

    print(f"Chamada {chamada + 1}:")
    print(f"Menor aptidão: {menor_aptidao}")
    print(f"Maior aptidão: {maior_aptidao}")
    print(f"Média aptidão: {media_aptidao}")
    print(f"Desvio padrão aptidão: {desvio_padrao_aptidao}")
    print("-" * 40)
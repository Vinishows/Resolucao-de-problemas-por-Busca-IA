import numpy as np
import matplotlib.pyplot as plt

T = 100  # número de gerações
N = 50   # número de indivíduos na população
P = 20   # quantidade de dimensões (variáveis) de cada indivíduo
limits = [-10, 10]  # limites das variáveis
rep_tax, mut_tax = 0.90, 0.01  # taxa de recombinação e mutação

# Função de Rastrigin
def f(x):
    A = 10
    soma = np.sum(x**2 - A * np.cos(2 * np.pi * x))
    return A * len(x) + soma + 1  # Ψ(x) = f(x) + 1

# Seleção por Torneio
def Selection(pop, k=3):
    selecionados = []
    for _ in range(len(pop)):
        # Seleciona os índices dos competidores ao invés de selecionar diretamente os indivíduos
        competidores_idx = np.random.choice(len(pop), k, replace=False)  
        competidores = pop[competidores_idx]  # Obtém os indivíduos com os índices selecionados
        melhor = min(competidores, key=f)  # Seleciona o melhor (menor valor de f)
        selecionados.append(melhor)
    return np.array(selecionados)

# Recombinação Simétrica via SBX
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

# Mutação Gaussiana
def Mutate(ind, mut_prob=mut_tax):
    for i in range(len(ind)):
        if np.random.uniform() < mut_prob:
            ind[i] += np.random.normal(0, 1)  # adição de ruído gaussiano
            ind[i] = np.clip(ind[i], *limits)  # garantir que os valores fiquem nos limites
    return ind

# Reproduzir uma nova população
def Reproduce(pop):
    new_pop = []
    for i in range(0, len(pop), 2):
        if np.random.uniform() < rep_tax:
            c1, c2 = SBX(pop[i], pop[i+1])
            new_pop.extend([Mutate(c1), Mutate(c2)])
        else:
            new_pop.extend([Mutate(pop[i]), Mutate(pop[i+1])])
    return np.array(new_pop)

# Inicializa a população
Pop = np.random.uniform(low=limits[0], high=limits[1], size=(N, P))

# Rodadas de execuções
Chamadas = 100  
resultados = []

for chamada in range(Chamadas):
    Pop = np.random.uniform(low=limits[0], high=limits[1], size=(N, P))  # reinicia a população a cada rodada
    for t in range(T):
        Pop = Reproduce(Selection(Pop))

    # Calcula as aptidões da última população
    fitness_values = np.array([f(ind) for ind in Pop])
    
    menor_aptidao = np.min(fitness_values)
    maior_aptidao = np.max(fitness_values)
    media_aptidao = np.mean(fitness_values)
    desvio_padrao_aptidao = np.std(fitness_values)
    
    # Armazena os resultados de cada rodada
    resultados.append([menor_aptidao, maior_aptidao, media_aptidao, desvio_padrao_aptidao])

    # Imprime os resultados da rodada atual
    print(f"Rodada {chamada + 1}:")
    print(f"Menor aptidão: {menor_aptidao}")
    print(f"Maior aptidão: {maior_aptidao}")
    print(f"Média aptidão: {media_aptidao}")
    print(f"Desvio padrão aptidão: {desvio_padrao_aptidao}")
    print("-" * 40)

# Gera a tabela de comparação
resultados = np.array(resultados)
tabela = {
    "Menor Aptidão": resultados[:, 0],
    "Maior Aptidão": resultados[:, 1],
    "Média Aptidão": resultados[:, 2],
    "Desvio Padrão Aptidão": resultados[:, 3],
}

# Exibe as estatísticas finais consolidadas
print(f"Menor valor de aptidão em todas as rodadas: {np.min(resultados[:, 0])}")
print(f"Maior valor de aptidão em todas as rodadas: {np.max(resultados[:, 1])}")
print(f"Média dos valores de aptidão: {np.mean(resultados[:, 2])}")
print(f"Desvio padrão dos valores de aptidão: {np.mean(resultados[:, 3])}")

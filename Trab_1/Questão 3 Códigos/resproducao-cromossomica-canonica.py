import numpy as np
import matplotlib.pyplot as plt

T = 100
N = 50
nd = 12
P = 20
limits = [-10, 10]
rep_tax, mut_tax = 0.85, 0.01

def psi(x, nd, inf, sup):
    s = 0
    for l in range(len(x)):
        s += x[nd-1-l]*2**l
    return inf + (sup-inf)/(2**nd-1) * s

def log(ind):
    return (np.log(10) / np.log(f(ind)))**30

def f(x):
    A = 10
    s = 0
    for i in range(P):
        start = nd*i
        final = start+nd
        xi = psi(x[start:final], nd, *limits)
        s += xi**2 - A*np.cos(2*np.pi*xi)
    return A*P + s + 1

def Aptabilities(pop):
    p = []
    s = 0
    for ind in pop:
        s += log(ind)
    for ind in pop:
        p.append(log(ind) / s)
    return np.array(p)

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

def Motel(x1,x2):
        RNA = np.random.randint(0,2,len(x1))
        DNA = list(zip(x1,x2))
        c1,c2 = [],[]
        for i in range(len(DNA)):
            c1.append(DNA[i][RNA[i]])
            c2.append(DNA[i][not RNA[i]])
        for i in range(len(DNA)):
            rnd_1 = np.random.uniform()
            rnd_2 = np.random.uniform()
            if rnd_1 < mut_tax:
                c1[i] = not c1[i]
            if rnd_2 < mut_tax:
                c2[i] = not c2[i]
        return np.array(c1), np.array(c2)

def Reproduce(pop):
    # Passar em pares
    p = []
    for i in range(0, len(pop), 2):
        if np.random.uniform() < rep_tax:
            c1, c2 = Motel(pop[i], pop[i+1])
            p.extend([c1,c2])
        else:
            p.extend([pop[i], pop[i+1]])
    return np.array(p)


Pop = np.random.randint(0, 2, size=(N, nd*P))
Chamadas = 6
Values_Melhores = []

for _ in range(Chamadas):
    for _ in range(T):
        aptabilities = Aptabilities(Pop)
        selection = Selection(Pop, aptabilities)
        Pop = Reproduce(Selection(Pop, aptabilities))
    # Pop == Ultima geração nesse ponto
    Values_Melhores.append(min([f(ind) for ind in Pop]))

for v in Values_Melhores:
    print(v)
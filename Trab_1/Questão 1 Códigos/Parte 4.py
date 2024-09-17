import numpy as np
import matplotlib.pyplot as plt

# Parâmetros do problema
max_int = 10000  # Número máximo de iterações
max_viz = 50     # Número máximo de vizinhanças
epsilon = .2     # Tamanho da perturbação para o Hill Climbing
sigma = .1       # Tamanho da perturbação para Busca Randômica Local

limits_x = [-5.12, 5.12]  # Limites para x1
limits_y = [-5.12, 5.12]  # Limites para x2

# Função de perturbação (aleatória)
def perturb(x, e, limits):
    return np.clip(np.random.uniform(x-e, x+e), *limits)

# Função de perturbação normal
def perturb_normal(x, e, limits):
    return np.clip(x+np.random.normal(loc=0,scale=e), *limits)

# Função objetivo
def F_Obj(x1, x2):
    return (x1**2 - 10*np.cos(2*np.pi*x1) + 10) + (x2**2 - 10*np.cos(2*np.pi*x2) + 10)

# Hill Climbing
rodadas = 100
x_otimos_hill = []
f_otimos_hill = []
count = 0
for rodada in range(rodadas):
    i = 0
    melhoria = True
    x_otm = limits_x[0]
    y_otm = limits_y[0]
    f_otm = F_Obj(x_otm, y_otm)
    last_value = f_otm
    
    while i < max_int and melhoria:
        j = 0
        melhoria = False
        while j < max_viz:
            x_cand = perturb(x_otm, epsilon, limits_x)
            y_cand = perturb(y_otm, epsilon, limits_y)
            f_cand = F_Obj(x_cand, y_cand)
            if f_cand < f_otm:   # Minimização
                x_otm = x_cand
                y_otm = y_cand
                f_otm = f_cand
                melhoria = True
                break
            if count == 25:
                if np.abs(last_value - f_otm) < 0.0000001:
                    break
            j += 1
            count +=1
        i += 1
    x_otimos_hill.append([x_otm, y_otm])
    f_otimos_hill.append(f_otm)

x_otimos_hill = np.array(x_otimos_hill)

# Busca Randômica Local
x_otimos_local = []
f_otimos_local = []
count = 0
for rodada in range(rodadas):
    i = 0
    melhoria = True
    x_otm, y_otm = np.random.uniform(*limits_x), np.random.uniform(*limits_y)
    f_otm = F_Obj(x_otm, y_otm)
    last_value = f_otm
    
    while i < max_int and melhoria:
        x_cand = perturb_normal(x_cand, sigma, limits_x)
        y_cand = perturb_normal(y_cand, sigma, limits_y)
        f_cand = F_Obj(x_cand, y_cand)
        if f_cand < f_otm:  # Minimização
            x_otm = x_cand
            y_otm = y_cand
            f_otm = f_cand
        if count == 25 and np.abs(last_value - f_otm) < 0.0000001:
            break
        count +=1
        i += 1
    x_otimos_local.append([x_otm, y_otm])
    f_otimos_local.append(f_otm)

x_otimos_local = np.array(x_otimos_local)

# Busca Randômica Global
x_otimos_global = []
f_otimos_global = []
count = 0
for rodada in range(rodadas):
    i = 0
    melhoria = True
    x_otm = np.random.uniform(*limits_x)
    y_otm = np.random.uniform(*limits_y)
    f_otm = F_Obj(x_otm, y_otm)
    last_value = f_otm
    
    while i < max_int and melhoria:
        x_cand = np.random.uniform(*limits_x)
        y_cand = np.random.uniform(*limits_y)
        f_cand = F_Obj(x_cand, y_cand)
        if f_cand < f_otm:  # Minimização
            x_otm = x_cand
            y_otm = y_cand
            f_otm = f_cand
        if count == 25 and np.abs(last_value - f_otm) < 0.0000001:
            break
        count +=1
        i += 1
    x_otimos_global.append([x_otm, y_otm])
    f_otimos_global.append(f_otm)

x_otimos_global = np.array(x_otimos_global)

#Calculo da moda
def moda_np(arr):
    unique, counts = np.unique(arr, return_counts=True)
    moda_index = np.argmax(counts)
    return unique[moda_index]

print("Moda Hill Climbing (f_otm):", moda_np(f_otimos_hill))
print("Moda LRS (f_otm):", moda_np(f_otimos_local))
print("Moda GRS (f_otm):", moda_np(f_otimos_global))

# Plotagem da superfície 3D
x1_vals = np.linspace(-5.12, 5.12, 400)
x2_vals = np.linspace(-5.12, 5.12, 400)
X1, X2 = np.meshgrid(x1_vals, x2_vals)
Z = F_Obj(X1, X2)

fig = plt.figure(figsize=(18, 6))

# Gráfico Hill Climbing
ax1 = fig.add_subplot(131, projection='3d')
ax1.plot_surface(X1, X2, Z, cmap='viridis', alpha=.1)
for i in range(len(x_otimos_hill)):
    ax1.scatter(x_otimos_hill[i, 0], x_otimos_hill[i, 1], F_Obj(*x_otimos_hill[i]),marker='o')
ax1.set_title('Hill Climbing')

# Gráfico Busca Randômica Local
ax2 = fig.add_subplot(132, projection='3d')
ax2.plot_surface(X1, X2, Z, cmap='viridis', alpha=.1)
for i in range(len(x_otimos_local)):
    ax2.scatter(x_otimos_local[i, 0], x_otimos_local[i, 1], F_Obj(*x_otimos_local[i]),marker='x')
ax2.set_title('Busca Randômica Local')

# Gráfico Busca Randômica Global
ax3 = fig.add_subplot(133, projection='3d')
ax3.plot_surface(X1, X2, Z, cmap='viridis', alpha=.1)
for i in range(len(x_otimos_global)):
    ax3.scatter(x_otimos_global[i, 0], x_otimos_global[i, 1], F_Obj(*x_otimos_global[i]),marker='*')
ax3.set_title('Busca Randômica Global')

plt.tight_layout()
plt.show()
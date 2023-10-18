from pyomo.environ import *
from glob import glob
import matplotlib.pyplot as plt
import math

A = None  # Quantidade de locais candidatos
B = None  # Quantidade de pontos de demanda
C = None  # Custo das antenas
D = None  # Alcance das antenas
nx = None  # Coordenada x de pontos de demanda
ny = None  # Coordenada y de pontos de demanda
mx = None  # Coordenada x de locais candidatos
my = None  # Coordenada y de locais candidatos

def read_instance(instance):
    global A, B, C, D, mx, my, nx, ny
    nx = []
    ny = []
    mx = []
    my = []
    file = open(instance, 'r')
    first = True
    for line in file.readlines():
        if first:
            A = int(line.split(' ')[1])
            B = int(line.split(' ')[3])
            C = int(line.split(' ')[5])
            D = int(line.split(' ')[7])
            first = False
            continue
        if (line.split(' ')[0] == 'n'):
            nx.append(int(line.split(' ')[1]))
            ny.append(int(line.split(' ')[2]))
        elif (line.split(' ')[0] == 'm'):
            mx.append(int(line.split(' ')[1]))
            my.append(int(line.split(' ')[2]))

def distance(i, j):
    return ((mx[i] - nx[j]) ** 2 + (my[i] - ny[j]) ** 2) ** 0.5

def solve():
    # Criação do modelo
    model = ConcreteModel()

    # Variáveis de decisão
    model.a = Var(range(A), domain=Binary)
    model.b = Var(range(B), domain=Binary)

    # Função objetivo
    model.obj = Objective(
        expr=sum([C * model.a[j] for j in range(A)]) * -1
             + sum([min([distance(i, j) for j in range(A)]) * model.b[i] for i in range(B)]),
        sense=maximize
    )

    # Restricoes
    model.cons = ConstraintList()

    # Restrição para garantir que pelo menos uma antena seja alocada
    for i in range(B):
        model.cons.add(expr=sum(model.a[j] for j in range(A)) >= 1)

    # Restrição para garantir que pelo menos uma antena seja alocada para cada ponto de demanda
    for i in range(B):
        model.cons.add(expr=sum(model.a[j] for j in range(A) if distance(i, j) <= D) >= model.b[i])

    # Solução
    solver = SolverFactory('glpk')
    results = solver.solve(model, timelimit=200)

    # Verificar se a solução é ótima
    is_optimal = (results.solver.status == SolverStatus.ok) and (results.solver.termination_condition == TerminationCondition.optimal)
    if is_optimal:
        # Verificar a cobertura de pontos de demanda
        uncovered_demand_points = [i + 1 for i in range(B) if model.b[i]() == 0]
        if uncovered_demand_points:
            is_optimal = False

    if is_optimal:
        print("Solução Ótima Encontrada!")
    else:
        print("O Solver não encontrou uma solução ótima ou há pontos de demanda não cobertos.")

    for j in range(A):
        print(f'Antena {j + 1}: {model.a[j]()}')

    for i in range(B):
        print(f'Ponto de demanda {i + 1}: {model.b[i]()}')

    # Valor da função objetivo
    print("\nValor da Função Objetivo:")
    print(model.obj.expr())

    # Executar a função para plotar a solução e salvar
    plot_solution_and_save(mx, my, nx, ny, [model.a[j]() for j in range(A)], [model.b[i]() for i in range(B)], instance_name, D)

def plot_solution_and_save(mx, my, nx, ny, a, b, instance_name, D):
    plt.figure(figsize=(8, 6))

    # Plotar os pontos de demanda
    plt.scatter(nx, ny, color='blue', label='Pontos de Demanda')

    # Plotar as antenas alocadas
    for j in range(len(mx)):
        if a[j] == 1:
            # Coordenadas do centro da antena
            ax = mx[j]
            ay = my[j]

            # Desenhar a área de cobertura (um círculo)
            circle = plt.Circle((ax, ay), D, fill=False, color='red', linestyle='dotted', label=f'Antena {j + 1} Coverage')
            plt.gca().add_patch(circle)

            plt.scatter(ax, ay, color='red', marker='^', s=100, label=f'Antena {j + 1}')

    # Adicionar legendas
    plt.legend()

    # Definir rótulos dos eixos
    plt.xlabel('Coordenada X')
    plt.ylabel('Coordenada Y')

    # Exibir o gráfico
    plt.title('Alocação de Antenas e Cobertura de Pontos de Demanda')
    plt.grid(True)

    # Salvar o gráfico como um arquivo de imagem (PNG)
    plt.savefig(f'{instance_name}_solution.png')
    plt.close()

for instance in glob('./instancias/instanciaGrande1.txt'):
    read_instance(instance)
    instance_name = instance[instance.rindex('/') + 1:]
    print(instance_name + ': ', end='')
    solve()

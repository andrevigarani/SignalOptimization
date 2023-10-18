from pyomo.environ import *
from glob import glob

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
            # colecao = int(line.split(' '))
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
    # Função para calcular a distância entre os pontos i e j -> ** 0.5 é usado para calcular a raiz quadrada
    return ((mx[i] - nx[j]) ** 2 + (my[i] - ny[j]) ** 2) ** 0.5

def solve():

    # Criação do modelo
    model = ConcreteModel()

    # Variáveis de decisão
    model.a = Var(range(A), domain = Binary)
    model.b = Var(range(B), domain = Binary)

    # Função objetivo
    model.obj = Objective(expr=sum([C * model.a[j] for j in range(A)])*-1
                               +sum([min([distance(i,j) for j in range(A)]) * model.b[i] for i in range(B)]),sense=maximize)

    # Restricoes
    model.cons = ConstraintList()

    # Restrição para garantir que pelo menos uma antena seja alocada
    for i in range(B):
        model.cons.add(expr=sum(model.a[j] for j in range(A)) >= 1)

    # Restrição para garantir que pelo menos uma antena seja alocada para cada ponto de demanda
    for i in range(B):
        model.cons.add(expr=sum(model.a[j] for j in range(A) if distance(i,j) <= D) >= model.b[i])

    # Solução
    solver = SolverFactory('glpk')
    results = solver.solve(model, timelimit=200)

    # Verificar se a solução é ótima
    if (results.solver.status == SolverStatus.ok) and (results.solver.termination_condition == TerminationCondition.optimal):
        print("Solução Ótima Encontrada!")
    else:
        print("O Solver não encontrou uma solução ótima.")

    for j in range(A):
        print(f'Antena {j+1}: {model.a[j]()}')

    for i in range(B):
        print(f'Ponto de demanda {i+1}: {model.b[i]()}')

    # Valor da função objetivo
    print("\nValor da Função Objetivo:")
    print(model.obj.expr())

# for instance in glob('./instancias/*'):
for instance in glob('./instancias/instanciaPequena1.txt'):
    read_instance(instance)
    print(instance[instance.rindex('/') + 1:] + ': ', end = '')
    solve()
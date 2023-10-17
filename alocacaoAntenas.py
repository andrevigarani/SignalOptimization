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
    model.a = Var(range(A), domain = Boolean)
    model.b = Var(range(B), domain = Boolean)

    # Função objetivo
    model.obj = Objective(expr=sum([C * model.a[i] for i in range(A)])+sum([min([distance(i, j) for j in range(B)]) * model.b[i] for i in range(B)]),sense=minimize)

    # Restrições
    # for i in range(B): model.con1 = Constraint(expr=sum([model.a[j] for j in range(A)]) >= 1)
    # for i in range(B): model.con2 = Constraint(expr= model.b[i] in [0, 1])
    # for j in range(A): model.con3 = Constraint(expr= model.a[j] in [0, 1])

    model.peloMenosUmaAntena = ConstraintList()
    for i in range(B):
        model.peloMenosUmaAntena.add(sum(model.a[j] for j in range(A)) >= 1)

    model.varBinaria = ConstraintList()
    for i in range(B):
        model.varBinaria.add(model.b[i] <= 1)
        model.varBinaria.add(0 <= model.b[i])
    for j in range(A):
        model.varBinaria.add(model.a[j] <= 1)
        model.varBinaria.add(0 <= model.a[j])

    # Solução
    opt = SolverFactory('glpk')
    opt.solve(model)
    return model.obj.expr()


for instance in glob('./instancias/instanciaPequena1.txt'):
    read_instance(instance)
    print(instance[instance.rindex('/') + 1:] + ': ', end = '')
    print(solve())
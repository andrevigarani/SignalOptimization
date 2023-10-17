from pyomo.environ import *
from glob import glob

A = None # Quantidade de locais candidatos
B = None # Quantidade de pontos de demanda
C = None # Custo das antenas
D = None # Alcance das antenas
nx = None # Coordenada x de pontos de demanda
ny = None # Coordenada y de pontos de demanda
mx = None # Coordenada x de locais candidatos
my = None # Coordenada y de locais candidatos

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

def solve():
    # Criação do modelo
    model = ConcreteModel()

for instance in glob('./instanciaPequena1.txt'):
    read_instance(instance)
    print(A)
    print(B)
    print(C)
    print(D)
    print(nx)
    print(ny)
    print(mx)
    print(my)
    # print(instance[instance.rindex('/') + 1:] + ': ', end = '')
    # print(solve())
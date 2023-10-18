# SignalOptimization
Esse código Python é um script que resolve um problema de localização de instalações usando o Pyomo e o solucionador GLPK. O código lê dados de entrada de um arquivo de instância, define um modelo de otimização matemática e, em seguida, o resolve. Aqui está uma explicação detalhada do que o código faz:

Importa as bibliotecas necessárias: Pyomo e o módulo glob.

Define variáveis globais para os parâmetros do problema: A (número de locais candidatos), B (número de pontos de demanda), C (custo das antenas), D (alcance das antenas), nx e ny (coordenadas dos pontos de demanda), mx e my (coordenadas dos locais candidatos).

Implementa uma função read_instance para ler os dados da instância de um arquivo. A função extrai os valores de A, B, C, D, nx e ny.

Implementa uma função distance para calcular a distância entre dois pontos usando a fórmula da distância euclidiana.

Implementa a função solve, que cria um modelo matemático concreto do Pyomo para o problema de localização de instalações.

Define variáveis de decisão:

a é uma variável binária que indica se uma antena é colocada em cada local candidato.
b é uma variável binária que indica se cada ponto de demanda é coberto por pelo menos uma antena.
Define a função objetivo, que maximiza o benefício total (negativo do custo):

O primeiro termo minimiza o custo total de colocar antenas.
O segundo termo minimiza a distância ponderada total dos pontos de demanda para as antenas.
Adiciona restrições:

Garante que pelo menos uma antena seja colocada.
Garante que cada ponto de demanda seja coberto por pelo menos uma antena dentro do alcance especificado.
Usa o solucionador GLPK para resolver o problema de otimização com um limite de tempo de 200 segundos.

Verifica se o solucionador encontrou uma solução ótima e, se sim, imprime os resultados:

Imprime se uma solução ótima foi encontrada.
Imprime as decisões binárias para a colocação de antenas nos locais candidatos.
Imprime as decisões binárias para cobrir os pontos de demanda.
Imprime o valor da função objetivo.

Por fim, há um loop que percorre todos os arquivos de instância no diretório 'instancias' e aplica as funções read_instance e solve a cada instância.


# Gerador de instâncias
Sem sucesso em encontrar instâncias para nosso problema , implementamos um gerador de instâncias para o problema de localização de instalações de diferentes tamanhos e salva os dados em arquivos de texto.

Define uma função geraInstancia que recebe três argumentos: o nome do arquivo de destino, o número de pontos de demanda e o número de locais candidatos. A função cria um arquivo de texto e escreve os dados da instância, incluindo o número de locais candidatos, o número de pontos de demanda, o custo das antenas (fixo em 7000) e o alcance das antenas (fixo em 10000).

Gera coordenadas aleatórias para os pontos de demanda e os locais candidatos usando a biblioteca random. Para cada ponto de demanda e local candidato, são gerados valores aleatórios de coordenadas x e y dentro de faixas específicas (0 a 33000 para x e 0 a 30000 para y).

Chama a função geraInstancia duas vezes: primeiro, para gerar 15 instâncias pequenas com 10 pontos de demanda e 10 locais candidatos, e depois para gerar 15 instâncias maiores com 100 pontos de demanda e 100 locais candidatos. Os arquivos de instância são nomeados de acordo com o tamanho e uma sequência numérica.

No geral, esse código é usado para criar dados de entrada (instâncias) para um problema de localização de instalações. Ele gera diferentes tamanhos de instâncias com números aleatórios de pontos de demanda e locais candidatos, que podem ser usados como entrada para o código que você forneceu anteriormente para resolver o problema de localização de instalações. Essa geração de instâncias é útil para testar e avaliar o desempenho do algoritmo de resolução em diferentes cenários.

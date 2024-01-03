## Overview

O presente repositório visa utilizar um algoritmo genético, implementado na linguagem Python, para otimizar os valores das passagens e os horários dos voos dos pesquisadores participantes do congresso sobre o aquecimento global em Roma. Através desse algoritmo, busca-se encontrar a melhor combinação de voos que
minimize os custos das passagens e reduza o tempo de espera nos aeroportos, proporcionando uma logística eficiente e econômica para os participantes.

## O algoritmo Genético 

### Individuo

O indivíduo do Algoritmo Genético (GA) construído para a implementação foi definido como um conjunto de 12 voos. Esses voos foram divididos em duas partes: a primeira parte consistia em seis voos partindo de Lisboa, Madrid, Paris, Dublin, Bruxelas ou Londres com destino a Roma, enquanto
a segunda parte incluía os seis voos de Roma com destino às cidades de origem de cada pesquisador. Cada voo desse conjunto apresenta informações como horário de embarque e desembarque, além do preço da passagem aérea. A população inicial foi estabelecida com 25 indivíduos,
sendo que cada um desses indivíduos foi criado a partir de uma seleção aleatória entre os 120 voos disponíveis na base de dados. É importante ressaltar que nenhum voo se repetiu em um mesmo indivíduo.

Abaixo está um pedaço do código em que geramos um indivíduo.

```python

    def gera_aleatorio(self):

        voos_ida = []
        voos_volta = []

        voo_ida = 0

        while len(self.aeroportos_visitados) < 6:

            voo = random.choice(list(self.df.items()))
            voo_ida = str(voo[1][0])

            if str(voo[1][0]) not in self.aeroportos_visitados and voo_ida != 'FCO':
                voos_ida.append(voo)
                self.aeroportos_visitados.add(str(voo[1][0]))

                if int(voo[1][3]) < self.primeiro_ida:
                    self.primeiro_ida = int(voo[1][3])

                if int(voo[1][3]) > self.ultimo_ida:
                    self.ultimo_ida = int(voo[1][3])

                self.preco += int(voo[1][4])

        voos_ida = sorted(voos_ida, key=lambda x: x[1][0])

```
Dado que a população inicial é formada de forma aleatória, existe a chance de um indivíduo possuir mais de um voo com o mesmo local de partida. Para lidar com essa situação, foi introduzida uma variável que verifica se o voo selecionado aleatoriamente já está presente no vetor de voos. Isso garante
que não haja repetição de voos no mesmo indivíduo. Importante salientar, que, para facilitar as manipulações para os operadores de seleção e cruzamento, foi necessário ordenar o vetor de voos de ida em ordem alfabética com base na cidade de embarque.

### População 

A população é simplesmente a coleção dos indivíduos. Esta deve ser gerada de forma aleatória em um primeiro momento. Como a criação de indivíduos já é feita aleatoriamente então a população, se criada a partir da função gera_aleatorio, deve idem ser aleatória.

### *Fitness*

A fitness é a forma de avaliar aptidão do indivíduo para uma solução ótima do problema. No caso desse algoritmo o cálculo proposto foi criar uma única variável numérica que contém a soma do preço da passagem de todos os voos, o que inclui a ida e a volta para cada destino, e os tempos de espera na ida e
na volta, convertidos para minutos, como exposto no trecho de código abaixo:

```python
    def calc_fitness(self):

        self.preco = 0

        for c in range(0, 12):

            if c < 6:
                if int(self.ind[c][1][3]) < self.primeiro_ida:
                    self.primeiro_ida = int(self.ind[c][1][3])

                if int(self.ind[c][1][3]) > self.ultimo_ida:
                    self.ultimo_ida = int(self.ind[c][1][3])
            else:

                if int(self.ind[c][1][2]) < self.primeiro_volta:
                    self.primeiro_volta = int(self.ind[c][1][2])

                if int(self.ind[c][1][2]) > self.ultimo_volta:
                    self.ultimo_volta = int(self.ind[c][1][2])

            self.preco += int(self.ind[c][1][4])
```
O tempo de espera na ida é dado pela diferença entre o horário em que o primeiro e o último pesquisador chegam em Roma, dessa forma temos sempre como base o maior tempo de espera enfrentado por um deles no aguardo da van. Na volta o cálculo é o mesmo, mas, dessa vez, são levados em conta os
horários em que os pesquisadores partirão para suas cidades de origem.

### Seleção

A seleção dos indivíduos para realizar o cruzamento é feito através do torneio. O torneio é um método de seleção de indivíduos para reprodução. A ideia é realizar competições entre subconjuntos aleatórios da população, conhecidos como "torneios", e selecionar os indivíduos mais aptos desses torneios para serem pais na próxima geração.
Além disso essa técnica é relativamente simples de implementar e não requer uma classificação completa de toda a população, tornando-o eficiente computacionalmente. Dessa forma, a probabilidade de escolher indivíduos mais aptos é maior, mas ainda há espaço para diversidade genética.

```python
        def torneio(self, pop):

            aux = uniform(0, 1)
            torn = sample(pop, self.ntoneio)

            if aux <= 0.75:
                i = min(torn, key=lambda indiv: indiv.fitness)
            else:
                i = max(torn, key=lambda indiv: indiv.fitness)
            return i
```
### Cruzamento (*Crossover*)

O cruzamento é o processo de juntar dois indivíduos, combinar seus atributos e gerar um novo indivíduo. Como os indivíduos pais são indivíduos da população, eles podem ser levados para as próximas gerações.

O cruzamento realizado é o crossover de ponto de corte.

```python
    def crossover(self, pai1: individuo, pai2: individuo):
        ind_filho = individuo(self.df)
        childP = []
        geneA = int(random.random() * len(pai1.ind))
        geneB = int(random.random() * len(pai1.ind))
        startGene = min(geneA, geneB)
        endGene = max(geneA, geneB)

        for i in range(0, 12):

            if startGene <= i <= endGene:
                childP.append(pai1.ind[i])
            else:
                childP.append(pai2.ind[i])
```

### Mutação

A operação de mutação é utilizada para introduzir a variabilidade genética nos indivíduos. A mutação utilizada foi a uniforme, caso, um gene dentro do indivíduo, que equivale a um voo, é selecionado aleatoriamente e seu valor é alterado para outro valor válido dentro do espaço de busca.

```python
            if aux < self.taxa_mutacao:

                limite_inf = math.floor(int(ind.ind[c][0]) / 20) * 20
                limite_sup = limite_inf + 19
                indice = random.randint(limite_inf, limite_sup)

                if c < 6:

                    while indice % 2 == 0:
                        n_rand = random.randint(limite_inf, limite_sup)
                        indice = n_rand

                    resultado = indice, ind.df[indice]

                    ind.ind[c] = resultado

                else:
                    while indice % 2 != 0:
                        n_rand = random.randint(limite_inf, limite_sup)
                        indice = n_rand

                    resultado = indice, ind.df[indice]

                    ind.ind[c] = resultado
```
A mutação ocorre em cada gene do indivíduo. Para cada gene, um número aleatório é gerado no intervalo de 0 a 1. Se esse número for menor que uma determinada taxa de mutação, o gene será mutado.

### Elitismo

O elitismo consiste em preservar o(s) melhor(es) indivíduo(s) de uma geração para a próxima, garantindo que suas características favoráveis sejam transmitidas. Isso ajuda a manter a qualidade da população e acelerar a convergência para soluções ótimas. No código em questão
comparamos o melhor indivíduo da população anterior com o melhor indivíduo da nova população. Se o melhor indivíduo da população anterior tiver um valor de fitness menor ao melhor indivíduo da nova população, substituímos o pior indivíduo da nova população pelo melhor
indivíduo da população anterior.


## Resultados

Após a realização dos testes, alguns indivíduos interessantes foram gerados, sendo entre estes um com o menor tempo de espera, um com o menor preço para passagens, outro com o melhor fitness, e por fim um indivíduo com um custo total das passagens relativamente acessível e
que possui tempo de espera razoável em comparação com os outros indivíduos.

* <strong>Melhor tempo de espera</strong>

<div align="center">
<img src="https://github.com/thiagcarvalho/OtimizadorHorariosVoos-GA/assets/46302988/12582d4b-487e-4980-95e2-d9b2b6dda10a.png" />
</div>

* <strong>Menor preço (passagens) </strong>

<div align="center">
<img src="https://github.com/thiagcarvalho/OtimizadorHorariosVoos-GA/assets/46302988/70360077-256b-496f-8a46-b0a8cd7bdc50.png" />
</div>

* <strong>Melhor *fitness*</strong>

<div align="center">
<img src="https://github.com/thiagcarvalho/OtimizadorHorariosVoos-GA/assets/46302988/ef111510-0439-4f0d-aaa5-edf294195946.png" />
</div>

* <strong>Indivíduo balanceado</strong>

<div align="center">
<img src="https://github.com/thiagcarvalho/OtimizadorHorariosVoos-GA/assets/46302988/24432d28-cbc8-44c3-82f9-05980b3d76a8.png" />
</div>












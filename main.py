import math
import pandas as pd
from random import shuffle, sample, uniform, random, randrange
import random
from pprint import pprint
import numpy as np
from copy import copy, deepcopy
import matplotlib.pyplot as plt
import sys


class individuo:
    def __init__(self, df: dict) -> None:
        self.ind = []
        self.df = df
        self.fitness = 0
        self.aeroportos_visitados = set()
        self.indice_voo = set()
        self.primeiro_ida = sys.maxsize
        self.ultimo_ida = -sys.maxsize - 1
        self.primeiro_volta = sys.maxsize
        self.ultimo_volta = -sys.maxsize - 1
        self.preco = 0
        # self.calc_fitness()

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

        while len(self.aeroportos_visitados) > 0:

            voo = random.choice(list(self.df.items()))
            voo_ida = str(voo[1][1])

            if voo_ida in self.aeroportos_visitados and str(voo[1][0]) == 'FCO':

                voos_volta.append(voo)
                self.aeroportos_visitados.remove(voo_ida)

                if int(voo[1][2]) < self.primeiro_volta:
                    self.primeiro_volta = int(voo[1][2])

                if int(voo[1][2]) > self.ultimo_volta:
                    self.ultimo_volta = int(voo[1][2])

                self.preco += int(voo[1][4])

        voos_volta = sorted(voos_volta, key=lambda x: x[1][1])

        self.ind = voos_ida + voos_volta


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

        self.fitness = self.ultimo_ida - self.primeiro_ida
        self.fitness += self.ultimo_volta - self.primeiro_volta
        self.fitness += self.preco

    def __str__(self) -> None:
        return str(self.ind)


class ga:
    def __init__(self, popsize, ngeneration, df, ntoneio, taxa_cruzamento, taxa_mutacao, n_elitismo) -> None:
        self.popsize = popsize
        self.ngeneration = ngeneration
        self.df = df
        self.ntoneio = ntoneio
        self.taxa_cruzamento = taxa_cruzamento
        self.taxa_mutacao = taxa_mutacao
        self.n_elitismo = n_elitismo
        self.melhor = 0
        self.curva_boa = []
        self.curva_ruim = []
        self.curva_media = []
        self.elite = []

    def pop_inicial(self):
        pop = []
        for i in range(0, self.popsize):
            ind = individuo(self.df)
            ind.gera_aleatorio()
            ind.calc_fitness()
            pop.append(ind)

        return pop

    def run(self):
        pop = self.pop_inicial()
        for i in range(0, self.ngeneration):
            new_pop = []
            for j in range(0, int(len(pop)/2)):
                ind1 = deepcopy(self.torneio(pop))
                ind2 = deepcopy(self.torneio(pop))

                aux = uniform(0, 1)
                if aux < self.taxa_cruzamento:
                    aux1 = self.crossover(ind1, ind2)
                    aux2 = self.crossover(ind2, ind1)
                    ind1 = aux1
                    ind2 = aux2

                ind1 = self.mutacao(ind1)
                ind2 = self.mutacao(ind2)

                ind1.calc_fitness()
                ind2.calc_fitness()
                new_pop.append(ind1)
                new_pop.append(ind2)

            #pop.sort(key=lambda x: x.fitness)
            best_oldgen = min(pop, key=lambda indiv: indiv.fitness)
            best_newgen = min(new_pop, key=lambda indiv: indiv.fitness)

            if int(best_oldgen.fitness) <= int(best_newgen.fitness):
                pior = max(new_pop, key=lambda indiv: indiv.fitness)
                indice_pior = new_pop.index(pior)
                new_pop[indice_pior] = best_oldgen

            self.elite, self.melhor= self.get_elite(new_pop, i)
            pop = new_pop


    def get_elite(self, pop, i):
        pop.sort(key=lambda x: x.fitness, reverse=True)
        meio = int(len(pop)/2)
        self.curva_boa.append(pop[-1].fitness)
        self.curva_ruim.append(pop[1].fitness)
        self.curva_media.append(pop[meio].fitness)
        print(i, pop[-1].fitness)
        return pop[-1].ind, pop[-1].fitness
    def torneio(self, pop):
        def torneio(self, pop):

            aux = uniform(0, 1)
            torn = sample(pop, self.ntoneio)


            if aux <= 0.75:
                i = min(torn, key=lambda indiv: indiv.fitness)
            else:
                i = max(torn, key=lambda indiv: indiv.fitness)
            return i
        aux = uniform(0, 1)
        torn = sample(pop, self.ntoneio)


        if aux <= 0.75:
            i = min(torn, key=lambda indiv: indiv.fitness)
        else:
            i = max(torn, key=lambda indiv: indiv.fitness)
        return i

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


        ind_filho.ind = childP
        ind_filho.calc_fitness()

        return ind_filho

    def mutacao(self, ind: individuo):

        for c in range(0, int(len(ind.ind))):

            aux = uniform(0, 1)

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

        return ind


def convert_to_minutes(value):
    hours, minutes = value.split(':')
    return int(hours) * 60 + int(minutes)


def convert_to_hours(value):
    hours = value // 60

    # Get additional minutes with modulus
    minutes = value % 60

    if int(hours) < 10:
        hours = "0"+str(hours)

    if int(minutes) < 10:
        minutes = "0"+str(minutes)

    # Create time as a string
    time_string = "{}:{}".format(hours, minutes)

    return time_string


dados = pd.read_csv('./dados/flights.txt', sep=',', skipfooter=0, header=None, index_col=None, engine='python')

dados.rename({0: 'aeroporto_saida', 1: 'aeroporto_chegada',
              2: 'horario_saida', 3: 'horario_chegada', 4: 'preco'}, axis=1, inplace=True)

dados['horario_saida'] = dados['horario_saida'].apply(convert_to_minutes)
dados['horario_chegada'] = dados['horario_chegada'].apply(convert_to_minutes)

base = {}
for i, row in dados.iterrows():
    base[i] = (row['aeroporto_saida'], row['aeroporto_chegada'], row['horario_saida'], row['horario_chegada'],
               row['preco'])

pop = []
GA = ga(popsize=25, ngeneration=400, df=base, ntoneio=2, taxa_cruzamento=0.65, taxa_mutacao=0.1, n_elitismo=1)
GA.run()

voos = ['Bruxelas', 'Paris', 'Dublin', 'Londres', 'Lisboa', 'Madrid']
preco = 0

for c in range(0, int(len(GA.elite)/2)):

    ida_partida = str(convert_to_hours(GA.elite[c][1][2]))
    ida_chegada = str(convert_to_hours(GA.elite[c][1][3]))
    volta_partida = str(convert_to_hours(GA.elite[c+6][1][2]))
    volta_chegada = str(convert_to_hours(GA.elite[c+6][1][3]))

    print(f'{voos[c]: <8}', '\t', ida_partida, '-', ida_chegada, f'{GA.elite[c][1][4]: >3} €\t', volta_partida,
          '-', volta_chegada, f'\t{GA.elite[c + 6][1][4]: >3} €')
    preco += int(GA.elite[c][1][4]) + int(GA.elite[c + 6][1][4])

print(f'Preço total: {preco} €')


f, ax = plt.subplots(figsize=(6,4))

ax.plot(GA.curva_boa, label='Melhor indivíduo')
ax.plot(GA.curva_ruim, label='Pior indivíduo')
ax.plot(GA.curva_media, label='Medio indivíduo')

ax.set(
    ylabel="Fitness",
    xlabel="Gerações"
)

ax.legend()

f.tight_layout()
f.savefig('./ind40_gera.png')
plt.show()

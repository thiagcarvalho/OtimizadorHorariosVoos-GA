def pop_inicial(self):
    pop = []
    for i in range(0, self.popsize):
        ind = individuo(self.df)
        ind.gera_aleatorio()
        ind.calc_fitness()
        pop.append(ind)

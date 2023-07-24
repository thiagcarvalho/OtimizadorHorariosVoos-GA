def gera_aleatorio(self):

    voos_ida = []
    voos_volta = []

    while len(self.aeroportos_visitados) < 6:

        voo = random.choice(list(self.df.items()))
        voo_ida = str(voo[1][0])

        if str(voo[1][0]) not in self.aeroportos_visitados and voo_ida != 'FCO':
            voos_ida.append(voo)
            self.aeroportos_visitados.add(str(voo[1][0]))

    voos_ida = sorted(voos_ida, key=lambda x: x[1][0])



	%Voos de volta
	
    while len(self.aeroportos_visitados) > 0:

        voo = random.choice(list(self.df.items()))
        voo_ida = str(voo[1][1])

        if voo_ida in self.aeroportos_visitados and str(voo[1][0]) == 'FCO':

            voos_volta.append(voo)
            self.aeroportos_visitados.remove(voo_ida)

    voos_volta = sorted(voos_volta, key=lambda x: x[1][1])

    self.ind = voos_ida + voos_volta
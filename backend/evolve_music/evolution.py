from soundtrack import Soundtrack


class Evolution:
    def __init__(self):
        self.individuals = []
        number_of_individuals = 10
        for i in range(0, number_of_individuals):
            self.individuals.append(Soundtrack())
        self.ranked_individuals = self.individuals

    def rank_generation(self, ranks: list):
        if len(ranks) != len(self.ranked_individuals):
            return
        for individual_id, rank in enumerate(ranks):
            individual = self.ranked_individuals[individual_id]
            individual.set_rank(rank)

    def next_generation(self):
        pass

    def individuals_to_rank(self):
        return self.ranked_individuals

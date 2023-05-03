import random
from itertools import combinations
from deap import base, creator, tools
from src.team_selectors.GeneticSelector import GeneticSelector

class GeneticSelectorLimitedChanges(GeneticSelector):
    def __init__(self, player_data, budget, max_players, initial_team, max_changes):
        super().__init__(player_data, budget, max_players)
        self.initial_team = initial_team
        self.max_changes = max_changes

    def _crossover(self, individual1, individual2):
        # Custom crossover function that ensures the number of changes is limited
        common_players = set(individual1).intersection(set(individual2))
        new_individual1 = list(common_players) + random.sample(set(individual1) - common_players, self.max_changes)
        new_individual2 = list(common_players) + random.sample(set(individual2) - common_players, self.max_changes)
        return (new_individual1, new_individual2)

    def select_team(self):
        # Modify the existing Genetic Algorithm to use the custom crossover function
        toolbox = base.Toolbox()
        toolbox.register("mate", self._crossover)
        
        # Other Genetic Algorithm operators remain the same
        toolbox.register("select", tools.selTournament, tournsize=3)
        toolbox.register("mutate", tools.mutFlipBit, indpb=0.1)
        toolbox.register("evaluate", self._eval_team)

        # Create the initial population
        population = [self._create_individual() for _ in range(self.pop_size)]

        # Run the genetic algorithm
        hof = tools.HallOfFame(1)
        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("avg", np.mean)
        stats.register("min", np.min)
        stats.register("max", np.max)

        population, log = algorithms.eaSimple(population, toolbox, cxpb=self.crossover_prob, mutpb=self.mutation_prob, ngen=self.n_generations, stats=stats, halloffame=hof, verbose=True)

        # Get the best individual
        best_individual = hof[0]

        # Decode the best individual to get the selected team
        selected_team = self._decode(best_individual)
        return selected_team

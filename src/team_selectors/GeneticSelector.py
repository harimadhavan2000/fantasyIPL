import random
import numpy as np
import pandas as pd
from deap import creator, base, tools, algorithms

class GeneticSelector:
    def __init__(self, player_data, budget, max_players):
        self.player_data = player_data
        self.budget = budget
        self.max_players = max_players

    def select_team(self):
        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMax)

        toolbox = base.Toolbox()

        # Attribute generator
        toolbox.register("attr_bool", random.randint, 0, 1)

        # Structure initializers
        toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, len(self.player_data))
        toolbox.register("population", tools.initRepeat, list, toolbox.individual)

        # Evaluation function
        def eval_team(individual):
            total_points = 0
            total_cost = 0
            role_counts = {'Batsman': 0, 'Bowler': 0, 'All-rounder': 0, 'Wicketkeeper': 0}

            for i in range(len(individual)):
                if individual[i]:  # Player is included in the team
                    total_points += self.player_data.iloc[i]['Predicted Points']
                    total_cost += self.player_data.iloc[i]['Cost']
                    role_counts[self.player_data.iloc[i]['Player Role']] += 1

            # Check if the constraints are satisfied
            if total_cost > self.budget or any(count > max_count for count, max_count in zip(role_counts.values(), [5, 5, 3, 1])):
                return 0,

            return total_points,

        # Operators
        toolbox.register("mate", tools.cxTwoPoint)
        toolbox.register("mutate", tools.mutFlipBit, indpb=0.1)
        toolbox.register("select", tools.selTournament, tournsize=3)
        toolbox.register("evaluate", eval_team)

        # Genetic algorithm parameters
        pop_size = 200
        crossover_prob = 0.7
        mutation_prob = 0.3
        n_generations = 100

        # Initialize the population
        pop = toolbox.population(n=pop_size)

        # Run the genetic algorithm
        hof = tools.HallOfFame(1)
        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("avg", np.mean)
        stats.register("min", np.min)
        stats.register("max", np.max)

        pop, log = algorithms.eaSimple(pop, toolbox, cxpb=crossover_prob, mutpb=mutation_prob, ngen=n_generations, stats=stats, halloffame=hof, verbose=True)

        best_individual = hof[0]

        # Create the best team
        selected_team = []
        for i in range(len(best_individual)):
            if best_individual[i]:
                player_name = self.player_data.iloc[i]['Player']
                player_role = self.player_data.iloc[i]['Player Role']
                player_cost = self.player_data.iloc[i]['Cost']
                selected_team.append((player_name, player_role, player_cost))

        return selected_team

# Instantiate the GeneticSelector class
genetic_selector = GeneticSelector(ipl_extended_stats_df, budget=100, max_players=11)

# Select the best team using the Genetic Algorithm
best_genetic_team = genetic_selector.select_team

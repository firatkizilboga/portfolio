from snakegame.game import Game
from snakegame.snake import Snake
from snakegame.brain import Brain
import time

class Evolver():
    def __init__(self):
        self.population_size = 100
        self.max_generations = 300
        self.mutation_rate = 0.3
        self.max_frames_playback = 600
        self.max_frames_training = 300
        self.generation = 0
        self.population = []
        
        for _ in range(self.population_size):
            snake = Snake()
            snake.brain = Brain()
            self.population.append(snake)


    def simulate_generation(self):
        for snake in self.population:
            game = Game()
            game.snake = snake
            frames = 0
            while (not game.game_over) and (game.frames < self.max_frames_training):
                game.step()
            game.snake = snake
            game.snake.fitness = game.fitness()

        self.generation += 1

    #order the population descending by fitness
    def order_population(self):
        self.population.sort(key=lambda snake: snake.fitness, reverse=True)


    def print_stats(self):
        best_fitness = self.population[0].fitness
        average_fitness = sum([snake.fitness for snake in self.population]) / len(self.population)
        print("Generation: {}, best fitness: {}, average fitness: {}".format(self.generation, best_fitness, average_fitness))

    def playback(self):
        game = Game()
        game.snake = self.population[0]
        frame = 0
        while (not game.game_over) and (game.frames<self.max_frames_playback):
            game.display()
            self.print_stats()
            time.sleep(0.05)
            game.step()
            frame += 1


        
    def reset_population(self):
        for snake in self.population:
            snake.reset()

    def evolve(self):
        snakes = []

        while self.generation < self.max_generations:
            self.simulate_generation()
            self.order_population()
            self.print_stats()
            new_population = []
            #mutate the top %20 of population
            for i in range(int(self.population_size * 0.2)):
                new_population.append(self.population[i])
                for _ in range(4):
                    snake = self.population[i].mutate(self.mutation_rate)
                    new_population.append(snake)
            self.population = new_population
            self.reset_population()
            snakes.append(self.population[0])
        return snakes
    
    def test(self):
        return ["test!!","teaisda"]
    

    @staticmethod
    def from_json(json):
        evolver = Evolver()
        evolver.population_size = int(json["population_size"])
        evolver.max_generations = int(json["max_generations"])
        evolver.mutation_rate = float(json["mutation_rate"])
        evolver.max_frames_playback = int(json["max_frames_playback"])
        evolver.max_frames_training = int(json["max_frames_training"])

        return evolver
    
    def to_json(self):
        return {
            "population_size": self.population_size,
            "max_generations": self.max_generations,
            "mutation_rate": self.mutation_rate,
        }
    
if __name__ == "__main__":
    evolver = Evolver()
    evolver.evolve()
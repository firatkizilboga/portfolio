from snake_game.game import Game
from snake_game.snake import Snake
from snake_game.brain import Brain
import time

class Evolver():
    def __init__(self, population_size=50, max_generations=300):
        self.population_size = population_size
        self.max_generations = max_generations
        self.population = []
        self.generation = 0

        for _ in range(self.population_size):
            snake = Snake()
            snake.brain = Brain()
            self.population.append(snake)

    def simulate_generation(self):
        for snake in self.population:
            game = Game()
            game.snake = snake
            frames = 0
            while (not game.game_over) and (game.frames < 600):
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
        while (not game.game_over) and (game.frames<600):
            game.display()
            self.print_stats()
            time.sleep(0.05)
            game.step()
            frame += 1

        
    def reset_population(self):
        for snake in self.population:
            snake.reset()

    def evolve(self):
        while self.generation < self.max_generations:
            self.simulate_generation()
            self.order_population()
            #self.playback()
            new_population = []
            #mutate the top %20 of population
            for i in range(int(self.population_size * 0.2)):
                new_population.append(self.population[i])
                for _ in range(4):
                    snake = self.population[i].mutate()
                    new_population.append(snake)
            self.population = new_population
            self.reset_population()
        
        self.order_population()
        self.playback()
    def test(self):
        return ["test!!","teaisda"]
if __name__ == "__main__":
    evolver = Evolver()
    evolver.evolve()
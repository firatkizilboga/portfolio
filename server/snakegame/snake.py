try:
    from brain import Brain
except ModuleNotFoundError:
    from snakegame.brain import Brain

class Snake():
    def __init__(self, brain = None):
        self.direction = [-1, 0]
        self.cells = [[5,5]]
        if brain is None:
            self.brain = Brain()
        else:
            self.brain = brain
        self.score = 0
        self.turns = 0
        self.fitness = 0
        self.unique_cell_discovered = set()

    def reset(self):
        brain = self.brain
        fitness = self.fitness
        self.__init__()
        self.brain = brain
        self.fitness = fitness

    def check_snake_food_intersection(self, food_location):
        if (self.cells[-1][0] == food_location[0]) and (self.cells[-1][1] == food_location[1]):
            return True
        return False
    
    def step(self, vision, food_location):
        new_direction = self.brain.predict(vision)
        if new_direction == [0,1,0]:
            new_direction = "forward"
        elif new_direction == [1,0,0]:
            new_direction = "left"
        elif new_direction == [0,0,1]:
            new_direction = "right"
        self.turn(new_direction)
        #(new_direction)
        
        self.move(food_location)
        #add new cell to unique_cell_discovered
        self.unique_cell_discovered.add(tuple(self.cells[-1]))


    def turn(self, direction): #left or right
        if direction == "forward":
            return
        if direction == "right":
            self.direction = [self.direction[1], -self.direction[0]]
        elif direction == "left":
            self.direction = [-self.direction[1], self.direction[0]]
        self.turns += 1
        
    def move(self, food_location):
        new_cell = [self.cells[-1][0] + self.direction[0], self.cells[-1][1] + self.direction[1]]
        self.cells.append(new_cell)
        
        grow = self.check_snake_food_intersection(food_location)
        if not grow:
            self.cells.pop(0)
        
        if grow:
            self.score += 1

    @staticmethod
    def from_json(json):
        snake = Snake()
        snake.direction = json["direction"]
        snake.score = json["score"]
        snake.frames_not_eaten = json["frames_not_eaten"]
        snake.turns = json["turns"]
        snake.cells = json["cells"]
        snake.brain = Brain.from_json(json["brain"])
        return snake
    
    def to_json(self):
        return {
            "score": self.score,
            "unique_cells_discovered": len(self.unique_cell_discovered),
            "turns": self.turns,
            "direction": self.direction,
            "cells": self.cells,
            "brain": self.brain.to_json()
        }

    
    
    def mutate(self, mutation_rate):
        #copy self  and mutate the copy
        snake = Snake()
        snake.brain = self.brain.mutate(mutation_rate)
        return snake

    #less than operator
    def __lt__(self, other):
        return self.fitness < other.fitness
    

    
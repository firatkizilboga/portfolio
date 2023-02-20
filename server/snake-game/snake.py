#import static functions
from brain import Brain
class Snake():
    def __init__(self):
        self.direction = [1, 0, 0, 0] #north, east, south, west
        self.cells = []
        self.brain = Brain()

    def turn(self, direction):
        #given a direction like left right or forward turn the snake in that direction
        if direction[0] == 1:
            if self.direction[0] == 1:
                self.direction = [0, 0, 0, 1]
            elif self.direction[1] == 1:
                self.direction = [1, 0, 0, 0]
            elif self.direction[2] == 1:
                self.direction = [0, 1, 0, 0]
            elif self.direction[3] == 1:
                self.direction = [0, 0, 1, 0]
        elif direction[2] == 1:
            if self.direction[0] == 1:
                self.direction = [0, 1, 0, 0]
            elif self.direction[1] == 1:
                self.direction = [0, 0, 1, 0]
            elif self.direction[2] == 1:
                self.direction = [0, 0, 0, 1]
            elif self.direction[3] == 1:
                self.direction = [1, 0, 0, 0]
        elif direction[1] == 1:
            pass

    #add a new [x,y] cell to the snake in the direction its moving north increments y south decrements y west decrements x east increments x and remove bottom
    def move(self):
        if self.direction[0] == 1:
            self.cells.append([self.cells[-1][0], self.cells[-1][1] + 1])
        elif self.direction[1] == 1:
            self.cells.append([self.cells[-1][0] + 1, self.cells[-1][1]])
        elif self.direction[2] == 1:
            self.cells.append([self.cells[-1][0], self.cells[-1][1] - 1])
        elif self.direction[3] == 1:
            self.cells.append([self.cells[-1][0] - 1, self.cells[-1][1]])
        self.cells.pop(0)

        #return head
        return self.cells[-1]
    
    #add a new [x,y] cell to the snake in the direction its moving north increments y south decrements y west decrements x east increments x
    def grow(self):
        if self.direction[0] == 1:
            self.cells.append([self.cells[-1][0], self.cells[-1][1] + 1])
        elif self.direction[1] == 1:
            self.cells.append([self.cells[-1][0] + 1, self.cells[-1][1]])
        elif self.direction[2] == 1:
            self.cells.append([self.cells[-1][0], self.cells[-1][1] - 1])
        elif self.direction[3] == 1:
            self.cells.append([self.cells[-1][0] - 1, self.cells[-1][1]])
            
        #return head
        return self.cells[-1]

    @staticmethod
    def from_json(json):
        snake = Snake()
        snake.direction = json["direction"]
        snake.cells = json["cells"]
        snake.brain = Brain.from_json(json["brain"])
        return snake

    def to_json(self):
        return {
            "direction": self.direction,
            "cells": self.cells,
            "brain": self.brain.to_json(),
        }



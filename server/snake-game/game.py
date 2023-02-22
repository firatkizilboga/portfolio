import numpy as np
from snake import Snake
import utils
class Game():
    def __init__(self,width = 10, height = 10, snake = None):
        if snake is None:
            snake = Snake()
        self.width = width
        self.height = height
        self.snake = snake
        self.food = self.get_random_food()
        self.game_over = False
        self.frames = 0
        self.frames_not_eaten = 0
        self.seen_food = False

    def to_json(self):
        return {
            "width": self.width,
            "height": self.height,
            "snake": self.snake.to_json(),
            "food": self.food,
            "score": self.score,
            "game_over": self.game_over
        }

    @staticmethod
    def from_json(json):
        game = Game()
        game.width = json["width"]
        game.height = json["height"]
        game.snake = Snake.from_json(json["snake"])
        game.food = json["food"]
        game.score = json["score"]
        game.game_over = json["game_over"]
        return game

    def check_snake_food_intersection(self):
        if (self.snake.cells[-1][0] == self.food[0]) and (self.snake.cells[-1][1] == self.food[1]):
            return True
        return False
    
    def check_snake_outside(self):
        if self.snake.cells[-1][0] < 0 or self.snake.cells[-1][0] >= self.width or self.snake.cells[-1][1] < 0 or self.snake.cells[-1][1] >= self.height:
            return True
        return False
        
    
    def check_snake_self_intersection(self):
        if self.snake.cells[-1] in self.snake.cells[:-1]:
            return True
        return False
        
    def step(self):
        self.frames += 1
        vision = self.get_vision()
        
        self.snake.step(vision, food_location = self.food)

        if self.check_snake_outside() or self.check_snake_self_intersection():
            self.game_over = True

        if self.check_snake_food_intersection():
            self.food = self.get_random_food()
        
    def get_random_food(self):
        food = [np.random.randint(0, self.width), np.random.randint(0, self.height)]
        while food in self.snake.cells:
            food = [np.random.randint(0, self.width), np.random.randint(0, self.height)]
        return food


    def get_vision(self):
        # 1 = wall or snake
        # 2 = food

        #for every direction, check if there is a wall, snake or food in that direction
        #if there is a wall/snake or food in that direction then vision['direction'] = [1, 0, distance] or [0, 1, distance]
        rays = {
            "north": 0,
            "east": 0,
            "south": 0,
            "west": 0
        }

        #shoot rays in every direction and see if they hit a wall/snake or food and compute the distance to that object
        #north
        head = self.snake.cells[-1]
        for direction in [[1,0], [-1,0], [0,1], [0,-1]]:
            new_head = self.snake.cells[-1].copy()
            #continue while new head is smaller than the width and height of the game or bigger than -1
            while True:
                new_head = [new_head[0] + direction[0], new_head[1] + direction[1]]
                if new_head[0] < 0 or new_head[0] >= self.width or new_head[1] < 0 or new_head[1] >= self.height:
                    rays[utils.array_to_direction(direction)] = [1, 0, utils.distance(head, new_head)]
                    break
                if new_head in self.snake.cells:
                    rays[utils.array_to_direction(direction)] = [1, 0, utils.distance(head, new_head)]
                    break
                if new_head == self.food:
                    rays[utils.array_to_direction(direction)] = [0, 1, utils.distance(head, new_head)]
                    break
                
        vision = {}
        snake_direction = utils.array_to_direction(self.snake.direction)

        if snake_direction == "north":
            vision["left"] = rays["west"]
            vision["forward"] = rays["north"]
            vision["right"] = rays["east"]
        elif snake_direction == "east":
            vision["left"] = rays["north"]
            vision["forward"] = rays["east"]
            vision["right"] = rays["south"]
        elif snake_direction == "south":
            vision["left"] = rays["east"]
            vision["forward"] = rays["south"]
            vision["right"] = rays["west"]
        elif snake_direction == "west":
            vision["left"] = rays["south"]
            vision["forward"] = rays["west"]
            vision["right"] = rays["north"]

        
        #turn the vision into a state where the state is a 1D array of 9 elements that is concatenated from the 3 elements of the 3 rays

        vision_fixed = []
        for key in vision:
            for element in vision[key]:
                vision_fixed.append(element)
        #if one of indexes 1 4 7 are 1 set self.seen_food to true
        if vision_fixed[1] == 1 or vision_fixed[4] == 1 or vision_fixed[7] == 1:
            self.seen_food = True
        return vision_fixed

    def display(self):
        
        print("\033[H\033[J")
        #print walls and snake and food
        for i in range(-1,self.height+1):
            for j in range(-1,self.width+1):
                if [j, i] in self.snake.cells:
                    print("X", end="")
                elif [j, i] == self.food:
                    print("O", end="")
                elif j == -1 or j == self.width or i == -1 or i == self.height:
                    print("#", end="")
                else:
                    print(" ", end="")
            print()

        print("Score: ", self.snake.score)
        print("Game Over: ", self.game_over)
        print(self.get_vision())

    def fitness(self):
        if self.game_over:
            go=-1000
        else:
            go=0
        if self.seen_food and self.snake.score == 0:
            sf = -10
        else:
            sf = 0

        return self.snake.score*10 - self.frames_not_eaten * 2 + go + len(self.snake.unique_cell_discovered)*2 + sf
if __name__ == "__main__":
    game = Game()
    while True:
        direction = input("Enter direction: ")
        if direction == "w":
            direction = [1,0]
        elif direction == "d":
            direction = [0,1]
        elif direction == "s":
            direction = [-1,0]
        elif direction == "a":
            direction = [0,-1]
        game.snake.direction = direction

        game.step()
        game.display()
        if game.game_over:
            break

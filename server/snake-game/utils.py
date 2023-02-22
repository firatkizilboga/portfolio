import numpy as np
def array_to_direction(arr):
    if arr == [1, 0]:
        return "north"
    elif arr == [-1, 0]:
        return "south"
    elif arr == [0, 1]:
        return "west"
    elif arr == [0, -1]:
        return "east"
    else:
        raise Exception("Invalid direction")

def direction_to_array(direction):
    if direction == "north":
        return [1, 0]
    elif direction == "south":
        return [-1, 0]
    elif direction == "west":
        return [0, 1]
    elif direction == "east":
        return [0, -1]
    else:
        raise Exception("Invalid direction")
    
def distance(a, b):
    return np.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)


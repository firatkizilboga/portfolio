import numpy as np
#implements the desicion making of the snake
class Brain():
    def __init__(self):
        self.weights = [np.random.rand(9, 3), #input layer
                        np.random.rand(3,3)
                        ]
        self.bias = [
                    np.random.rand(3),
                    np.random.rand(3),
                    ]
    
    def predict(self, inputs):
        #multiply inputs by weights and add bias for every layer
        xw=np.array(inputs).ravel()
        for weights, bias in zip(self.weights, self.bias):
            xw = np.dot(xw,weights) + bias
        xw=xw.reshape(-1,1).tolist()
        #make the biggest value 1 and the rest 0
        xw[xw.index(max(xw))]=1
        for i in range(len(xw)):
            if xw[i]!=1:
                xw[i]=0

        return xw
     
    
    def to_json(self):
        weights = [layer.tolist() for layer in self.weights]
        bias = [layer.tolist() for layer in self.bias]
        return {
            "weights": weights,
            "bias": bias,
        }
    
    @staticmethod
    def from_json(json):
        brain = Brain()
        brain.weights = json["weights"]
        for l, layer in enumerate(brain.weights):
            brain.weights[l] = np.array(layer)
        
        brain.bias = json["bias"]
        for l, layer in enumerate(brain.bias):
            brain.bias[l] = np.array(layer)
        return brain
    
    def mutate(self):
        mutation_rate, mutation_amount = 0.2, 1
        #copy weights and bias
        weights = [layer.copy() for layer in self.weights]
        bias = [layer.copy() for layer in self.bias]

        for layer in weights:
            for row in layer:
                for i in range(len(row)):
                    if np.random.rand() < mutation_rate:
                        row[i] += np.random.rand()
        
        for layer in bias:
            for i in range(len(layer)):
                if np.random.rand() < mutation_rate:
                    layer[i] += np.random.rand()

        #create a new brain
        brain = Brain()
        brain.weights = weights
        brain.bias = bias

        return brain
import numpy as np
#implements the desicion making of the snake
class Brain():
    def __init__(self):
        self.weights = [np.random.rand(9, 6), #input layer
                        np.random.rand(6, 6), #hidden layer
                        np.random.rand(6, 3), #output layer
                        ]
        self.bias = [
                    np.random.rand(6),
                    np.random.rand(6),
                    np.random.rand(3),
                    ]
        
    def predict(self, inputs):
        #multiply inputs by weights and add bias for every layer
        xw=np.array(inputs).ravel()
        for l, layer in enumerate(self.layers):
            xw=np.dot(xw,layer) + self.bias[self.layers.index(l)]
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

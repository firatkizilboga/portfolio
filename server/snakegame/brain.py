import numpy as np
#implements the desicion making of the snake
class Brain():
    def __init__(self, network_arch):
        if network_arch is None:
            network_arch = [9, 3]
        
        self.network_arch = network_arch
        for i in range(len(network_arch)-1):
            if i==0:
                self.weights = [np.random.rand(network_arch[i], network_arch[i+1])]
            else:
                self.weights.append(np.random.rand(network_arch[i], network_arch[i+1]))


    def predict(self, inputs):
        #multiply inputs by weights and add bias for every layer
        xw=np.array(inputs).ravel()
        for weights in self.weights:
            xw = np.dot(xw,weights)
        xw=xw.reshape(-1,1).tolist()
        #make the biggest value 1 and the rest 0
        xw[xw.index(max(xw))]=1
        for i in range(len(xw)):
            if xw[i]!=1:
                xw[i]=0

        return xw
     
    
    def to_json(self):
        weights = [layer.tolist() for layer in self.weights]
        return {
            "weights": weights,
        }
    
    @staticmethod
    def from_json(json):
        brain = Brain(json["network_arch"])
        brain.weights = json["weights"]
        for l, layer in enumerate(brain.weights):
            brain.weights[l] = np.array(layer)
        return brain
    
    def mutate(self, mutation_rate=0.3):
        #copy weights and bias
        weights = [layer.copy() for layer in self.weights]

        for layer in weights:
            for row in layer:
                for i in range(len(row)):
                    if np.random.rand() < mutation_rate:
                        row[i] += np.random.rand()
        #create a new brain
        brain = Brain(self.network_arch)
        brain.weights = weights

        return brain
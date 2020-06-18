"""
tree
Author: Neil Balaskandarajah
Created on: 18/06/2020
Tree data structure for the solving algorithm
"""

class Tree():
    def __init__(self, head):
        self.layers = []
        self.layers.append(head)
        self.layer = 1

    def get_head(self):
        return layers[0]

    def get_layer(self):
        return self.layer
    
    def step_up(self):
        if self.layer == 1:
            raise Exception("Cannot step past first layer!")
        self.layer -= 1

    def step_down(self):
        self.layer += 1

    def add(self, x):
        if len(self.layers) < self.layer+1: 
            self.layers.append([])
        if isinstance(x, list):
            self.layers[self.layer].extend(x) #itertools.chain instead?
        else:
            self.layers[self.layer].append(x)

    def dump(self):
        for l in self.layers:
            print(l)

if __name__ == 'main':
    t = Tree(2)
    t.add(3)

    t.step_down()
    t.add([5,6])

    t.step_up()
    t.add(3)

    t.dump()
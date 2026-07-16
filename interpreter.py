import parser

class Interpreter():
    def __init__(self,node: list):
        self.node = node
        self.position = 0
        self.currentNode = self.node[self.position]
    def advance(self):
        if (self.position + 1 < len(self.node) - 1):
            self.position += 1
            self.currentNode = self.node[self.position]
    
    def consume(self,*types):
        pass
    def interpreter(self):
        pass
        
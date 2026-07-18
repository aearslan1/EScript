from parser import Parser
from lexer import Lexer
import sys

class Error():
    def __init__(self,text: str):
        self.text = text

    def head(self):#her hatada yazılacak olan dosya bilgisi ve hatalı konum.
        print(f"Dosya '{sys.argv[0]}'\n\t->")
    
    def syntaxError(self,content: str):
        self.head()
        print(f"Yazım Hatası > {content}")
        sys.exit(1)
    
    def variableError(self,content:str):
        self.head()
        print(f"Değişken Hatası > {content}")
        sys.exit(1)

class Interpreter():
    def __init__(self,node: tuple,text: str):
        self.node = node
        if self.node:
            self.position = 0
            self.currentNode = self.node[self.position]
            self.variables =self.variables = {
        ("ID", "x"): ("ValueNode", ("ID", "y")),
        ("ID", "y"): ("ValueNode", ("STRING", "Merh"))
    }
            self.functions = {}
            self.builtInFunctions = {}
            self.errorManager = Error(text)
        else:
            self.currentNode = None
        
    
    def advance(self):
        if (self.position + 1 < len(self.node)):
            self.position += 1
            self.currentNode = self.node[self.position]
        else:
            self.currentNode = None
    def resolve(self,valNode: tuple):
        valNodeType = valNode[0]
        
        if (valNodeType == "ListNode"):
            valList = []
            values = valNode[1]
            for pureValue in values:
                value = self.resolve(pureValue)
                valList.append(value)
            return valList

        elif (valNodeType == "ValueNode"):
            valNode = valNode[1]
            valDtype = valNode[0]
            valValue = valNode[1]
            
            if (valDtype == "STRING" or valDtype == "INT" or valDtype == "FLOAT" or valDtype == "BOOL"):
                return valValue

            elif (valDtype == "ID"):
                if valNode in self.variables:
                    value = self.variables[valNode]
                else:
                    self.errorManager.variableError(f"'{valValue}' isimli değişken bulunamadı")
                
                value = self.resolve(value)
                return value
            
            else:
                print(valNode)
        

    def printCommand(self):
        valueNodes = self.currentNode[1]
        willPrint = ""
        for valueNode in valueNodes:
            val = self.resolve(valueNode)
            willPrint += str(val)
        endParam = str(self.resolve(self.currentNode[2]))
        print(willPrint,end=endParam)
        
    def assignCommand(self):
        dataType = self.currentNode[1][1]
        varName = self.currentNode[2]
        valueList = self.currentNode[3]
        valueDtype = valueList[0]

        if (dataType == "tamsayı"):
            realDataType = int     
        elif (dataType == "metin"):
            realDataType = str   
        elif (dataType == "ondalık"):
            realDataType = float  
        elif (dataType == "mantıksal"):
            realDataType = bool

    

    def interpreter(self):
        while (self.currentNode != None):
            if (self.currentNode[0] == "PrintNode"):
                self.printCommand()
            
            elif (self.currentNode[0] == "AssignNode"):
                self.assignCommand()

            self.advance()

if __name__ == "__main__":
    with open("testNotepad.txt","r",encoding="utf-8") as file:
        content = file.readlines()
        content = "".join(content)

    eparser = Parser(content,Lexer(content).lexer()).parser()
    einterpreter = Interpreter(eparser,content).interpreter()
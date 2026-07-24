from parser import Parser
from lexer import Lexer
import sys


class Error():
    def __init__(self,text: str,pos = 0):
        self.text = text
        self.textList = text.split("\n")
        self.position = pos

    def head(self):#her hatada yazılacak olan dosya bilgisi ve hatalı konum.
        print(f"Dosya '{sys.argv[0]}'\n\t->{self.textList[self.position]}")
    
    def syntaxError(self,content: str):
        self.head()
        print(f"Yazım Hatası > {content}")
        sys.exit(1)
    
    def variableError(self,content: str):
        self.head()
        print(f"Değişken Hatası > {content}")
        sys.exit(1)
    
    def typeError(self,content: str):
        self.head()
        print(f"Tip Hatası > {content}")
        sys.exit(1)
    
    def divisionByZeroError(self,content: str):
        self.head()
        print(f"Sıfıra Bölünme Hatası > {content}")
        sys.exit(1)

    def valueError(self,content: str):
        self.head()
        print(f"Değer Hatası > {content}")
        sys.exit(1)

    def undefinedFunctionError(self,content: str):
        self.head()
        print(f"Tanımsız Fonksiyon Hatası > {content}")
        sys.exit(1)
class Interpreter():
    def __init__(self,text: str):
        self.node = ()
        self.text = text
        self.position = 0
        self.currentNode = ()
        self.variables = {}
        self.functions = {}
        self.builtInFunctions = {}
        self.errorManager = Error(text,self.position)
        self.turnToTypeMap = {int : "INT",
                                  float : "FLOAT",
                                  bool : "BOOL",
                                  str : "STRING",
                                  }

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
        if (valueList[1] is None):
            if (varName in self.variables):
                varValue = self.variables[varName]
                resolvedVal = self.resolve(varValue)
            else:
                self.errorManager.variableError(f"'{varName}' adında bir değişken bulunamadı")
        else:
            resolvedVal = self.resolve(valueList)
        
        if (dataType == "tamsayı"):
            try:
                resolvedVal = ("INT",int(resolvedVal))
            except ValueError:
                self.errorManager.typeError(f"değer 'tamsayı' tipine dönüştürülemiyor.")

        elif (dataType == "ondalık"):
            try:
                resolvedVal = ("FLOAT",float(resolvedVal))
            except ValueError:
                self.errorManager.typeError(f"değer 'ondalık' tipine dönüştürülemiyor") 
        
        elif (dataType == "metin"):
            try:
                resolvedVal = ("STRING",str(resolvedVal))
            except ValueError:
                self.errorManager.typeError(f"değer 'metin' tipine dönüştürülemiyor") 
        
        elif (dataType == "mantıksal"):            
            if (resolvedVal == "doğru" or resolvedVal == 1):
                rresult = "doğru"
            elif (resolvedVal == "yanlış" or resolvedVal == 0):
                rresult = "yanlış"
            
            else:
                self.errorManager.typeError(f"değer 'bool' tipine dönüştürülemiyor") 
            resolvedVal = ("BOOL",rresult)
  
        elif (dataType == "liste"):
            self.variables[varName] = valueList
            return
        self.variables[varName] = ("ValueNode",resolvedVal)
  
    def defineFunctionCommand(self):
        funcName = self.currentNode[1]
        params = self.currentNode[2]
        body = self.currentNode[3]
        self.functions[funcName] = {"params": params, "body": body}

    def addCommand(self):
        varName = self.currentNode[1]
        
        if varName in self.variables:
            addedVal = self.currentNode[2]
            varValue = self.variables[varName]
            if(varValue[0] == "ValueNode"):
                resolvedVarValue = self.resolve(varValue)
                resolvedAddedValue = self.resolve(addedVal)
                try:
                    result = resolvedVarValue + resolvedAddedValue
                except TypeError:
                    self.errorManager.typeError("bu iki değer birbiri ile toplanamaz")
                self.variables[varName] = ("ValueNode",(self.turnToTypeMap[type(result)],result))

            elif (varValue[0] == "ListNode"):
                varValueListValues = list(varValue[1])
                
                if (addedVal[0] == "ValueNode" and addedVal[1][0] == "ID"):
                    
                    addedVarName = addedVal[1]
                    if (addedVarName in self.variables):
                        varValue = self.variables[addedVarName]

                    else:
                        self.errorManager.variableError(f"'{varName}' isimli bir değişken bulunamadı")
                    varValueListValues.append(varValue)
            
                else:
                    varValueListValues.append(addedVal)
                self.variables[varName] = ("ListNode",varValueListValues)

                
            

        else:
            self.errorManager.variableError(f"'{varName[1]}' isimlli bir değişken bulunamadı")
       
    def minusCommand(self):
        varName = self.currentNode[1]
        
        if varName in self.variables:
            addedVal = self.currentNode[2]
            varValue = self.variables[varName]
            if(varValue[0] == "ValueNode"):
                resolvedVarValue = self.resolve(varValue)
                resolvedAddedValue = self.resolve(addedVal)
                try:
                    result = resolvedVarValue - resolvedAddedValue
                except TypeError:
                    self.errorManager.typeError("bu iki değer birbiri ile çıkarılamaz")
                self.variables[varName] = ("ValueNode",(self.turnToTypeMap[type(result)],result))
            elif (varValue[0] == "ListNode"):
                
                varValueListValues = list(varValue[1])
                if (addedVal[0] == "ValueNode" and addedVal[1][0] == "ID"):
                    print(varValueListValues)
                    addedVarName = addedVal[1]
                    if (addedVarName in self.variables):
                        varValue = self.variables[addedVarName]
                    
                    else:
                        self.errorManager.variableError(f"{varName} isimli bir değişken bulunamadı")
                    try:
                        
                        varValueListValues.remove(varValue)
                    except ValueError:
                        self.errorManager.valueError(f"{self.resolve(addedVal)} listede yok")
                else:

                    try:
                        varValueListValues.remove(addedVal)
                    except ValueError:
                        self.errorManager.valueError(f"{self.resolve(addedVal)} listede yok")
                self.variables[varName] = ("ListNode",varValueListValues)
        else:
            self.errorManager.variableError(f"'{varName[1]}' isimlli bir değişken bulunamadı")
    
    def multCommand(self):
        varName = self.currentNode[1]
        
        if varName in self.variables:
            addedVal = self.currentNode[2]
            varValue = self.variables[varName]
            if(varValue[0] == "ValueNode"):
                resolvedVarValue = self.resolve(varValue)
                resolvedAddedValue = self.resolve(addedVal)
                try:
                    result = resolvedVarValue * resolvedAddedValue
                except TypeError:
                    self.errorManager.typeError("bu iki değer birbiri ile çarpılamaz")
                self.variables[varName] = ("ValueNode",(self.turnToTypeMap[type(result)],result))

        
        else:
            self.errorManager.variableError(f"'{varName[1]}' isimlli bir değişken bulunamadı")
    
    def divCommand(self):
        varName = self.currentNode[1]
        
        if varName in self.variables:
            addedVal = self.currentNode[2]
            varValue = self.variables[varName]
            if(varValue[0] == "ValueNode"):
                resolvedVarValue = self.resolve(varValue)
                resolvedAddedValue = self.resolve(addedVal)
                if (resolvedAddedValue == 0):
                    self.errorManager.divisionByZeroError("herhangi bir sayı '0'a  bölünemez")
                
                try:
                    result = resolvedVarValue / resolvedAddedValue
                except TypeError:
                    self.errorManager.typeError("bu iki değer birbiri ile bölünemez")
                varResult = ("ValueNode",(self.turnToTypeMap[type(result)],result))
                if (result.is_integer()):
                    varResult = ("ValueNode",("INT",int(result)))
                self.variables[varName] = varResult
                
        
        else:
            self.errorManager.variableError(f"'{varName[1]}' isimlli bir değişken bulunamadı")
    
    def modCommand(self):
        varName = self.currentNode[1]
        
        if varName in self.variables:
            addedVal = self.currentNode[2]
            varValue = self.variables[varName]
            if(varValue[0] == "ValueNode"):
                resolvedVarValue = self.resolve(varValue)
                resolvedAddedValue = self.resolve(addedVal)
                if (resolvedAddedValue == 0):
                    self.errorManager.divisionByZeroError("herhangi bir sayı '0'a  bölünemez")
                
                try:
                    result = resolvedVarValue % resolvedAddedValue
                except TypeError:
                    self.errorManager.typeError("bu iki değer birbiri ile bölünemez")
                varResult = ("ValueNode",(self.turnToTypeMap[type(result)],result))
                if (result.is_integer()):
                    varResult = ("ValueNode",("INT",int(result)))
                self.variables[varName] = varResult
                
        
        else:
            self.errorManager.variableError(f"'{varName[1]}' isimlli bir değişken bulunamadı")
    def compareCommand(self):
        valValue1 = self.resolve(self.currentNode[1])
        valValue2 = self.resolve(self.currentNode[3])
        logicOp = self.currentNode[2]
        try:
            if (logicOp[0] == "EQ"):
                if (valValue1 == valValue2):
                    result = ("ValueNode",("BOOL","doğru"))
                else:
                    result = ("ValueNode",("BOOL","yanlış"))
            
            elif (logicOp[0] == "LT"):
                if (valValue1 < valValue2):
                    result = ("ValueNode",("BOOL","doğru"))
                else:
                    result = ("ValueNode",("BOOL","yanlış"))
        
            elif (logicOp[0] == "GT"):
                if (valValue1 > valValue2):
                    result = ("ValueNode",("BOOL","doğru"))
                else:
                    result = ("ValueNode",("BOOL","yanlış"))
            
            elif (logicOp[0] == "LE"):
                if (valValue1 <= valValue2):
                    result = ("ValueNode",("BOOL","doğru"))
                else:
                    result = ("ValueNode",("BOOL","yanlış"))
            
            elif (logicOp[0] == "GE"):
                if (valValue1 >= valValue2):
                    result = ("ValueNode",("BOOL","doğru"))
                else:
                    result = ("ValueNode",("BOOL","yanlış"))
            
            elif (logicOp[0] == "NEQ"):
                if (valValue1 != valValue2):
                    result = ("ValueNode",("BOOL","doğru"))
                else:
                    result = ("ValueNode",("BOOL","yanlış"))
        except TypeError:
            self.errorManager.typeError(f"({self.turnToTypeMap[type(valValue1)]}) ile ({self.turnToTypeMap[type(valValue2)]}) tipleri birbiri ile karşılaştırılamaz")
        
        self.variables[self.currentNode[4]] = result
   
    def andGateCommand(self):
        valValue1 = self.resolve(self.currentNode[1])
        valValue2 = self.resolve(self.currentNode[2])
        assignVar = self.currentNode[3]
        if (valValue1 == "doğru" and valValue2 == "doğru"):
            result = "doğru"
        else:
            result = "yanlış"


        self.variables[assignVar] = ("ValueNode",("BOOL",result))
    
    def orGateCommand(self):
        valValue1 = self.resolve(self.currentNode[1])
        valValue2 = self.resolve(self.currentNode[2])
        assignVar = self.currentNode[3]
        if (valValue1 == "doğru" or valValue2 == "doğru"):
            result = "doğru"
        else:
            result = "yanlış"


        self.variables[assignVar] = ("ValueNode",("BOOL",result))
    
    def xorGateCommand(self):
        valValue1 = self.resolve(self.currentNode[1])
        valValue2 = self.resolve(self.currentNode[2])
        assignVar = self.currentNode[3]
        
        if ((valValue1 == "doğru" and valValue2 == "yanlış") or (valValue1 == "yanlış" and valValue2 == "doğru")):
            result = "doğru"
        else:
            result = "yanlış"

        self.variables[assignVar] = ("ValueNode",("BOOL",result))
    
    def notGateCommand(self):
        value = self.resolve(self.currentNode[1])
        assignVar = self.currentNode[2]

        if (value == "doğru"):
            result = "yanlış"
        else:
            result = "doğru"

        self.variables[assignVar] = ("ValueNode",("BOOL",result))

    def ifCommand(self):
        valueResult = self.resolve(self.currentNode[1])
        ifBody = self.currentNode[2]
        elseBody = self.currentNode[3]
        if (valueResult == "doğru"):
            result = self.interpreter(ifBody)
            if(result == "BreakLoop"):
                return "BreakLoop"
        elif (not elseBody is None):
            result = self.interpreter(elseBody)
            if(result == "BreakLoop"):
                return "BreakLoop"

    def loopCommand(self):
        count = self.resolve(self.currentNode[1])
        loopBody = self.currentNode[2]

        for _ in range(count):
            result = self.interpreter(loopBody)
            if (result == "BreakLoop"):
                break
    
    def inputCommand(self):
        dataType = self.currentNode[1][1]
        varName = self.currentNode[2]
        resolvedVal = input()
        if (dataType == "tamsayı"):
            try:
                resolvedVal = ("INT",int(resolvedVal))
            except ValueError:
                self.errorManager.typeError(f"değer 'tamsayı' tipine dönüştürülemiyor.")

        elif (dataType == "ondalık"):
            try:
                resolvedVal = ("FLOAT",float(resolvedVal))
            except ValueError:
                self.errorManager.typeError(f"değer 'ondalık' tipine dönüştürülemiyor") 
        
        elif (dataType == "metin"):
            try:
                resolvedVal = ("STRING",str(resolvedVal))
            except ValueError:
                self.errorManager.typeError(f"değer 'metin' tipine dönüştürülemiyor") 
        
        elif (dataType == "mantıksal"): 
            if (resolvedVal == "doğru" or resolvedVal == 1):
                rresult = "doğru"
            elif (resolvedVal == "yanlış" or resolvedVal == 0):
                rresult = "yanlış"
            
            else:
                self.errorManager.typeError(f"değer 'bool' tipine dönüştürülemiyor") 
            resolvedVal = ("BOOL",rresult)

        self.variables[varName] = ("ValueNode",resolvedVal)


    def interpreter(self,nodes: tuple):
        if not nodes:
            return

        for position,node in enumerate(nodes):
            self.position = position
            self.currentNode = node
            nodeType = self.currentNode[0]
            self.errorManager = Error(self.text,self.position)

            if nodeType == "PrintNode":
                self.printCommand()
            elif nodeType == "AssignNode":
                self.assignCommand()
            elif nodeType == "FunctionDefineNode":
                self.defineFunctionCommand()
            elif nodeType == "AddNode":
                self.addCommand()
            elif nodeType == "MinusNode":
                self.minusCommand()
            elif nodeType == "MultNode":
                self.multCommand()
            elif nodeType == "DivNode":
                self.divCommand()
            elif nodeType == "ModNode":
                self.modCommand()
            elif nodeType == "CompareNode":
                self.compareCommand()
            elif nodeType == "AndGateNode":
                self.andGateCommand()
            elif nodeType == "OrGateNode":
                self.orGateCommand()
            elif nodeType == "XorGateNode":
                self.xorGateCommand()
            elif nodeType == "NotGateNode":
                self.notGateCommand()
            elif nodeType == "IfNode":
                result = self.ifCommand()
                if (result == "BreakLoop"):
                    return "BreakLoop"
                    
                
            elif nodeType == "InputNode":
                self.inputCommand()
            elif nodeType == "LoopNode":
                self.loopCommand()
            elif nodeType == "BreakNode":
                return "BreakLoop"

            elif nodeType == "ReturnNode":
                return self.currentNode
            
            else:
                self.errorManager.syntaxError(f"'{self.currentNode}' bilinmeyen komut.")
if __name__ == "__main__":
    with open("testNotepad.txt","r",encoding="utf-8") as file:
        content = file.readlines()
        content = "".join(content)

    eparser = Parser(content,Lexer(content).lexer()).parser()
    einterpreter = Interpreter(content).interpreter(eparser)

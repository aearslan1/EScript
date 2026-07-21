import lexer
import sys

class Error():
    def __init__(self,text: str):
        self.text = text

    def head(self):#her hatada yazılacak olan dosya bilgisi ve hatalı konum.
        print(f"Dosya '{sys.argv[0]}'\n\t->{self.text}")
    
    def syntaxError(self,content: str):
        self.head()
        print(f"Yazım Hatası > {content}")
        sys.exit(1)

class Parser():
    def __init__(self,text: str,tokens: list):
        self.tokens = tokens
        self.functionMode = False
        self.position = 0
        self.currentToken = self.tokens[self.position]
        self.errorManager = Error(text) 
        self.endTokens = ["RBRACE","NEWLINE","EOF"]
    def valueNode(self):
        if (self.currentToken[0] == "LBRACKET"):
            self.consume("LBRACKET")
            values = []
            while (not self.currentToken[0] in self.endTokens and self.currentToken[0] != "RBRACKET"):
                value = self.valueNode()
                values.append(value)
                if (not self.currentToken[0] == "RBRACKET"):
                    self.consume("COMMA")
                else:
                    self.consume("RBRACKET")
                    break
                
            return ("ListNode",values)

        else:
            value = self.consume("INT","FLOAT","STRING","BOOL","ID")
            if (value[0] == "ID" and self.currentToken[0] == "LPAREN"):
                self.consume("LPAREN")
                params = []
                while (not self.currentToken[0] in self.endTokens and self.currentToken[0] != "RPAREN"):
                    param = self.valueNode()
                    params.append(param)
                    if (not self.currentToken[0] == "RPAREN"):
                        self.consume("COMMA")
                self.consume("RPAREN")
                value = ("FunctionCall",params)
            
        
        node = ("ValueNode",value)
        return node
    def lookAhead(self,offset = 1):
        if (self.position + offset < len(self.tokens)):
            return self.tokens[self.position + offset][0]
        return None
    def consume(self,*types):
        if (self.currentToken[0] in types):
            val = self.currentToken
            self.advance()
            return val
        else:
            self.errorManager.syntaxError(f"beklenmeyen token '{",".join(types)}' tokenleri bekleniyordu '{self.currentToken[0]}' geldi.")
        
    def advance(self):
        if (self.position + 1 < len(self.tokens)):
            self.position += 1
            self.currentToken = self.tokens[self.position]
        else:
            self.currentToken = None

    def parser(self):
        node = []
        while(self.currentToken[0] != "EOF"):
            if (self.functionMode and self.currentToken[0] == "RBRACE"):
                break
            if (self.currentToken[0] == "PRINT_COMMAND"):
                self.consume("PRINT_COMMAND")
                willPrintValues = []
                self.consume("LT")
                
                while (not self.currentToken[0] in self.endTokens and self.currentToken[0] != "LT"):
                    value = self.valueNode()
                    willPrintValues.append(value)
                    if (not self.currentToken[0] in self.endTokens and self.currentToken[0] != "LT"):
                          self.consume("PLUS","COMMA")
                
                if (self.currentToken[0] == "LT"):
                    self.consume("LT")
                    end = self.valueNode()
                else:
                    end = ("ValueNode",("STRING","\n"))
                
                    
                node.append(("PrintNode",willPrintValues,end))
            elif (self.currentToken[0] == "ASSIGN_COMMAND"):
                self.consume("ASSIGN_COMMAND")
                willPrintValues = []
                self.consume("LT")
                dtype = self.consume("DTYPE")
                self.consume("LT")
                varName = self.consume("ID")

                if (self.currentToken[0] == "ASSIGN"):
                    self.consume("ASSIGN")
                    value = self.valueNode()
                else:
                    value = ("ValueNode",None)

                if (self.functionMode):
                    if (not self.currentToken[0] in self.endTokens):
                        self.errorManager.syntaxError("fazla token tespit edildi.")
                else:
                    if (not self.currentToken[0] in ["NEWLINE","EOF"]):
                        self.errorManager.syntaxError(f"fazla token tespit edildi '{self.currentToken[0]}'")
                node.append(("AssignNode",dtype,varName,value))
            
            elif (self.currentToken[0] == "ADD_COMMAND"):
                self.consume("ADD_COMMAND")
                willPrintValues = []
                self.consume("LT")
                varName = self.consume("ID")
                self.consume("COMMA")
                value = self.valueNode()
                node.append(("AddNode",varName,value))


            elif (self.currentToken[0] == "MINUS_COMMAND"):
                self.consume("MINUS_COMMAND")
                willPrintValues = []
                self.consume("LT")
                varName = self.consume("ID")
                self.consume("COMMA")
                value = self.valueNode()
                node.append(("MinusNode",varName,value))
            
            elif (self.currentToken[0] == "MULT_COMMAND"):
                self.consume("MULT_COMMAND")
                willPrintValues = []
                self.consume("LT")
                varName = self.consume("ID")
                self.consume("COMMA")
                value = self.valueNode()
                node.append(("MultNode",varName,value))
          
            elif (self.currentToken[0] == "DIV_COMMAND"):
                self.consume("DIV_COMMAND")
                willPrintValues = []
                self.consume("LT")
                varName = self.consume("ID")
                self.consume("COMMA")
                value = self.valueNode()
                node.append(("DivNode",varName,value))

            elif (self.currentToken[0] == "FUNCTIONDEFINE_COMMAND"):
                self.functionMode = True
                self.consume("FUNCTIONDEFINE_COMMAND")
                funcName = self.consume("ID")
                self.consume("LPAREN")
                params = []
                while (not self.currentToken[0] in self.endTokens and self.currentToken[0] != "RPAREN"):
                    param = self.consume("ID")
                    params.append(param)
                    if (not self.currentToken[0] in self.endTokens and self.currentToken[0] != "RPAREN"):
                          self.consume("COMMA")
                self.consume("RPAREN")
                self.consume("LBRACE")
                while (self.currentToken[0] != "EOF" and self.currentToken[0] != "RBRACE"):
                    functionNode = self.parser()
                self.consume("RBRACE")

                node.append(("FunctionDefineNode",funcName,params,functionNode))

            elif (self.currentToken[0] == "RETURN_COMMAND"):
                self.consume("RETURN_COMMAND")
                if (not self.functionMode):
                    self.errorManager.syntaxError("'döndür' komutu sadece fonksiyon içinde çalışabilir")
                value = self.valueNode()
                node.append(("ReturnNode",value))
                self.consume("NEWLINE","RBRACE")
            
            elif (self.currentToken[0] == "ID"):
                funcName = self.consume("ID")
                self.consume("LPAREN")
                params = []
                while (not self.currentToken[0] in self.endTokens and self.currentToken[0] != "RPAREN"):
                    param = self.valueNode()
                    params.append(param)
                    if (not self.currentToken[0] == "RPAREN"):
                        self.consume("COMMA")
                node.append(("FunctionCallNode",funcName,params))
            
            elif (self.currentToken[0] == "AND_GATE"):
                self.consume("AND_GATE")
                self.consume("LT")
                varName = self.valueNode()
                self.consume("COMMA")
                value = self.valueNode()
                self.consume("LT")

                assignVar = self.consume("ID")
                node.append(("AndGateNode",varName,value,assignVar))
            
            elif (self.currentToken[0] == "OR_GATE"):
                self.consume("OR_GATE")
                self.consume("LT")
                varName = self.valueNode()
                self.consume("COMMA")
                value = self.valueNode()
                self.consume("LT")

                assignVar = self.consume("ID")
                node.append(("OrGateNode",varName,value,assignVar))
            
            elif (self.currentToken[0] == "XOR_GATE"):
                self.consume("XOR_GATE")
                self.consume("LT")
                varName = self.valueNode()
                self.consume("COMMA")
                value = self.valueNode()
                self.consume("LT")

                assignVar = self.consume("ID")
                node.append(("XorGateNode",varName,value,assignVar))
            
            elif (self.currentToken[0] == "NOT_GATE"):
                self.consume("NOT_GATE")
                self.consume("LT")
                varName = self.valueNode()
                self.consume("LT")
                assignVar = self.consume("ID")
                node.append(("NotGateNode",varName,assignVar))
            
            elif (self.currentToken[0] == "COMPARE_COMMAND"):
                self.consume("COMPARE_COMMAND")
                self.consume("LT")
                self.consume("LPAREN")
                val1 = self.valueNode()
                logicOp = self.consume("LT","EQ","NEQ","GT","LE","GE")
                val2 = self.valueNode()
                self.consume("RPAREN")
                self.consume("LT")
                assignVar = self.consume("ID")
                node.append(("CompareNode",val1,logicOp,val2,assignVar))
            
            elif (self.currentToken[0] == "IF_COMMAND"):
                self.functionMode = True
                self.consume("IF_COMMAND")
                result = self.valueNode()
                self.consume("LBRACE")
                ifBody = []
                while (self.currentToken[0] != "EOF" and self.currentToken[0] != "RBRACE"):
                    ifBody.extend(self.parser())
                
                self.consume("RBRACE")

                while (self.currentToken and self.currentToken[0] == "NEWLINE"):
                    self.advance()
                elseBody = None
                if (self.currentToken[0] == "ELSE_COMMAND"):
                    self.consume("ELSE_COMMAND")
                    self.consume("LBRACE")
                    elseBody = []
                    while (self.currentToken[0] != "EOF" and self.currentToken[0] != "RBRACE"):
                        elseBody.extend(self.parser())
                    self.consume("RBRACE")
                node.append(("IfNode",result,ifBody,elseBody))
                self.functionMode = False
            elif (self.currentToken[0] == "INPUT_COMMAND"):
                self.consume("INPUT_COMMAND")
                self.consume("LT")
                dtype = self.consume("DTYPE")
                self.consume("LT") 
                varName = self.consume("ID")
                node.append(("InputNode",dtype,varName))
            else:
                self.advance()
        return node

if __name__ == "__main__":
    with open("testNotepad.txt","r",encoding="utf-8") as file:
        content = file.readlines()
        content = "".join(content)

    eparser = Parser(content,lexer.Lexer(content).lexer())
    node = eparser.parser()
    for i in node:
        print(i)
    
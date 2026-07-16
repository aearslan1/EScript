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
    def __init__(self,text: str):
        self.tokens = lexer.Lexer(text).lexer()
        self.nodes = []
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
                
            return ["ListNode",values]
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
            value = ["FunctionCall",params]
        node = ["ValueNode",value]
        return node
    def lookAhead(self,offset = 1):
        if (self.position + offset < len(self.tokens) - 1):
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
        while(self.currentToken[0] != "EOF"):
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
                    end = "\n"
                
                    
                self.nodes.append(["PrintNode",willPrintValues,end])
            else:
                self.advance()

if __name__ == "__main__":
    with open("testNotepad.txt","r",encoding="utf-8") as file:
        content = file.readlines()
        content = "".join(content)

    eparser = Parser(content)
    eparser.parser()
    print(eparser.nodes)
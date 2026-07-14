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

    def consume(self,*types):
        for i in types:
            if (i == self.currentToken[0]):
                return self.currentToken
            else:
                self.errorManager.syntaxError(f"beklenmeyen token,'{i}' bekleniyordu '{self.currentToken[0]}' geldi.")
    
    def advance(self):
        if (self.position + 1 < len(self.tokens)):
            self.position += 1
            self.currentLetter = self.text[self.position]
        else:
            self.currentToken = None

    def parser(self):
        pass


if __name__ == "__main__":
    with open("testNotepad.txt","r",encoding="utf-8") as file:
        content = file.readlines()
        content = "".join(content)

    eparser = Parser(content)
    eparser.parser()
    print(eparser.nodes)
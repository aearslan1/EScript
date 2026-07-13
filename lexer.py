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
    
class Lexer():
    def __init__(self,text: str):
        self.text = text
        self.position = 0
        self.currentLetter = self.text[self.position] #anlık harfi alıyoruz
        self.tokens = []
        self.errorManager = Error(self.text)

    def stringMod(self):
        stringPack = ""
        self.advance()
        while (not(self.currentLetter is None) and self.currentLetter != '"'):
            stringPack += self.currentLetter
            self.advance()
        if (self.currentLetter != '"'):
            self.errorManager.syntaxError("kapatılmamış bir tırnak var.")
        self.tokens.append(["STRING",stringPack])

        self.advance()
    
    def alphaMod(self):
        alphaPack = ""
        while (not(self.currentLetter is None) and self.currentLetter.isalpha()):
            alphaPack += self.currentLetter
            self.advance()
        self.tokens.append(["ALPHA",alphaPack])

    def numberMod(self):
        numberPack = ""
        isFloat = False
        while (not(self.currentLetter is None) and self.currentLetter.isdigit()):
            numberPack += self.currentLetter
            self.advance()
        self.tokens.append(["NUMBER",numberPack])
    def advance(self): #position'u bir kaydıran fonksiyon
        if (self.position + 1 < len(self.text)):
            self.position += 1
            self.currentLetter = self.text[self.position]
        else:
            self.currentLetter = None

    def lexer(self):
        while (not self.currentLetter is None):
            if (self.currentLetter.isalpha()):
                self.alphaMod()

            elif (self.currentLetter == '"'):
                self.stringMod()
            
            elif (self.currentLetter.isdigit()):
                self.numberMod()

            else:
                self.advance()
            
        if self.currentLetter is None:
            self.tokens.append(["EOF",None])
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
        self.tokens = []
        if text:
            self.text = text
            self.position = 0
            self.currentLetter = self.text[self.position] #anlık harfi alıyoruz
        
            self.errorManager = Error(self.text)
            self.dataTypes = ["tamsayı","ondalık","metin","mantıksal","liste"]
            self.basicCommandMap = {"yaz":"PRINT_COMMAND","yap":"ASSIGN_COMMAND","ekle":"ADD_COMMAND","fnk":"FUNCTIONDEFINE_COMMAND","çıkar":"MINUS_COMMAND","çarp":"MULT_COMMAND","böl":"DIV_COMMAND","mod":"MOD_COMMAND","eğer" : "IF_COMMAND","değilse":"ELSE_COMMAND","krş" : "COMPARE_COMMAND" ,"döndür":"RETURN_COMMAND","and":"AND_GATE","or":"OR_GATE","xor":"XOR_GATE","not":"NOT_GATE","giriş" : "INPUT_COMMAND","döngü":"LOOP_COMMAND","kır" : "BREAK_COMMAND"}
            self.outlierAlphaValues = ["_"]
            self.usefulSigns = {"+":"PLUS","-":"MINUS","*":"STAR","/":"SLASH","(":"LPAREN",")":"RPAREN","[":"LBRACKET","]":"RBRACKET","{":"LBRACE","}":"RBRACE","\n":"NEWLINE",".":"DOT",",":"COMMA",";":"SEMICOLON",":":"COLON"}
            self.advanceSigns = [" ", "\t", "\r"]
        else:
            self.currentLetter = None
    def stringMod(self):
        stringPack = ""
        self.advance()
        while (not(self.currentLetter is None) and self.currentLetter != '"'):
            if self.currentLetter == "\\":
                self.advance() 
                
                if self.currentLetter is None:
                    self.errorManager.syntaxError("kaçış karakterinden sonra metin aniden bitti.")
                if self.currentLetter == "n":
                    stringPack += "\n"
                elif self.currentLetter == "t":
                    stringPack += "\t"
                elif self.currentLetter == '"':
                    stringPack += '"' 
                elif self.currentLetter == "\\":
                    stringPack += "\\" 
                else:
                    stringPack += "\\" + self.currentLetter
            else:
                stringPack += self.currentLetter
            self.advance()
        if (self.currentLetter != '"'):
            self.errorManager.syntaxError("kapatılmamış bir tırnak var.")
        self.tokens.append(("STRING",stringPack))

        self.advance()
    
    def lookAhead(self,offset = 1):
        if (self.position + offset < len(self.text) ):
            return self.text[self.position + offset]
        return None

    def alphaMod(self):
        alphaPack = ""
        while (not(self.currentLetter is None) and (self.currentLetter.isalpha() or self.currentLetter in self.outlierAlphaValues)):
            alphaPack += self.currentLetter
            self.advance()
        
        if not self.currentLetter is None and self.currentLetter.isdigit():
            while (not(self.currentLetter is None) and (self.currentLetter.isalpha() or self.currentLetter in self.outlierAlphaValues or self.currentLetter.isdigit())):
                alphaPack += self.currentLetter
                self.advance()
        
        if alphaPack in self.basicCommandMap:
            self.tokens.append((self.basicCommandMap[alphaPack],alphaPack))
        elif alphaPack in self.dataTypes:
            self.tokens.append(("DTYPE",alphaPack))
        
        elif alphaPack == "doğru" or alphaPack == "yanlış":
            self.tokens.append(("BOOL",alphaPack))
            
        else:
            self.tokens.append(("ID",alphaPack))

    def numberMod(self):
        numberPack = ""
        isFloat = False
        if (self.currentLetter == "-"):
            numberPack += "-"
            self.advance()
        while (not(self.currentLetter is None) and self.currentLetter.isdigit()):
            numberPack += self.currentLetter
            self.advance()
        
        if self.currentLetter == ".":

            if self.lookAhead() is None or not self.lookAhead().isdigit():
                self.errorManager.syntaxError("tamamlanmamış bir float değeri var.")
            if self.lookAhead().isdigit():
                numberPack += "."
                isFloat =  True
                self.advance()
                while (not(self.currentLetter is None) and self.currentLetter.isdigit()):
                    numberPack += self.currentLetter
                    self.advance()
        
        if isFloat:
            self.tokens.append(("FLOAT",float(numberPack)))
        else:
            self.tokens.append(("INT",int(numberPack)))
           
    def advance(self): #position'u bir kaydıran fonksiyon
        if (self.position + 1 < len(self.text)):
            self.position += 1
            self.currentLetter = self.text[self.position]
        else:
            self.currentLetter = None

    def lexer(self):

        while (not self.currentLetter is None):
            if (self.currentLetter.isalpha() or self.currentLetter in self.outlierAlphaValues):
                self.alphaMod()

            elif (self.currentLetter == '"'):
                self.stringMod()
            
            elif (self.currentLetter.isdigit()):
                self.numberMod()

            else:
                if (self.currentLetter == "-"):
                    if (not self.lookAhead() is None and self.lookAhead().isdigit()):
                        self.numberMod()
                    else:
                        self.tokens.append(["MINUS","-"])
                        self.advance()
                    
                elif (self.currentLetter == "+"):
                    if (not self.lookAhead() is None and self.lookAhead().isdigit()):
                        self.advance()
                        self.numberMod()
                    else:
                        self.tokens.append(["PLUS","+"])
                        self.advance()
                
                elif (self.currentLetter == "="):
                    self.advance()
                    if self.currentLetter == "=":
                        self.tokens.append(["EQ","=="])
                        self.advance()
                    else:
                        self.tokens.append(["ASSIGN","="])
                
                elif (self.currentLetter == "!"):
                    self.advance()
                    if self.currentLetter == "=":
                        self.tokens.append(["NEQ","!="])
                        self.advance()
                    else:
                        self.errorManager.syntaxError(f"'!' bilinmeyen bir işaret.")    
                
                elif (self.currentLetter == "<"):
                    self.advance()
                    if self.currentLetter == "=":
                        self.tokens.append(["LE","<="])
                        self.advance()
                    else:
                        self.tokens.append(["LT","<"])
                
                elif (self.currentLetter == ">"):
                    self.advance()
                    if self.currentLetter == "=":
                        self.tokens.append(["GE",">="])
                        self.advance()
                    else:
                        self.tokens.append(["GT",">"])
                        
                elif (self.currentLetter in self.usefulSigns):
                    self.tokens.append([self.usefulSigns[self.currentLetter],self.currentLetter])
                    self.advance()
                
                else:
                    if self.currentLetter == "#":
                        while(not self.currentLetter is None and not self.currentLetter == "\n"):
                            self.advance()
                    elif self.currentLetter in self.advanceSigns:
                        self.advance()
                    else:
                        self.errorManager.syntaxError(f"'{self.currentLetter}' bilinmeyen bir işaret.")    
        if self.currentLetter is None:
            self.tokens.append(["EOF",None])
        return self.tokens
if __name__ == "__main__":
    with open("testNotepad.txt","r",encoding="utf-8") as file:
        content = file.readlines()
        content = "".join(content)

    elexer = Lexer(content)
    print(elexer.lexer())
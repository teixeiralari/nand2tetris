from JackTokens import *


class Tokenizer:

    __already_called = False
    __more_tokens_flag = False

    def __init__(self, file_path):
        self.__file = open(file_path)
        self.__char = ''
        self.__peek = self.__file.read(1)
        self.__current_token = None
        self.__current_type = None

    def next_char(self):
        self.__char = self.__peek
        self.__peek = self.__file.read(1)

    def advance(self):
        self.__already_called = False

        if self.__char.isalpha() or self.__char == "_": 
            self.__current_token = self.__char
            while self.__peek not in SYMBOLS and not self.__peek.isspace() and self.__peek != '':
                self.next_char()
                self.__current_token += self.__char
            self.__current_type = JTok.KEYWORD if self.__current_token in KEYWORDS else JTok.IDENTIFIER

        elif self.__char in SYMBOLS:
            self.__current_token = self.__char
            self.__current_type = JTok.SYMBOL

        elif self.__char == "\"": 
            self.__current_token = self.__char
            while self.__peek != "\"":
                self.next_char()
                self.__current_token += self.__char
            self.next_char()
            self.__current_token += self.__char
            self.__current_type = JTok.STRING_CONST

        elif self.__char.isdigit(): 
            self.__current_token = self.__char
            while self.__peek.isdigit():
                self.next_char()
                self.__current_token += self.__char
            self.__current_type = JTok.INT_CONST

       

    def has_more_tokens(self):
        if self.__already_called:
            return self.__more_tokens_flag

        if self.__peek == '':  
            self.__more_tokens_flag = False

        elif self.__peek == '/': 
            self.next_char()
            if self.__peek == '/':  
                while self.__char != '\n' and self.__char != '':
                    self.next_char()
                return self.has_more_tokens()

            elif self.__peek == '*':  
                self.next_char()
                self.next_char()
                while not (self.__char == '*' and self.__peek == '/'):
                    self.next_char()
                self.next_char()
                return self.has_more_tokens()

           
            self.__more_tokens_flag = True
            return self.__more_tokens_flag

        elif self.__peek.isspace():  
            while self.__peek.isspace():
                self.next_char()
            return self.has_more_tokens()

        else: 
            self.next_char()
            self.__more_tokens_flag = True

        self.__already_called = True
        return self.__more_tokens_flag

    def token_type(self):
        return self.__current_type

    def key_word(self):
        return self.__current_token

    def symbol(self):
        return self.__current_token

    def identifier(self):
        return self.__current_token

    def intVal(self):
        return int(self.__current_token)

    def string_val(self):
     return self.__current_token[1:-1]


from Tokenizer import Tokenizer
from xml.etree.ElementTree import Element, SubElement, tostring
from JackTokens import JackTokens as JTok
from JackTokens import *
from xml.dom import minidom
from SymbolTable import SymbolTable
from SymbolTable import Kind
from VMWriter import VMWriter

EXPRESSION = "expression"
EXPRESSION_LIST = "expressionList"
SYMBOL = "symbol"
TERM = "term"
INTEGER_CONSTANT = "integerConstant"
STRING_CONSTANT = "stringConstant"
KEYWORD = "keyword"
IDENTIFIER = "identifier"
SUBROUTINE_CALL = "subroutineCall"
CLASS = "class"
STATEMENTS = "statements"

CONSTANT = "constant"
TEMP = "temp"
POINTER = "pointer"
ARGUMENT = "argument"


class CompilationEngine:


    def __init__(self, source):
        self.if_counter = 0
        self.while_counter = 0
        self.tokenizer = Tokenizer(source)
        self.tokenizer.has_more_tokens()
        self.tokenizer.advance()
        self.symbols = SymbolTable()
        self.writer = VMWriter(source)
        self.arithmetic_op = {}
        self.init_op()
        self.root = Element(CLASS)
        self.class_name = ""
        self.compile_class(self.root)
        self.writer.close()

    def init_op(self):
        self.arithmetic_op = {'+': "add",
                         '-': "sub",
                         '*': "call Math.multiply 2",
                         '/': "call Math.divide 2",
                         '&': "and",
                         '|': "or",
                              '<': "lt",
                              '>': "gt",
                              '=': "eq"
                        }

    def next(self):
        """
        Proceed to the next token.
        :return:
        """
        if self.tokenizer.has_more_tokens():
            self.tokenizer.advance()

    def compile_expression(self,caller):
        """
        Compiles an expression.
        :param caller:
        :return:
        """
        op_stack = []
        self.compile_term(SubElement(caller,TERM))
        while self.tokenizer.token_type() is JTok.SYMBOL and self.tokenizer.symbol() in OPERATORS:
            op_stack.append(self.tokenizer.symbol())
            self.next()
            self.compile_term(SubElement(caller,TERM))

        while op_stack:
            self.writer.write_arithmetic(self.arithmetic_op[op_stack.pop()])

    def compile_expressionList(self,caller):
        num_of_args = 0
        #  if expression list is empty
        if self.tokenizer.token_type() is JTok.SYMBOL and self.tokenizer.symbol() == ")":
            caller.text = " "
            return num_of_args

        num_of_args += 1
        self.compile_expression(SubElement(caller,EXPRESSION))
        while self.tokenizer.token_type() is JTok.SYMBOL and self.tokenizer.symbol() == ",":
            #SubElement(caller,SYMBOL).text = self.tokenizer.symbol()
            num_of_args += 1
            self.next()
            self.compile_expression(SubElement(caller,EXPRESSION))
        return num_of_args

    def compile_subroutineCall(self,caller,first_token):
        func_name = first_token
        
        is_method = 0
        if self.tokenizer.symbol() == '.':
            self.next()
            if self.symbols.kind_of(func_name): 
                segment = self.symbols.kind_of(func_name)
                segment = Kind.get_segment(segment)
                index = self.symbols.index_of(func_name)
                self.writer.write_push(segment,index)
                func_name = self.symbols.type_of(func_name)
                is_method = 1

            func_name = func_name+"."+self.tokenizer.identifier()
            self.next()
        else:
            func_name = self.class_name+"."+func_name
            self.writer.write_push(POINTER,0)
            is_method = 1

        self.next()
        num_of_args = self.compile_expressionList(SubElement(caller, EXPRESSION_LIST))+is_method

        self.writer.write_call(func_name,num_of_args)
       
        self.next()


    def compile_term(self,caller):
        type = self.tokenizer.token_type()
        if type is JTok.INT_CONST:
            self.writer.write_push(CONSTANT,self.tokenizer.intVal())
            self.next()

        elif type is JTok.STRING_CONST:

            string_val = self.tokenizer.string_val()
            self.writer.write_push(CONSTANT,len(string_val))
            self.writer.write_call("String.new", 1)
            for c in string_val:
                self.writer.write_push(CONSTANT,ord(c))
                self.writer.write_call("String.appendChar", 2)
            self.next()

        elif type is JTok.KEYWORD:
           if self.tokenizer.key_word() in {"null", "false"}:
                self.writer.write_push(CONSTANT, 0)
            elif self.tokenizer.key_word() == "true": 
                self.writer.write_push(CONSTANT, 1)
                self.writer.write_arithmetic("neg")
            elif self.tokenizer.key_word() == "this":
                self.writer.write_push(POINTER, 0)
            else:
                print("unexpected")

            self.next()

        elif type is JTok.IDENTIFIER:
            name = self.tokenizer.identifier()

            self.next()
            type = self.tokenizer.token_type()

            if type is JTok.SYMBOL and self.tokenizer.symbol() in {".", "("}:
                    self.compile_subroutineCall(caller,name)

            elif type is JTok.SYMBOL and self.tokenizer.symbol() == '[': 
                self.next()

                self.compile_expression(SubElement(caller, EXPRESSION))
                kind = self.symbols.kind_of(name)
                index = self.symbols.index_of(name)
                if kind is not None:
                    self.writer.write_push(kind.get_segment(),index)
                else:
                    print("unexpected")
                self.writer.write_arithmetic("add")
                self.writer.write_pop(POINTER,1)
                self.writer.write_push("that",0)
                self.next()

            else:
                kind = self.symbols.kind_of(name)
                index = self.symbols.index_of(name)
                if kind is not None:
                    self.writer.write_push(kind.get_segment(),index)
                else:
                    print("unexpected")

        elif type is JTok.SYMBOL:
            if self.tokenizer.symbol() == '(':
                self.next()

                self.compile_expression(SubElement(caller, EXPRESSION))
                self.next()

            elif self.tokenizer.symbol() in {'-','~'}:
                unary_op = self.tokenizer.symbol()
                self.next()
                self.compile_term(SubElement(caller,TERM))
                if unary_op == "-":
                    self.writer.write_arithmetic("neg")
                elif unary_op == "~":
                    self.writer.write_arithmetic("not")
                else:
                    "unexpected"



    def compile_do(self, caller):
        self.next()

        name = self.tokenizer.identifier()
        self.next()

        self.compile_subroutineCall(caller,name)
        self.writer.write_pop(TEMP,0)
        self.next()

    def compile_let(self, caller):
        self.next()

        varName = self.tokenizer.identifier()
        self.next()

        kind = self.symbols.kind_of(varName)
        kind = kind.get_segment()
        index = self.symbols.index_of(varName)

        if self.tokenizer.symbol() == '[': 
            self.next() 

            self.compile_expression(SubElement(caller, EXPRESSION))
            self.writer.write_push(kind,index)
            self.writer.write_arithmetic("add")
            self.next() 
            self.next() 
            self.compile_expression(SubElement(caller, EXPRESSION))
            self.writer.write_pop(TEMP,0)
            self.writer.write_pop(POINTER,1)
            self.writer.write_push(TEMP,0)
            self.writer.write_pop("that",0)

        else:
            self.next() 

            self.compile_expression(SubElement(caller, EXPRESSION))
            self.writer.write_pop(kind,index)

        self.next() 


    def compile_return(self, caller):
        self.next()

        if self.tokenizer.token_type() is JTok.SYMBOL and self.tokenizer.symbol() == ";":
            self.writer.write_push(CONSTANT, 0)
            self.writer.write_return()
            self.next()
            return

        self.compile_expression(SubElement(caller,EXPRESSION))
        self.writer.write_return()
        self.next()

    def compile_while(self, caller):
        while_index = self.while_counter
        self.while_counter += 1
        self.writer.write_label("WHILE_EXP"+str(while_index))
        self.next() 

        self.next() 

        self.compile_expression(SubElement(caller, EXPRESSION))
        self.writer.write_arithmetic("not")
        self.writer.write_if("WHILE_END"+str(while_index))

        self.next()

        self.next() 

        self.compile_statements(SubElement(caller, STATEMENTS))

        self.writer.write_goto("WHILE_EXP"+str(while_index))
        self.writer.write_label("WHILE_END"+str(while_index))
        self.next()


    def compile_statements(self, caller):
        STATEMENTS = {'do','while','let','return','if'}
        caller.text = " "
        while self.tokenizer.token_type() is JTok.KEYWORD and self.tokenizer.key_word() in STATEMENTS:
            if self.tokenizer.key_word() == 'do':
                self.compile_do(SubElement(caller, 'doStatement'))
            elif self.tokenizer.key_word() == 'while':
                self.compile_while(SubElement(caller, 'whileStatement'))
            elif self.tokenizer.key_word() == 'let':
                self.compile_let(SubElement(caller, 'letStatement'))
            elif self.tokenizer.key_word() == 'return':
                self.compile_return(SubElement(caller, 'returnStatement'))
            elif self.tokenizer.key_word() == 'if':
                self.compile_if(SubElement(caller, 'ifStatement'))

    def compile_if(self, caller):
       self.next()  # (
        self.compile_expression(caller)
        self.next()  # {

        if_index = self.if_counter
        self.if_counter += 1
        self.writer.write_if("IF_TRUE" + str(if_index))

        self.writer.write_goto("IF_FALSE" + str(if_index))
        self.writer.write_label("IF_TRUE" + str(if_index))

        self.compile_statements(caller)

        self.next()

        if self.tokenizer.key_word() == 'else':
            self.writer.write_goto("IF_END" + str(if_index))
            self.writer.write_label("IF_FALSE" + str(if_index))

            self.next()  
            self.next()  
            self.compile_statements(caller)
            self.next()  
            self.writer.write_label("IF_END" + str(if_index))
        else:
            self.writer.write_label("IF_FALSE" + str(if_index))

        return

    def compile_var_dec(self, caller):
        kind = self.tokenizer.key_word()
        self.next()

        return self.compile_list_of_vars(caller, "var", Kind[kind])

    def compile_class(self,caller):
        SubElement(caller,KEYWORD).text = self.tokenizer.key_word()
        self.next()

        SubElement(caller,IDENTIFIER).text = self.tokenizer.identifier()
        self.class_name = self.tokenizer.identifier()
        self.next()

        SubElement(caller,SYMBOL).text = self.tokenizer.symbol() #{
        self.next()

        while self.tokenizer.token_type() is JTok.KEYWORD and self.tokenizer.key_word() in {'static','field'}:
            self.compile_classVarDec(SubElement(caller,"classVarDec"))

        while not self.tokenizer.token_type() is JTok.SYMBOL:
            self.compile_subroutine(SubElement(caller,"subroutineDec"))

        SubElement(caller,SYMBOL).text = self.tokenizer.symbol() #}
        self.next()


    def compile_list_of_vars(self,caller,category, kind):
        num_of_vars = 0
        type = self.compile_type(caller)
        self.symbols.define(self.tokenizer.identifier(),type,kind)
        num_of_vars += 1
        self.next()

        while self.tokenizer.symbol() != ';':
            self.next()
            self.symbols.define(self.tokenizer.identifier(), type, kind)
            num_of_vars += 1
            self.next()

        self.next()
        return num_of_vars

    def compile_classVarDec(self,caller):
        kind = self.tokenizer.key_word()
        self.next()
        self.compile_list_of_vars(caller, kind, Kind[kind])



    def compile_type(self,caller):
        tag = KEYWORD if self.tokenizer.token_type() is JTok.KEYWORD else IDENTIFIER
        text = self.tokenizer.key_word() if tag is KEYWORD else self.tokenizer.identifier()
        SubElement(caller, tag).text = text
        self.next()
        return text

    def compile_subroutine(self,caller):
        subroutine_type = self.tokenizer.key_word()
        self.next()

        
        if self.tokenizer.token_type() is JTok.KEYWORD and self.tokenizer.key_word() == "void":
            SubElement(caller,KEYWORD).text = self.tokenizer.key_word()
            self.next()
        else:
            self.compile_type(caller)

        name = self.class_name+"."+self.tokenizer.identifier()
        self.symbols.start_subroutine()
        self.next()

        self.next()
        if subroutine_type == "method":
            self.symbols.define("this", "", Kind.arg)
        self.compile_parameterList(SubElement(caller,"parameterList"))

        self.next() 

        self.next() 

        num_of_locals = 0
        while self.tokenizer.token_type() is JTok.KEYWORD and self.tokenizer.key_word() == "var":
            num_of_locals += self.compile_var_dec(SubElement(caller,"varDec"))

        self.writer.write_function(name,num_of_locals)

        if subroutine_type == "constructor":
            self.writer.write_push(CONSTANT, self.symbols.var_count(Kind.field))
            self.writer.write_call("Memory.alloc", 1)
            self.writer.write_pop(POINTER,0)

        elif subroutine_type == "method":
            self.writer.write_push(ARGUMENT,0)
            self.writer.write_pop(POINTER,0)

        self.compile_statements(SubElement(caller,"statements"))

        self.next() # Skips }

    def compile_parameterList(self,caller):
        if self.tokenizer.token_type() is JTok.SYMBOL and self.tokenizer.symbol() == ")":
            caller.text = " "
            return

        type = self.compile_type(caller)
        name = self.tokenizer.identifier()
        self.symbols.define(name,type,Kind.arg)
        self.next()
        while self.tokenizer.token_type() is JTok.SYMBOL and self.tokenizer.symbol() == ",":
            self.next()
            type = self.compile_type(caller)
            name = self.tokenizer.identifier()
            self.symbols.define(name, type, Kind.arg)
            self.next()


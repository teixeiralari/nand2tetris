from splitEverthing import split
from LexicalElements import *

def prepare(file):
    newFile = open(file)
    mylist = list()
    for line in newFile:
        aux = ''
        #line = line.replace(" ", "")
        line = line.replace("\n", "")
        line = line.replace("\t", "")
        if((line != '') and (line[0:2] != '//')):
            if('//' in line):
                aux = line.split('//')
                aux = aux[0]
            elif ('/*' in line):
                pass
            else:
                aux=line
        if aux != '' and aux[0:2] != ' *':
            mylist.append(aux)
    final = split(mylist)
    return final

def token_(path_):
    prepare_ = prepare(path_)
    token = list()
    file = open('Main.xml','w')
    file.write('<tokens>\n')
    for word in prepare_:
        if word in keyword:
            file.write('<keyword> ' + word + ' </keyword>\n')
            token.append('<keyword> ' + word + ' </keyword>')
        elif word in symbol:
            if word in symbols_replace:
                file.write('<symbol> ' + symbols_replace[word] + ' </symbol>\n')
                token.append('<symbol> ' + symbols_replace[word] + ' </symbol>')
            else:
                file.write('<symbol> ' + word + ' </symbol>\n')
                token.append('<symbol> ' + word + ' </symbol>')
        elif word.isdigit():
            file.write('<integerConstant> ' + word + ' </integerConstant>\n')
            token.append('<integerConstant> ' + word + ' </integerConstant>')
        elif ('"' in word):
            file.write('<stringConstant> ' + word[1:-1] + ' </stringConstant>\n')
            token.append('<stringConstant> ' + word[1:-1] + ' </stringConstant>')
        else:
            file.write('<identifier> ' + word + ' </identifier>\n')
            token.append('<identifier> ' + word + ' </identifier>')
    
    file.write('</tokens>\n')
    return token



path_ = 'C:/Users/laris/Dropbox/nand2tetris/projects/10/ArrayTest/Main.jack'


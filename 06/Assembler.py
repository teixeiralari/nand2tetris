#C-instruction: 111 - comp(7) - dest(3) - jump(3)
#comp = o que é pra fazer (depois do igual)
#dest = para onde essa operacao vai
#jump = se tem algum jump

comp = {
    "0": "0101010",
    "1": "0111111",
    "-1": "0111010",
    "D": "0001100",
    "A": "0110000",
    "!D": "0001101",
    "!A": "0110001",
    "-D": "0001111",
    "-A": "0110011",
    "D+1": "0011111",
    "A+1": "0110111",
    "D-1": "0001110",
    "A-1": "0110010",
    "D+A": "0000010",
    "D-A": "0010011",
    "A-D": "0000111",
    "D&A": "0000000",
    "D|A": "0010101",
    "M": "1110000",
    "!M": "1110001",
    "-M": "1110011",
    "M+1": "1110111",
    "M-1": "1110010",
    "D+M": "1000010",
    "D-M": "1010011",
    "M-D": "1000111",
    "D&M": "1000000",
    "D|M": "1010101"
    }


dest = {
    "null": "000",
    "M": "001",
    "D": "010",
    "A": "100",
    "MD": "011",
    "AM": "101",
    "AD": "110",
    "AMD": "111"
    }


jump = {
    "null": "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111"
    }


# table of symbols used in assembly code, initialized to include
# standard ones
table = {
    "SP": 0,
    "LCL": 1,
    "ARG": 2,
    "THIS": 3,
    "THAT": 4,
    'R0': 0,
    'R1': 1,
    'R2': 2,
    'R3': 3,
    'R4': 4,
    'R5': 5,
    'R6': 6,
    'R7': 7,
    'R8': 8,
    'R9': 9,
    'R10': 10,
    'R11': 11,
    'R12': 12,
    'R13': 13,
    'R14': 14,
    'R15': 15,
    "SCREEN": 16384,
    "KBD": 24576,
    }


path_='/home/lariteixeira/nand2tetris/06/rect/RectL'
path_file = path_ + '.asm'
file_hack = path_ + '.hack'

def Parser(path_):
    mylist = list()
    
    file_ = open(path_)
    for line in file_:
        aux = ''
        line = line.replace(" ", "")
        line = line.replace("\n", "")
        if((line != '') and (line[0:2] != '//')):
            if('//' in line):
                aux = line.split('/')
                aux = aux[0]
            else:
                aux=line
        if aux != '':
            mylist.append(aux)
    return mylist


def getTypeCommand(_instruction):
    if(_instruction[0]=='@'):
        return 'A_COMMAND'
    elif((_instruction[0] == '(') and (_instruction[-1]==')')):
        return 'L_COMMAND'
    else:
        return 'C_COMMAND'

def firstPass():
    ROM = 0
    myfile = Parser(path_file)
    for i in myfile:
        command = getTypeCommand(i)
        if (command != 'L_COMMAND'):
            ROM += 1
        else:
            temp = i[1:-1]
            if temp not in table:
                table.update({temp:ROM})
    return myfile

def aInstruction(i,RAM):
    hack = '0'
    if i in table:
        temp = table[i]
        temp = str(bin(temp)[2::])
        hack += '0'*(15 - len(temp)) + temp
    elif (i.isdigit()==True):
        temp = str(bin(int(i))[2::])
        hack += '0'*(15 - len(temp)) + temp
    else:
        temp = i
        table.update({temp:RAM})
        binRAM = bin(RAM)[2::]
        hack += '0'*(15-len(binRAM)) + binRAM
        RAM +=1
    
    return hack, RAM

def cInstruction(i, RAM):
    hack = '111'
    if i.find('=') != -1: #encontrou =
        if i.find(';')==-1: #nao encontrou ;
            dest1 = i.split('=')[0]
            comp1 = i.split('=')[1]
            jump1 = 'null'
        else:
            aux = i.split('=')
            dest1 = aux[0]
            comp1 = aux[1].split(';')[0]
            jump1 = aux[1].split(';')[1]
    else:
        if (i.find(';') != -1):
            comp1 = i.split(';')[0]
            jump1 = i.split(';')[1]
            dest1 = 'null'
    hack += comp[comp1] + dest[dest1] + jump[jump1]
    return hack
    
        
    

def secondPass(newfile):
    with open(newfile, 'w') as outfile:
        RAM = 16
        myfile = firstPass()
        for i in myfile:
            command = getTypeCommand(i)
            if command == 'A_COMMAND':
                a,ram = aInstruction(i[1::],RAM)
                outfile.write(a + '\n')
                RAM = ram
            elif command == 'C_COMMAND':
                c = cInstruction(i,RAM)
                outfile.write(c + '\n')
            else:
                pass
        
secondPass(file_hack)

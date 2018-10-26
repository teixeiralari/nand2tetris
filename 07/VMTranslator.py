import os, sys


class Parser:
  def __init__(self, source):
    self.infile = open(source)
    self.command = None
    self.advanceReachedEOF = False

    self.cType = {
        "sub" : "math",
        "add" : "math",
        "neg" : "math",
        "eq"  : "math",
        "gt"  : "math",
        "lt"  : "math",
        "and" : "math",
        "or"  : "math",
        "not" : "math",
        "push" : "push",
        "pop"  : "pop",
        "EOF"  : "EOF",
        }

  def hasMoreCommands(self):
    position = self.infile.tell()
    self.advance()
    self.infile.seek(position)
    return not self.advanceReachedEOF

  def advance(self):
    thisLine = self.infile.readline()
    if thisLine == '':
      self.advanceReachedEOF = True
    else:
      splitLine = thisLine.split("/")[0].strip()
      if splitLine == '':
        self.advance()
      else:
        self.command = splitLine.split()

  def commandType(self):
    return self.cType.get(self.command[0], "invalid cType")

  def arg1(self):
    return self.command[1]

  def arg2(self):
    return self.command[2]


class CodeWriter:
  def __init__(self, dest):
    self.root = dest[:-4].split('/')[-1]
    self.outfile = open(dest, "w")
    self.nextLabel = 0

  def setFileName(self, source):
    self.fileName = source[:-3]

  def writeArithmetic(self, command):
    instruction = ""
    if command == "add":
      instruction += "@SP\n"
      instruction += "AM=M-1\n"
      instruction += "D=M\n" 
      instruction += "@SP\n" 
      instruction += "AM=M-1\n" 
      instruction += "M=D+M\n" 
      instruction += "@SP\n"
      instruction += "M=M+1\n" 
    elif command == "sub":
      instruction += "@SP\n" 
      instruction += "AM=M-1\n"
      instruction += "D=M\n" 
      instruction += "@SP\n" 
      instruction += "AM=M-1\n" 
      instruction += "M=M-D\n" 
      instruction += "@SP\n"
      instruction += "M=M+1\n" 
    elif command == "neg":
      instruction += "@SP\n"
      instruction += "A=M-1\n" 
      instruction += "M=-M\n" 
    elif command == "not":
      instruction += "@SP\n" 
      instruction += "A=M-1\n" 
      instruction += "M=!M\n" 
    elif command == "or":
      instruction += "@SP\n" 
      instruction += "AM=M-1\n"
      instruction += "D=M\n" 
      instruction += "@SP\n" 
      instruction += "A=M-1\n"
      instruction += "M=D|M\n" 
    elif command == "and":
      instruction += "@SP\n"
      instruction += "AM=M-1\n"
      instruction += "D=M\n" 
      instruction += "@SP\n" 
      instruction += "A=M-1\n"
      instruction += "M=D&M\n" 
    elif command == "eq":
      label = str(self.nextLabel)
      self.nextLabel += 1
      instruction += "@SP\n"
      instruction += "AM=M-1\n"
      instruction += "D=M\n" 
      instruction += "@SP\n"
      instruction += "A=M-1\n"
      instruction += "D=M-D\n" 
      instruction += "M=-1\n" 
      instruction += "@eq" + label + "\n" 
      instruction += "D;JEQ\n"
      instruction += "@SP\n"
      instruction += "A=M-1\n"
      instruction += "M=0\n" 
      instruction += "(eq" + label + ")\n"
    elif command == "gt":
      label = str(self.nextLabel)
      self.nextLabel += 1
      instruction += "@SP\n" 
      instruction += "AM=M-1\n"
      instruction += "D=M\n" 
      instruction += "@SP\n" 
      instruction += "A=M-1\n"
      instruction += "D=M-D\n" 
      instruction += "M=-1\n" 
      instruction += "@gt" + label + "\n"
      instruction += "D;JGT\n"
      instruction += "@SP\n" 
      instruction += "A=M-1\n"
      instruction += "M=0\n" 
      instruction += "(gt" + label + ")\n"
    elif command == "lt":
      label = str(self.nextLabel)
      self.nextLabel += 1
      instruction += "@SP\n" 
      instruction += "AM=M-1\n"
      instruction += "D=M\n" 
      instruction += "@SP\n"
      instruction += "A=M-1\n"
      instruction += "D=M-D\n" 
      instruction += "M=-1\n" 
      instruction += "@lt" + label + "\n"
      instruction += "D;JLT\n"
      instruction += "@SP\n" 
      instruction += "A=M-1\n"
      instruction += "M=0\n" 
      instruction += "(lt" + label + ")\n"
    else:
      pass
    self.outfile.write(instruction)

  def writePushPop(self, command, segment, index):
    instruction = ""
    if command == "push":
      if segment == "constant":
        instruction += "@" + index + "\n" 
        instruction += "D=A\n"
        instruction += "@SP\n" 
        instruction += "A=M\n" 
        instruction += "M=D\n"
        instruction += "@SP\n" 
        instruction += "M=M+1\n"
      elif segment == "static":
        instruction += "@" + self.root + "." + index + "\n"
        instruction += "D=M\n"
        instruction += "@SP\n" 
        instruction += "A=M\n" 
        instruction += "M=D\n"
        instruction += "@SP\n"
        instruction += "M=M+1\n"
      elif segment == "this":
        instruction += "@" + index + "\n" 
        instruction += "D=A\n"
        instruction += "@THIS\n"
        instruction += "A=M+D\n" 
        instruction += "D=M\n"
        instruction += "@SP\n"
        instruction += "A=M\n"
        instruction += "M=D\n"
        instruction += "@SP\n"
        instruction += "M=M+1\n"
      elif segment == "that":
        instruction += "@" + index + "\n"
        instruction += "D=A\n"
        instruction += "@THAT\n"
        instruction += "A=M+D\n" 
        instruction += "D=M\n"
        instruction += "@SP\n" 
        instruction += "A=M\n"
        instruction += "M=D\n"
        instruction += "@SP\n"
        instruction += "M=M+1\n"
      elif segment == "argument":
        instruction += "@" + index + "\n" 
        instruction += "D=A\n"
        instruction += "@ARG\n"
        instruction += "A=M+D\n" 
        instruction += "D=M\n"
        instruction += "@SP\n" 
        instruction += "A=M\n"
        instruction += "M=D\n"
        instruction += "@SP\n" 
        instruction += "M=M+1\n"
      elif segment == "local":
        instruction += "@" + index + "\n" 
        instruction += "D=A\n"
        instruction += "@LCL\n"
        instruction += "A=M+D\n" 
        instruction += "D=M\n"
        instruction += "@SP\n" 
        instruction += "A=M\n"
        instruction += "M=D\n"
        instruction += "@SP\n"
        instruction += "M=M+1\n"
      elif segment == "temp":
        instruction += "@" + index + "\n"
        instruction += "D=A\n"
        instruction += "@5\n"
        instruction += "A=A+D\n" 
        instruction += "D=M\n"
        instruction += "@SP\n" 
        instruction += "A=M\n"
        instruction += "M=D\n"
        instruction += "@SP\n"
        instruction += "M=M+1\n"
      elif segment == "pointer":
        instruction += "@" + index + "\n"
        instruction += "D=A\n"
        instruction += "@3\n"
        instruction += "A=A+D\n" 
        instruction += "D=M\n"
        instruction += "@SP\n"
        instruction += "A=M\n"
        instruction += "M=D\n"
        instruction += "@SP\n" 
        instruction += "M=M+1\n"
      else:
        pass
    elif command == "pop":
      if segment == "static":
        instruction += "@SP\n"
        instruction += "AM=M-1\n"
        instruction += "D=M\n"
        instruction += "@" + self.root + "." + index + "\n"
        instruction += "M=D\n"
      elif segment == "this":
        instruction += "@" + index + "\n"
        instruction += "D=A\n"
        instruction += "@THIS\n"
        instruction += "D=M+D\n" 
        instruction += "@R13\n"
        instruction += "M=D\n"
        instruction += "@SP\n" 
        instruction += "AM=M-1\n"
        instruction += "D=M\n"
        instruction += "@R13\n"
        instruction += "A=M\n"
        instruction += "M=D\n"
      elif segment == "that":
        instruction += "@" + index + "\n" 
        instruction += "D=A\n"
        instruction += "@THAT\n"
        instruction += "D=M+D\n" 
        instruction += "@R13\n"
        instruction += "M=D\n"
        instruction += "@SP\n"
        instruction += "AM=M-1\n"
        instruction += "D=M\n"
        instruction += "@R13\n"
        instruction += "A=M\n"
        instruction += "M=D\n"
      elif segment == "argument":
        instruction += "@" + index + "\n" 
        instruction += "D=A\n"
        instruction += "@ARG\n"
        instruction += "D=M+D\n" 
        instruction += "@R13\n"
        instruction += "M=D\n"
        instruction += "@SP\n"
        instruction += "AM=M-1\n"
        instruction += "D=M\n"
        instruction += "@R13\n" 
        instruction += "A=M\n"
        instruction += "M=D\n"
      elif segment == "local":
        instruction += "@" + index + "\n"
        instruction += "D=A\n"
        instruction += "@LCL\n"
        instruction += "D=M+D\n" 
        instruction += "@R13\n"
        instruction += "M=D\n"
        instruction += "@SP\n"
        instruction += "AM=M-1\n"
        instruction += "D=M\n"
        instruction += "@R13\n"
        instruction += "A=M\n"
        instruction += "M=D\n"
      elif segment == "pointer":
        instruction += "@" + index + "\n" 
        instruction += "D=A\n"
        instruction += "@3\n"
        instruction += "D=A+D\n" 
        instruction += "@R13\n"
        instruction += "M=D\n"
        instruction += "@SP\n" 
        instruction += "AM=M-1\n"
        instruction += "D=M\n"
        instruction += "@R13\n" 
        instruction += "A=M\n"
        instruction += "M=D\n"
      elif segment == "temp":
        instruction += "@" + index + "\n"
        instruction += "D=A\n"
        instruction += "@5\n"
        instruction += "D=A+D\n" 
        instruction += "@R13\n"
        instruction += "M=D\n"
        instruction += "@SP\n"
        instruction += "AM=M-1\n"
        instruction += "D=M\n"
        instruction += "@R13\n" 
        instruction += "A=M\n"
        instruction += "M=D\n"
      else:
        pass
    self.outfile.write(instruction)

    
def main():
  path_ = 'xxx'
  parser = Parser(path_ + ".vm")
  writer = CodeWriter(path_ + ".asm")
  
  while parser.hasMoreCommands():
    parser.advance()
    cType = parser.commandType()
    if cType == "push" or cType == "pop":
      writer.writePushPop(cType, parser.arg1(), parser.arg2())
    elif cType == "math":
      writer.writeArithmetic(parser.command[0])
    else:
      pass


main()

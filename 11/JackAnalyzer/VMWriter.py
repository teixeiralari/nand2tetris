from SymbolTable import Kind
class VMWriter:
    def __init__(self, file):
        self.file = open(file[:-5] + ".vm", 'w')

    def write_goto(self, label):
        self.file.write("goto " + label + "\n")

    def write_if(self, label):
        self.file.write("if-goto " + label + "\n")

    def write_call(self, name, n_args):
        self.file.write("call " + name + " " + str(n_args) + "\n")

    def write_function(self, name, n_locals):
        self.file.write("function " + name + " " + str(n_locals) + "\n")

    def write_return(self):
        self.file.write("return" + "\n")

    def write_push(self, segment, index):
        self.file.write("push " + segment + " " + str(index) + "\n")

    def write_pop(self, segment, index):
        self.file.write("pop " + segment + " " + str(index) + "\n")

    def write_arithmetic(self, command):
        self.file.write(command + "\n")

    def write_label(self, label):
       self.file.write("label " + label + "\n")

    def close(self):
        self.file.close()


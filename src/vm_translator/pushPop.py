class PushPop:
    def __init__(self, nomclass=None):
        """ initialise la classe Parser """
        self.nomclass = nomclass

    def asm(self, command):
        type = command['type']
        match type:
            case 'push':
                return self._commandpush(command)
            case 'pop':
                return self._commandpop(command)

    def _commandpush(self, command):
        """Renvoi le code de la fonction push du segment lu ou erreur"""
        segment = command['segment']
        # segment=local|argument|static|constant|this|that|pointer
        match segment:
            # Faire une fonction par type de segment
            case 'local' | 'argument' | 'this' | 'that':  #
                return self._commandpushlocal(command)
            case 'static':  #
                return self._commandpushstatic(command)
            case 'constant':  # static foo.i
                return self._commandpushconstant(command)
            case 'pointer':  #
                return self._commandpushpointer(command)
            case 'temp':  #
                return self._commandpushtemp(command)
            case _:
                print(f'SyntaxError : {command}')
                exit()

    def _commandpop(self, command):
        """Renvoi le code de la fonction push du segment lu ou erreur"""
        segment = command['segment']
        # segment=local|argument|static|constant|this|that|pointer
        match segment:
            # Faire une fonction par type de segment
            case 'local' | 'argument' | 'this' | 'that':  #
                return self._commandpoplocal(command)
            case 'static':  #
                return self._commandpopstatic(command)
            case 'constant':  # static foo.i
                return self._commandpopconstant(command)
            case 'pointer':  #
                return self._commandpoppointer(command)
            case 'temp':  #
                return self._commandpoptemp(command)
            case _:
                print(f'SyntaxError : {command}')
                exit()

    def _commandpushlocal(self, command):
        """Renvoi le code de la fonction push local/argument/this/that i lu"""
        segment = command['segment']
        match segment:
            case 'local':
                bob = 'LCL'
            case 'argument':
                bob = 'ARG'
            case 'this':
                bob = 'THIS'
            case 'that':
                bob = 'THAT'
        parameter = command['parameter']

        return f"""\t//{command['type']} {command['segment']} {parameter}
        @{parameter}
        D=A
        @{bob}
        A=D+M
        D=M
        @SP
        A=M
        M=D
        @SP
        M=M+1
        """

    def _commandpoplocal(self, command):
        """Renvoi le code de la fonction pop local/argument/this/that i"""
        segment = command['segment']
        match segment:
            case 'local':
                bob = 'LCL'
            case 'argument':
                bob = 'ARG'
            case 'this':
                bob = 'THIS'
            case 'that':
                bob = 'THAT'
        parameter = command['parameter']

        return f"""\t//{command['type']} {command['segment']} {parameter}
        @{parameter}
        D=A
        @{bob}
        D=D+M
        @R13
        M=D
        @SP
        AM=M-1
        D=M
        @R13
        A=M
        M=D
        """

    def _commandpushstatic(self, command):
        """Renvoi le code de la fonction push static i lu"""
        parameter = command['parameter']
        return f"""\t//{command['type']} {command['segment']} {parameter}
        @{self.nomclass}.{parameter}
        D=M
        @SP
        A=M
        M=D
        @SP
        M=M+1        
        """

    def _commandpopstatic(self, command):
        """Renvoi le code de la fonction push static i lu"""
        parameter = command['parameter']
        return f"""\t//{command['type']} {command['segment']} {parameter}
        @SP
        AM=M-1
        D=M
        @{self.nomclass}.{parameter}
        M=D        
        """

    def _commandpushconstant(self, command):
        """Renvoi le code de la fonction push constant i lu"""
        parameter = command['parameter']
        return f"""\t//{command['type']} {command['segment']} {parameter}
        @{parameter}
        D=A
        @SP
        A=M
        M=D
        @SP
        M=M+1
        """

    def _commandpopconstant(self, command):
        """Renvoi le code de la fonction push constant i lu"""
        parameter = command['parameter']
        return f"""\t//{command['type']} {command['segment']} {parameter}
        @SP
        M=M-1
        """

    def _commandpushpointer(self, command):
        """Renvoi le code de la fonction push pointer i"""
        parameter = command['parameter']
        # pointer 0 -> THIS, pointer 1 -> THAT
        base = 'THIS' if str(parameter) == '0' else 'THAT'
        return f"""\t//{command['type']} {command['segment']} {parameter}
        @{base}
        D=M
        @SP
        A=M
        M=D
        @SP
        M=M+1
        """

    def _commandpoppointer(self, command):
        """Renvoi le code de la fonction pop pointer i"""
        parameter = command['parameter']
        base = 'THIS' if str(parameter) == '0' else 'THAT'
        return f"""\t//{command['type']} {command['segment']} {parameter}
        @SP
        AM=M-1
        D=M
        @{base}
        M=D
        """

    def _commandpushtemp(self, command):
        """Renvoi le code de la fonction push temp i lu"""
        parameter = int(command['parameter']) + 5  # temp i est en RAM[5+i]
        return f"""\t//{command['type']} {command['segment']} {command['parameter']}
        @{parameter}
        D=M
        @SP
        A=M
        M=D
        @SP
        M=M+1
        """

    def _commandpoptemp(self, command):
        """Renvoi le code de la fonction pop temp i lu"""
        parameter = int(command['parameter']) + 5  # temp i est en RAM[5+i]
        return f"""\t//{command['type']} {command['segment']} {command['parameter']}
        @SP
        AM=M-1
        D=M
        @{parameter}
        M=D
        """
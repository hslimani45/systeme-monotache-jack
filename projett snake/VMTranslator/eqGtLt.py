class eqGtLt:
    """Génère le code ASM pour les comparaisons eq, gt, lt.

    Utilise un compteur pour générer des labels uniques EQ_TRUE$n, GT_TRUE$n, LT_TRUE$n.
    """

    def __init__(self):
        self.counter = 0

    def _commandArith(self, command):
        """Dispatch pour les commandes eq, gt, lt."""
        op = command['type']
        match op:
            case 'eq':
                return self._commandEq(command)
            case 'gt':
                return self._commandGt(command)
            case 'lt':
                return self._commandLt(command)
            case _:
                print(f'SyntaxError : {command}')
                exit()

    def _commandEq(self, command):
        self.counter += 1
        n = self.counter
        return f"""\t// {command['type']}
@SP
AM=M-1       
D=M          
A=A-1        
D=M-D       
@EQ_TRUE${n}
D;JEQ
@SP
A=M-1
M=0
@EQ_END${n}
0;JMP
(EQ_TRUE${n})
@SP
A=M-1
M=-1
(EQ_END${n})
"""

    def _commandGt(self, command):
        self.counter += 1
        n = self.counter
        return f"""\t// {command['type']}
@SP
AM=M-1
D=M
A=A-1
D=M-D 
@GT_TRUE${n}
D;JGT
@SP
A=M-1
M=0
@GT_END${n}
0;JMP
(GT_TRUE${n})
@SP
A=M-1
M=-1
(GT_END${n})
"""

    def _commandLt(self, command):
        self.counter += 1
        n = self.counter
        return f"""\t// {command['type']}
@SP
AM=M-1
D=M
A=A-1
D=M-D 
@LT_TRUE${n}
D;JLT
@SP
A=M-1
M=0
@LT_END${n}
0;JMP
(LT_TRUE${n})
@SP
A=M-1
M=-1
(LT_END${n})
"""
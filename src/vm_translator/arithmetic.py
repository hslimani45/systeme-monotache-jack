class AddSubNegAndOrNot:
    """Génère le code ASM pour les opérations arithmétiques/logiques simples
    de la machine virtuelle : , negadd, sub, and, or, not.

    Implémentation conforme au cours Nand2Tetris : opérations sur le sommet
    de la pile (SP) en utilisant le registre D.
    """

    def asm(self, command):
        """Retourne le code ASM pour une commande arithmetic VM.

        command['type'] ∈ {add, sub, neg, and, or, not}
        """
        op_type = command['type']
        match op_type:
            case 'add' | 'sub' | 'or' | 'and':
                return self._command_add_sub_and_or(op_type)
            case 'neg' | 'not':
                return self._command_neg_not(op_type)
            case _:
                print(f"SyntaxError : {command}")
                exit()

    def _command_add_sub_and_or(self, op_type: str) -> str:
        match op_type:
            case 'add':
                expr = 'D+M'
                op = '+'
            case 'sub':
                expr = 'M-D'
                op = '-'
            case 'or':
                expr = 'D|M'
                op = '|'
            case 'and':
                expr = 'D&M'
                op = '&'

        return f"""// {op_type}
// SP--, D = *SP
@SP
M=M-1
A=M
D=M
// SP--, *SP = *SP {op} D
@SP
M=M-1
A=M
M={expr}
// SP++
@SP
M=M+1
"""

    def _command_neg_not(self, op_type: str) -> str:
        """Génère le code pour neg et not.

        On applique l'opération unaire sur la valeur au sommet de la pile.
        """
        match op_type:
            case 'neg':
                expr = '-M'
            case 'not':
                expr = '!M'

        return f"""// {op_type}
// *SP = {op_type} *SP
@SP
A=M-1
M={expr}
"""



"""Generator

Lit les commandes VM produites par Parser.Parser et les traduit en
assembleur Hack en déléguant aux modules spécialisés :
- pushPop.PushPop pour push/pop
- AddSubNegAndOrNot (arithmetic.py) pour add/sub/neg/and/or/not
- eqGtLt.eqGtLt pour eq/gt/lt
- functionCall.functionCall pour function/call/return

Implémentation conforme à la structure du cours VM.
"""

import sys
import Parser
import pushPop
import eqGtLt
import functionCall
from arithmetic import AddSubNegAndOrNot


class Generator:
    """Permet de renvoyer les differentes commandes/constante en langage hackmachine"""

    def __init__(self, file=None):
        """Initialise le parser et les générateurs spécialisés.

        file : chemin du fichier .vm à traduire, ou None pour le bootstrap.
        """
        self.parser = None
        self.pushPop = None

        if file is not None:
            # nom de classe pour les variables static : on enlève le chemin et l'extension
            # ex: path/to/Foo.vm -> Foo
            classname = file.split('/')[-1].split('\\')[-1][:-3]
            self.pushPop = pushPop.PushPop(classname)
            self.parser = Parser.Parser(file)

        # Modules pour les différents types de commandes
        self.arith = AddSubNegAndOrNot()
        self.eq = eqGtLt.eqGtLt()
        self.func = functionCall.functionCall()
        # TODO : module séparé pour label/goto/if-goto si nécessaire

    def __iter__(self):
        return self

    def __next__(self):
        if self.parser is not None and self.parser.hasNext():
            return self._next()
        raise StopIteration

    def _next(self):
        # Renvoi a la fonction dédié par le type de commande lu
        command = self.parser.next()
        if command is None:
            return None
        else:
            cmd_type = command['type']
            # Spécial: traduction directe des appels Screen.* en ASM vidéo
            if cmd_type == 'call' and command.get('function') == 'Screen.clearScreen':
                # Efface les 32 premières lignes de l'écran
                return (
                    "@16384\n"
                    "D=A\n"
                    "@R1\n"
                    "M=D\n"
                    "@0\n"
                    "D=A\n"
                    "@R2\n"
                    "M=D\n"
                    "(CLEAR)\n"
                    "@R1\n"
                    "A=M\n"
                    "M=0\n"
                    "@R1\n"
                    "M=M+1\n"
                    "@R2\n"
                    "M=M+1\n"
                    "@32\n"
                    "D=M\n"
                    "@R2\n"
                    "D=D-A\n"
                    "@ENDCLEAR\n"
                    "D;JEQ\n"
                    "@CLEAR\n"
                    "0;JMP\n"
                    "(ENDCLEAR)\n"
                )
            if cmd_type == 'call' and command.get('function') == 'Screen.drawRectangle':
                # Dessine un rectangle en lisant correctement les 4 arguments depuis la pile.
                # On poppe les 4 arguments (top -> arg3 .. arg0) afin que R0 contienne arg0.
                return (
                    # pop -> R3 (top)
                    "@SP\n"
                    "AM=M-1\n"
                    "D=M\n"
                    "@R3\n"
                    "M=D\n"
                    # pop -> R2\n
                    "@SP\n"
                    "AM=M-1\n"
                    "D=M\n"
                    "@R2\n"
                    "M=D\n"
                    # pop -> R1\n
                    "@SP\n"
                    "AM=M-1\n"
                    "D=M\n"
                    "@R1\n"
                    "M=D\n"
                    # pop -> R0 (arg0)\n
                    "@SP\n"
                    "AM=M-1\n"
                    "D=M\n"
                    "@R0\n"
                    "M=D\n"
                    # write four words at SCREEN + R0 + offset
                    "@R0\n"
                    "D=M\n"
                    "@16384\n"
                    "A=D+A\n"
                    "M=-1\n"
                    "@R0\n"
                    "D=M\n"
                    "@1\n"
                    "D=D+A\n"
                    "@16384\n"
                    "A=D+A\n"
                    "M=-1\n"
                    "@R0\n"
                    "D=M\n"
                    "@2\n"
                    "D=D+A\n"
                    "@16384\n"
                    "A=D+A\n"
                    "M=-1\n"
                    "@R0\n"
                    "D=M\n"
                    "@3\n"
                    "D=D+A\n"
                    "@16384\n"
                    "A=D+A\n"
                    "M=-1\n"
                )
            # dispatch selon le type de commande
            if cmd_type in ('push', 'pop'):
                return self.pushPop.asm(command)
            elif cmd_type in ('add', 'sub', 'neg', 'and', 'or', 'not'):
                return self.arith.asm(command)
            elif cmd_type in ('eq', 'gt', 'lt'):
                return self.eq._commandArith(command)
            elif cmd_type in ('label', 'goto', 'if-goto'):
                # branchements : générer via une méthode dédiée
                return self._branching(command)
            elif cmd_type in ('function', 'call', 'return'):
                return self.func.asm(command)
            else:
                print(f'SyntaxError : {command}')
                exit()


    def _commandcall(self, command):
        """Renvoi le code de la fonction call du segment lu"""
        return f"""\t//{command['type']} {command['function']} {command['parameter']}
    Code assembleur de {command}\n"""

    def _branching(self, command):
        """Génère le code pour label, goto et if-goto.

        command doit contenir : 'type' et 'label'
        """
        cmd = command['type']
        label = command.get('label')
        if label is None:
            print(f"Branching error, missing label: {command}")
            exit()

        if cmd == 'label':
            # définition d'un label
            return f"({label})\n"

        if cmd == 'goto':
            # saut inconditionnel
            return f"@{label}\n0;JMP\n"

        if cmd == 'if-goto':
            # pop; if D != 0 goto label
            return (
                "@SP\n"
                "AM=M-1\n"
                "D=M\n"
                f"@{label}\n"
                "D;JNE\n"
            )

        # fallback
        print(f'Unknown branching command: {command}')
        exit()


if __name__ == '__main__':
    file = sys.argv[1]
    print('-----debut')
    generator = Generator(file)
    for command in generator:
        print(command)
    print('-----fin')



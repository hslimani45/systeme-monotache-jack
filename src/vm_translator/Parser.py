"""On importe sys qui permet d'avoir accès à certaines fonctions et interagir avec l'interpréteur Python, on importe aussi Lexer pour pouvoir s'en servir dans le fichier"""

import sys
import Lexer


class Parser:
    """On crée une classe Parser dans laquelle on initialise deux attributs lexer et command, on importe le module Lexer
    depuis le fichier Lexer qu'on affecte à self.lexer et on affecte la lecture du fichier (qui n'est utilisable que dans la classe) à self.command"""

    def __init__(self, file):
        self.lexer = Lexer.Lexer(file)
        self.command = self._read()

    def next(self):
        """On stocke la lecture du fichier dans res, on continue de lire le fichier puis on renvoie la valeur précédente"""
        res = self.command
        self.command = self._read()
        return res

    def look(self):
        """Fonction qui retourne la lecture de tout le fichier"""
        return self.command

    def hasNext(self):
        """Fonction qui permet de dire si self.command est non vide ou si au contraire elle l'est"""
        return self.command is not None

    def __iter__(self):
        return self

    def __next__(self):
        if self.hasNext():
            return self.next()
        else:
            raise StopIteration

    def _read(self):
        """La commande command lit l'entièreté du fichier lexer et retourne None si son contenu est vide. Sinon, """
        command = self.lexer.look()
        if command is None:
            return None
        else:
            type = command['type']
            # Remplacement du match/case (Python 3.10) par if/elif
            if type == 'pushpop':
                return self._commandpushpop()
            elif type == 'branching':
                return self._commandbranching()
            elif type == 'arithmetic':
                return self._commandarithmetic()
            elif type == 'function':
                return self._commandfunction()
            elif type == 'return':
                return self._commandreturn()
            else:
                print(f'SyntaxError : {command}')
                exit()

    def _commandarithmetic(self):
        # No comment
        command = self.lexer.next()
        return {'line': command['line'], 'col': command['col'], 'type': command['token']}

    def _commandpushpop(self):
        # No comment
        command = self.lexer.next()
        segment = self.lexer.next()
        parameter = self.lexer.next()
        if segment is None or parameter is None or segment['type'] != 'segment' or parameter['type'] != 'int':
            print(f"SyntaxError (line={command['line']}, col={command['col']}): {command['token']}")
            exit()

        return {'line': command['line'], 'col': command['col'], 'type': command['token']
            , 'segment': segment['token'], 'parameter': parameter['token']}

    def _commandbranching(self):
        # No comment
        command = self.lexer.next()
        label = self.lexer.next()
        if label is None or label['type'] != 'string':
            print(f"SyntaxError (line={command['line']}, col={command['col']}): {command['token']}")
            exit()

        return {'line': command['line'], 'col': command['col'], 'type': command['token']
            , 'label': label['token']}

    def _commandfunction(self):
        # No comment
        command = self.lexer.next()
        name = self.lexer.next()
        parameter = self.lexer.next()
        if name is None or parameter is None or name['type'] != 'string' or parameter['type'] != 'int':
            print(f"SyntaxError (line={command['line']}, col={command['col']}): {command['token']}")
            exit()

        return {'line': command['line'], 'col': command['col'], 'type': command['token']
            , 'function': name['token'], 'parameter': parameter['token']}

    def _commandreturn(self):
        # No comment
        command = self.lexer.next()
        return {'line': command['line'], 'col': command['col'], 'type': command['token']}


if __name__ == "__main__":
    file = sys.argv[1]
    print('-----debut')
    parser = Parser(file)
    for command in parser:
        print(command)
    print('-----fin')

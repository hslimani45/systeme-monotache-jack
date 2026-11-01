import re
import sys

import Reader

''' Analyseur lexical '''


class Lexer:
    """Il lit un fichier caractere par caractere et produit une suite de tokens"""

    def __init__(self, file):
        self.reader = Reader.Reader(file)
        self.token = self._read()

    def _comment(self):
        # IL permet de commenter
        t = self.reader.next()
        if self.reader.hasNext():
            t = self.reader.next()
        else:
            return
        if t['char'] == '/':
            while t is not None and t['char'] != '\n':
                t = self.reader.next()
            return
        else:
            while True:
                while t is not None and t['char'] != '*':
                    t = self.reader.next()
                t = self.reader.next()
                if t is None or t['char'] == '/':
                    return

    def _skip(self):
        # Ignore un caractere non significatif comme espace,saute ligne.
        self.reader.next()
        return

    def _toke(self):
        # Construit un token avec les lettres,chiffres et tirets.
        res = ''
        t = self.reader.next()
        while t is not None and re.fullmatch(r'[a-zA-Z0-9_\.\-]', t['char']):
            res += t['char']
            t = self.reader.next()
        return res

    def next(self):
        """Renvoie le token courat et lire la souvente """
        res = self.token
        self.token = self._read()
        return res

    def _read(self):
        """Lit les prochains tokens en sautant espaces et commentaires.
        Retourne un dict {line, col, type, token} ou None à la fin.
        Suivi fidèlement de la spécification de tokens VM du cours.
        """
        token = None
        while self.reader.hasNext() and token is None:
            self.line = self.reader._line
            self.col = self.reader._col
            t = self.reader.look()
            char = t['char']

            # Remplacement de match/case par if/elif pour rester compatible
            # avec la version de Python utilisée en TP.
            if char == '/':
                self._comment()
            elif char in (' ', '\t', '\n'):
                self._skip()
            elif re.fullmatch(r'[a-zA-Z0-9]', char):
                token = self._toke()
            else:
                print(f'SyntaxError : line={self.line}, col={self.col}')
                exit()

        if token is None:
            return None
        else:
            pattern = self._pattern()
            group = pattern.fullmatch(token)
            if group is None:
                print(f'SyntaxError (line={self.line}, col={self.col}): {token}')
                exit()
            else:
                return {'line': self.line, 'col': self.col, 'type': group.lastgroup, 'token': token}

    def hasNext(self):
        """ Indique s'il reste des tokens a lire """
        return self.token is not None

    def look(self):
        """ Donne un apperçu de prochain token sans l'avancer """
        return self.token

    def _pattern(self):
        # Expresssion qui definit les types de tokens du langage.Chaque nom de groupe correspond a un type de token.
        return re.compile(r"""
            (?P<pushpop>push|pop) |
            (?P<segment>local|argument|static|constant|this|that|pointer|temp) |
            (?P<branching>label|goto|if-goto) |
            (?P<arithmetic>add|sub|neg|eq|gt|lt|and|or|not) |
            (?P<function>function|call) |
            (?P<return>return) |
            (?P<string>[a-zA-Z][a-zA-Z0-9_\.]*) | # label et nom de fonction
            (?P<int>[0-9]+) # des entiers 
        """, re.X)

    def __iter__(self):
        return self

    def __next__(self):
        if self.hasNext():
            return self.next()
        else:
            raise StopIteration


if __name__ == "__main__":
    file = sys.argv[1]
    print('-----debut')
    lexer = Lexer(file)
    for token in lexer:
        print(token)
    print('-----fin')

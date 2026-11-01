import os
import sys


class Reader:
    """Classe qui lit un fichier caractère par caractère
    et garde la position (ligne, colonne, caractère courant)"""

    def __init__(self, file):
        self.char = None    #Charactère courant
        self._line = 1      #ligne du charactère
        self._col = 1       #cologne du charactère

        #Si le fichier exist -> on l'ouvre
        if os.path.exists(file):
            self.file = open(file, "r")
            self.char = self.file.read(1) #self.char = premier charactère du fichier

    def look(self):
        """Renvoie la position du charactère courrant"""
        return {'line': self._line, 'col': self._col, 'char': self.char}

    def next(self):
        """Renvoie un dict contenant la ligne et la cologne du charactère courrant, 
        Puis ligne et cologne divient ligne et cologne du charactère suivant"""
        res = {'line': self._line, 'col': self._col, 'char': self.char}
        if self.hasNext():
            if self.char == '\n':
                self._line += 1
                self._col = 1
            else:
                self._col += 1
            self.char = self.file.read(1)
            if not self.hasNext():
                self.file.close()
        return res

    def hasNext(self):
        """Renvoie True si self.char exist,
        sinon renvoie False"""
        if self.char:
            return True
        else:
            return False

    def __iter__(self):
        """Permet d’utiliser Reader dans une boucle for."""
        return self

    def __next__(self):
        """Définit le comportement de next(lecteur)."""
        if self.hasNext():
            return self.next()
        else:
            raise StopIteration


if __name__ == "__main__":
    file = sys.argv[1] #recupère le fichier passé en argumetn
    print('-----debut')
    lecteur = Reader(file)
    for c in lecteur: #parcour "lecteur" qui est un objet "Reader"
        print(c)
    print('-----fin')

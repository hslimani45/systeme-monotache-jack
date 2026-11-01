import os
import glob
import sys

import Generator
import functionCall


class Translator:
    """Traduit un ou plusieurs fichiers .vm (virtual machine) en un fichier assembleur .asm"""

    def __init__(self, files, asm):
        #Fichier de sortie en assembleur .asm
        self.asm = open(asm, "w")
        #Fichier ou dossier vm en entré
        self.files = files
 
    def translate(self):
        """Lance la traduction VM -> ASM"""
        #Écrit le bootstrap (initialisation de la pile + appel à Sys.init)
        self.asm.write(self._bootstrap())
        # os.listdir("/home/user")
        #Si self.files est un seul fichier .vm
        if os.path.isfile(self.files):
            self._translateonefile(self.files)
        #Si self.files est un répertoire, on parcourt tous les fichier .vm dedans
        else:
            if os.path.isdir(self.files):
                for file in glob.glob(f'{self.files}/*.vm'):
                    self._translateonefile(file)

    def _translateonefile(self, file):
        """Traduit un seul fichier .vm en code assembleur .asm"""
        #Écrit un commentaire pour indiquer le début du fichier
        self.asm.write(f"""\n//code de {file}\n""")

        #Créer un générateur qui lit les commandes VM et les traduits en ASM
        generator = Generator.Generator(file)

        #Pour chaque commande ASM produite par le générateur, on l'écrit dans le fichier de sortie
        for command in generator:
            self.asm.write(command)

    def _bootstrap(self):
        """Retourne le code assembleur de bootstrap(initialisation)"""
        #Génère le code ASM qui appelle la fonction Sys.init
        # Use the functionCall module to generate the Sys.init call bootstrap
        init = functionCall.functionCall().asm({'type': 'call', 'function': 'Sys.init', 'parameter': '0'})

        # Initialise le pointeur de la pile (SP) à l'adresse 256 
        return f"""// Bootstrap
    @256
    D=A
    @SP
    M=D
{init}
"""


if __name__ == "__main__":
    #Vérifie qu'on a bien passé les arguments en ligne de commande 
    if len(sys.argv) < 2:
        print("Usage: Translator.py <vm file| dir> <asm file>")
    else:
        #1er argument = fichier ou dossier .vm 
        vmfiles=sys.argv[1]
        #2ième argument = fichier .asm de sortie 
        asmfile=sys.argv[2]
        
        #Créer un traducteur et lance la traduction 
        translator = Translator(vmfiles,asmfile)
        translator.translate()

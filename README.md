# Monotâche — Snake, Jack et machine virtuelle

Projet autour de la chaîne de traduction Jack → VM → assembleur Hack, avec un jeu Snake comme exemple. Les traducteurs sont écrits en Python ; le jeu est écrit en Jack.

## Contenu

- `SnakeVM/` : sources Jack et fichiers VM du Snake.
- `projett snake/Jack/` : analyse lexicale, analyse syntaxique et génération de code VM.
- `projett snake/VMTranslator/` : traduction des instructions VM en assembleur Hack, avec initialisation de la pile et appel à `Sys.init`.
- Les dossiers `test/`, `asm/` et la seconde copie de `SnakeVM/` conservent les sorties et variantes du travail initial. Les fichiers de `test/` sont des exemples assembleur, pas une suite de tests automatisés.

## Compiler le Snake

Python 3.10 ou plus récent suffit pour lancer les traducteurs. Depuis la racine du dépôt :

```sh
mkdir -p build
cd build
python3 "../projett snake/Jack/Translator.py" ../SnakeVM
cp ../SnakeVM/Sys.vm .
python3 "../projett snake/VMTranslator/Translator.py" . Snake.asm
```

Le compilateur écrit les fichiers `.vm` dans le dossier courant, d’où l’utilisation de `build/`.

## Jouer

Le jeu utilise l’environnement Jack/Hack de nand2tetris et ses services système : écran, clavier, mémoire et temporisation. Il ne se lance pas directement avec Python.

Charger les fichiers VM dans le VM Emulator de nand2tetris, avec les services de son OS disponibles. Les flèches dirigent le serpent, Espace passe au niveau suivant lorsqu’il est terminé et Échap quitte la partie. Le code prévoit dix niveaux de difficulté.

La sortie assembleur ne contient pas à elle seule l’OS Jack : sa génération ne suffit donc pas à obtenir un jeu autonome dans le CPU Emulator. Les fichiers VM fournis et ceux produits par le compilateur sont conservés séparément pour permettre leur comparaison.

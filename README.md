# AVANT DE JOUER : 
Le programme ne marche pas sur pyzo à cause de l’utilisation de fonctions python appartenant à curses. 
Il est recommandé d’utiliser Visual Studio Code à la place.
Les inputs sur un système avec MacOS ou Linux ne marcheront pas car les nombres qu'utilise le système pour identifier 
quelle touche a été appuyée sont différents, il faut donc changer les valeurs suivantes dans la fonction detect_keys si le programme ne marche pas:
    450 par 259;
    456 par 258;
    452 par 261;
    454 par 260.

# FICHIERS DU PROJET
- main.py : programme Python.
- titles.json : Contient les titres en format 2D et 3D.
- README.md : Explications du jeu et comment jouer

# COMMENT LANCER LE PROGRAMME ?
Placer les trois fichiers dans le même dossier. 
Ouvrir un terminale sur Visual Studio Code.
Saisir dans le terminale : pip install windows-curses
Appuyer sur la bouton Run au dessus de la barre à outils.

# COMMENT L'UTILISER ?
Appuyer sur les touches flèche pour se déplacer.
Le serpent grandit quand il mange une pomme.
La partie est perdue si le serpent sort de la zone ou s'il rentre dans sa queue.
Le score est affiché pendant la partie.

# ORGANISATION DU CODE
main() exécuté toutes les autres fonctions et finit avec detect_keys
Cette fonction detect_keys lis les inputs effectués par le joueur et déplace le serpent en appelant les autres fonctions.
Si le joueur ne fait rien pendant 300 millisecondes (avec stdscr.timeout(300)), le serpent se déplace automatiquement vers la case suivante.

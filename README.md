# CurvedSnake

CurvedSnake est une adaptation de CurveFever codée en Python 3.

#Dépendances

CurvedSnake requiert les modules (packages) suiavnts :

- tkinter pour l'interface graphique (package fourni avec Python 3) ;

- pyglet pour jouer de la musique en fond (package imposant et très peu utilisé dans ce contexte) ;
    * le package est à installer avec `pip install pyglet` (attention aux droits d'administrateurs qui peuvent être nécessaires)
    * ATTENTION : par défaut, ce package ne supporte que le format `wav`. Pour pouvoir lire des `mp3`, il est nécessaire d'installer AVbin (voir plus bas).

- shelve pour les sauvegardes (fourni avec Python 3).

# TO DO:

- Améliorer arc de cercle ;

- Tout faire pour éviter les lags ;

- Points de classement ;

- Éventuels exploits lorsque l'on prend plusieurs bonus à la suite (par exemple).

# Idées de bonus:

- Lors du bonus invert_color (négatif), mettre la musique de nyan-cat ;

- Faire en sortes que les autres ne puissent tourner que d'un seul côté
(ATTENTION: mettre un signe sur la tête des autres joueurs pour qu'ils soient prévenu) ;

- Faire apparaître des obstacles (des bébés chats par exemple) ;

- Bonus qui fait acquérir des points de classement supplémentaire (points de classement à faire) ;

#Pour utiliser des mp3:

- Pour Windows : copier le fichier avbin.dll dans C:/Windows/System32

- Pour mac : installer la version AVbin 10 (les autres ne fonctionnent pas)

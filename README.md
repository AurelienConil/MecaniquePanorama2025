# Mecanique Panorama

# Installation depuis le dernier release.


Extraire le zip, et le placer n'importe où . Le dossier Documents est bien.

Dans le dossier data, créer un dossier "photos" ( il est absent car vide dans le git)

Dans le dossier utils, installer tous les utilitaires

## Installation des dependances de git

pip install pyserial
pip install python-osc


# dans le dossier data/python

Modifier script.py afin de choisir le bon port COM pour la roue

# Lancer script.py & mecanique panorama

Dans le dossier data/script se trouve start_win.bat

Il lance le python et .exe ( avec priorité haute : gain de perf sur windows non négligeable)





# Explications plus en détail


## Logiciel vidéo
localisé dans bin/MecaniquePanorama2025.exe


## Dossier des images

localisé dans /bin/data

* photos
    * 1
        * intro.png + 00001.jpg ...
    * 2
    * 3
    * 4
    * 5

* settings
    * scan.xml ( fichier à modifier à chaque date)
    * corner_settings.xml ( contient la déformation vidéo, en fonction de l'écran)

* python
    * script.py ( lit arduino, envoit OSC)
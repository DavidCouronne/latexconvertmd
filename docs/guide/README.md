---
title: Guide d'utilisation
sidebar: auto
---

# Guide d'utilisation

## Dépendances

+ texsoup
``` bash
pip install texsoup
```
+ dvisvg : à télécharger sur le site [https://dvisvgm.de/](https://dvisvgm.de/)
+ Image Magick
+ Python 3
+ Une distribution LaTeX


## Installation
```bash
python -m pip install --index-url https://test.pypi.org/simple/ latexconvertmd --upgrade
```

## Principes

### Encodage UTF-8

La consersion assume que le fichier source est encodé en UTF-8. Le ou les exports sont aussi en UTF-8.

### Nettoyage du fichier LaTeX

+ Les "mises en forme", comme \vspace, \hspace, \hfill, etc... sont efacées
+ Les espaces ou tabulations en début de ligne sont retirés
+ Les commentaires (%Mon commentaire...) sont effacés
+ Les commandes de mise en page comme \lhead, \rhead, etc... sont effacées

### Convertion de PsStricks et TikZ

Tous les environnements PsStricks et Tikz sont extraits du fichier source, empaquetés dans un fichier temporaire avec une classe `standalone` et les packages du `\header`, compilés en `dvi` avec LaTeX, puis convertis en `svg` avec `dvisvg`. Une balise est alors implémenté dans le fichier source pour l'import des figures.

### Environnements mathématiques

Les envrionnements mathématiques sont laissés tel quel, à quelques exeptions près. Le rendu a été testé avec `Katex v0.10.0`. Si vous utilisez `MathJax` ou un autre moteur de rendu, les résultats peuvent être différents.

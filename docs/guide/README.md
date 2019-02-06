---
author: David Couronné
title: Guide d'utilisation de latexconvertmd
description: katex, latexconvertmd, utilisation katex, markdown
sidebar: auto
---

# Guide d'utilisation

## Dépendances

- dvisvg : à télécharger sur le site [https://dvisvgm.de/](https://dvisvgm.de/)
- Image Magick
- Python 3
- Une distribution LaTeX

## Installation

```bash
python -m pip install --index-url https://test.pypi.org/simple/ latexconvertmd --upgrade
```

## Principes

### Encodage UTF-8

La convertion assume que le fichier source est encodé en UTF-8. Le ou les exports sont aussi en UTF-8.

### Nettoyage du fichier LaTeX

- Les "mises en forme", comme \vspace, \hspace, \hfill, etc... sont effacées
- Les espaces ou tabulations en début de ligne sont retirés
- Les commentaires (%Mon commentaire...) sont effacés
- Les commandes de mise en page comme \lhead, \rhead, etc... sont effacées

### Convertion de PsStricks et TikZ

Tous les environnements PsStricks et Tikz sont extraits du fichier source, empaquetés dans un fichier temporaire avec une classe _standalone_ et les packages du préambule, compilés en _.dvi_ avec LaTeX, puis convertis en _.svg_ avec _dvisvgm_. Une balise est alors implémenté dans le fichier source pour l'import des figures.

### Environnements mathématiques

Les environnements mathématiques sont laissés tel quel, à quelques exeptions près. Le rendu a été testé avec _Katex v0.10.0_. Si vous utilisez _MathJax_ ou un autre moteur de rendu, les résultats peuvent être différents.

### Possibilité de forcer la convertion en svg

Si une partie du code LaTeX ne peut être convertie "simplement" en Markdown, il est possible de marquer dans le fichier source les parties du code à compiler avec LaTeX puis convertir en _svg_.

### Les input et include sont intégrés

Par défaut, tous les _input_ et _include_ sont intégrés dans le Source. Par défaut aussi, si un des fichiers n'est pas trouvé, le _include_ ou _input_ est laissé tel quel.

### tabular et tabularx

Les tableaux

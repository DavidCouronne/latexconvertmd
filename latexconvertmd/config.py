#!/usr/local/bin/python
# -*- coding:utf-8 -*-
# Auteur: David Couronné
# Convertion automatique de LaTeX en Markdown
import re

from latexconvertmd import LaTeXCommands

# Default output folder,name end figure

outputFolder = "export-md"
outputName = "README.md"
outputFigure = "figure"

# Commandes à supprimer avec TexSoup
delCommands = ['vspace',
               'ref'
               'arraycolsep',
               'label',
               'renewcommand',
               'hspace',
               'parindent',
               'raisebox',
               'rhead',
               'lhead',
               'lfoot',
               'rfoot',
               'addtolength',
               'pagestyle',
               'thispagestyle',
               'marginpar']
# Commandes sans argument à supprimer
listeCommandesClean = [LaTeXCommands.LaTeXCommand(r"\\newpage", 0),
                       LaTeXCommands.LaTeXCommand(r"\\hfill", 0),
                       LaTeXCommands.LaTeXCommand(r"\\medskip", 0),
                       LaTeXCommands.LaTeXCommand(r"\\bigskip", 0),
                       LaTeXCommands.LaTeXCommand(r"\\smallskip", 0),
                       LaTeXCommands.LaTeXCommand(r"\\setlength", 0),
                       LaTeXCommands.LaTeXCommand(r"\\Large", 0),
                       LaTeXCommands.LaTeXCommand(r"\\large", 0),
                       LaTeXCommands.LaTeXCommand(r"\\decofourleft", 0),
                       LaTeXCommands.LaTeXCommand(r"\\decofourright", 0),
                       LaTeXCommands.LaTeXCommand(r"\\tableofcontents", 0),
                       LaTeXCommands.LaTeXCommand(r"\\strut", 0),
                       LaTeXCommands.LaTeXCommand(r"\\arraycolsep", 0),
                       ]
# Commandes de mise en page ou de glue avec plusieurs arguments à supprimer
listeCommandesLayout = [LaTeXCommands.LaTeXCommand("\\addtolength", 2)]


# Remplacement de commandes avec un ou plusieurs arguments
listeReplace = [[LaTeXCommands.LaTeXCommand("\\boldmath", 1), [1]],
                [LaTeXCommands.LaTeXCommand("\\textbf", 1), ["**", 1, "**"]],
                [LaTeXCommands.LaTeXCommand("\\emph", 1), [
                    "_", 1, "_"]],
                [LaTeXCommands.LaTeXCommand("\\rm", 1), [
                    1]],
                [LaTeXCommands.LaTeXCommand("\\fbox", 1), [
                    1]],
                [LaTeXCommands.LaTeXCommand("\\mbox", 1), [
                    1]],
                [LaTeXCommands.LaTeXCommand("\\textcolor", 2), [
                    2]],
                [LaTeXCommands.LaTeXCommand("\\np", 1), [
                    1]],
                [LaTeXCommands.LaTeXCommand("\\textsc", 1), [
                    1]],
                [LaTeXCommands.LaTeXCommand("\\widehat", 1), [
                    1]],
                [LaTeXCommands.LaTeXCommand("\\vect", 1), [
                 '\\overrightarrow{', 1, '}']],
                [LaTeXCommands.LaTeXCommand("\\vectt", 1), [
                 '\\overrightarrow{', 1, '}']],
                [LaTeXCommands.LaTeXCommand("\\fexo", 3), [
                 '# ', 2, '\n']],
                ]
# Remplacement de commandes avec aucun argument ou commandes math.
listeReplaceSimple = [[LaTeXCommands.LaTeXCommand(r"\\Ouv", 0), r"(O; $\\vec{u}$, $\\vec{v}$)"],
                      [LaTeXCommands.LaTeXCommand(
                          r"\\Oijk", 0), r"(O; $\\vec{i}$, $\\vec{j}$, $\\vec{k}$)"],
                      [LaTeXCommands.LaTeXCommand(r"\\degres", 0), "°"],
                      # newcommand{\vect}[1]{\overrightarrow{\,\mathstrut#1\,}}
                      # \newcommand{\vectt}[1]{\overrightarrow{\,\mathstrut\text{#1}\,}}% vecteur(AB)
                      #[LaTeXCommands.LaTeXCommand(r"\\vect", 0), r"\\vec"],
                      [LaTeXCommands.LaTeXCommand(r"\\og", 0), " « "],
                      [LaTeXCommands.LaTeXCommand(r"\\fg", 0), " » "],
                      [LaTeXCommands.LaTeXCommand(r"\\e", 0), "e"],
                      [LaTeXCommands.LaTeXCommand(r"\\i", 0), "i"],
                      [LaTeXCommands.LaTeXCommand(
                          r"\\ds", 0), r"\\displaystyle"],
                      ]

# Remplacement sans regex
listeReplaceText = [["\\,\\%", "%"],
                    #["\\\\", "\n\n"],
                    ["\\[", " $$ "],
                    ["\\]", " $$ "],
                    ["pspicture*", "pspicture"],
                    ["\\begin{center}", "\n"],
                    ["\\end{center}", "\n"],
                    ["~", ""],
                    ["\\begin{flushleft}", ""],
                    ["\\end{flushleft}", ""],
                    ["\\end{document}", ""],
                    ["\\newline", "\n\n"],
                    ["\\'e", "é"],
                    ["\\`A", "A"],
                    ["\\begin{equation*}","$$\\begin{matrix}"],
                    ["\\end{equation*}","\\end{matrix}$$"],
                    ["\\begin{equation}","$$\\begin{matrix}"],
                    ["\\end{equation}","\\end{matrix}$$"],

                    ]

# Environnements avec titre optionnel
# Par exemple \begin{definition}[Titre]

listeEnv = [['definition', '::: warning Définition ', ':::'],
            ['definitions', '::: warning Définitions ', ':::'],
            ['remarque', '::: tip Remarque ', ':::'],
            ['remarques', '::: tip Remarques ', ':::'],
            ['exemple', '::: tip Exemple ', ':::'],
            ['propriete', '::: warning Propriété ', ':::'],
            ['proprietes', '::: warning Propriétés ', ':::'],
            ['theoreme', '::: warning Théorème ', ':::'],
            ['methode', '::: tip Méthode ', ':::'],
            ['exercice', '::: tip Exercice ', ':::'],
            ['solution', '<ClientOnly><Solution>', '</Solution>\n\n'], 
            ['preuve', '::: tip Preuve ', ':::'],
            ]

# Tex Header
TEX_HEADER = r"""\documentclass{standalone}
\usepackage{apmep}
\usepackage{dcmaths}
\usepackage{dccornouaille}
\usepackage{dctikz}
\usepackage{dccours}
\usepackage{sesatikz}
%Les packages pstricks
\usepackage{pst-plot,pst-tree,pstricks,pst-node,pst-func}
\usepackage{pst-eucl}
\usepackage{pstricks-add}
\usepackage{pst-all}
\usepackage{eurosym} %Pour le symbole euro: \euro
\usepackage{enumitem}
\usepackage{fourier} %Pour les symboles standards
\usepackage[np]{numprint} % Permet de mettre en forme les nombres
\usepackage{colortbl} %Pour colorer les tableaux
\usepackage{diagbox} %Charge slashbox, calc, keyval, fp, pit2e Permet de faire des diagonales dans un tableau
\usepackage{multicol} %Pour écrire sur plusieurs colonnes
%Pour les tableaux de valeur et de variation
\usepackage{tkz-tab}

\usetikzlibrary{matrix,arrows,decorations.pathmorphing}
% l' unité
\newcommand{\myunit}{1 cm}
%Nouveau type de colonne dans tabularx: C qui correspond à X centré
\newcolumntype{C}{>{\centering\arraybackslash}X}

%On écrit les maths tout le temps en grand
\everymath{\displaystyle}

\tikzset{
    node style sp/.style={draw,circle,minimum size=\myunit},
    node style ge/.style={circle,minimum size=\myunit},
    arrow style mul/.style={draw,sloped,midway,fill=white},
    arrow style plus/.style={midway,sloped,fill=white},
}
\newcommand{\touchecalc}[1]{\fbox{#1}}
\begin{document}

"""

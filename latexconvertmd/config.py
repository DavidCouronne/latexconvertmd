#!/usr/local/bin/python
# -*- coding:utf-8 -*-
# Auteur: David Couronné
# Convertion automatique de LaTeX en Markdown
import re

from latexconvertmd import LaTeXCommands


#Export folder

exportFolder = "export-md"

# Commandes à supprimer avec TexSoup
delCommands = ['vspace',
'renewcommand',
'hspace',
'parindent',
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
                [LaTeXCommands.LaTeXCommand("\\np", 1), [
                    1]],
                [LaTeXCommands.LaTeXCommand("\\textsc", 1), [
                    1]],
                [LaTeXCommands.LaTeXCommand("\\vect", 1), [
                 '\\overrightarrow', 1,'} }']],
                 [LaTeXCommands.LaTeXCommand("\\vectt", 1), [
                 '\\overrightarrow', 1,'} }']],
                ]
# Remplacement de commandes avec aucun argument ou commandes math.
listeReplaceSimple = [[LaTeXCommands.LaTeXCommand(r"\\Ouv", 0), r"(O; $\\vec{u}$, $\\vec{v}$)"],
                      [LaTeXCommands.LaTeXCommand(
                          r"\\Oijk", 0), r"(O; $\\vec{i}$, $\\vec{j}$, $\\vec{k}$)"],
                      [LaTeXCommands.LaTeXCommand(r"\\degres", 0), "°"],
                      #newcommand{\vect}[1]{\overrightarrow{\,\mathstrut#1\,}}
#\newcommand{\vectt}[1]{\overrightarrow{\,\mathstrut\text{#1}\,}}% vecteur(AB)
                      #[LaTeXCommands.LaTeXCommand(r"\\vect", 0), r"\\vec"],
                      [LaTeXCommands.LaTeXCommand(r"\\og", 0), " « "],
                      [LaTeXCommands.LaTeXCommand(r"\\fg", 0), " » "],
                      [LaTeXCommands.LaTeXCommand(r"\\e", 0), "e"],
                      [LaTeXCommands.LaTeXCommand(r"\\i", 0), "i"],
                      [LaTeXCommands.LaTeXCommand(r"\\ds", 0), r"\\displaystyle"],
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
                    ["\\strut", ""],

                    ]

# Environnements avec titre optionnel
# Par exemple \begin{definition}[Titre]

listeEnv = [['definition','::: tip ',':::'],
]
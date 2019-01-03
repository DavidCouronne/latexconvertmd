#!/usr/local/bin/python
# -*- coding:utf-8 -*-
# Auteur: David Couronné
# Convertion automatique de LaTeX en Markdown

import re
import os
import codecs

from TexSoup import TexSoup

from latexconvertmd import LaTeXCommands, config


class Source:
    def __init__(self, original="", exportFolder = config.exportFolder):
        self.original = original  # On garde l'original pour développement
        self.contenu = original
        self.lines = self.contenu.splitlines()
        self.exportFolder = exportFolder
        self.nbfigure = 0

    def collapseLines(self):
        """Recolle les lignes dans self.contenu"""
        self.contenu = "\n".join(self.lines)

    def cleanSpace(self):
        """Agit sur les lignes.
        Enlève les espaces en début et fin de chaque ligne"""
        new_lines = []
        for line in self.lines:
            line = line.strip()
            new_lines.append(line)
        self.lines = new_lines

    def cleanCommand(self):
        """Agit sur le contenu.
        Supprime toutes les commandes de listeCommandesClean et delCommand du fichier config.py
        Et au passage gère les sections et subsections"""
        soup = TexSoup(self.contenu)
        for section in soup.find_all('section'):
            section.replace('## '+section.string)
        for subsection in soup.find_all('subsection'):
            subsection.replace('### '+subsection.string)
        for command in config.delCommands: 
            for include in soup.find_all(command):       
                include.delete()
        self.contenu = repr(soup)
        for command in config.listeCommandesClean:
            self.contenu = re.sub(command.regex, "", self.contenu)
            self.lines = self.contenu.splitlines()

    def cleanLayout(self):
        """Agit sur le contenu.
        Supprime toutes les commandes de listeLayout du fichier config.py"""
        for command in config.listeCommandesLayout:
            self.contenu = command.cleanCommand(self.contenu)

    def replaceCommandSimple(self):
        """Agit sur le contenu.
        Remplace les commandes sans arguments"""
        for command, replace in config.listeReplaceSimple:
            self.contenu = re.sub(command.regex, replace, self.contenu)

    def replaceCommand(self):
        """Agit sur le contenu.
        Remplace toutes les commande de listeReplace de config.py"""
        for command, arg in config.listeReplace:
            #print("commande", command)
            #print("arg", arg)
            self.contenu = command.replaceCommand(self.contenu, arg)

    def replaceText(self):
        """Agit sur le contenu.
        Remplacement simple sans regex"""
        for texaremplacer, textederemplacement in config.listeReplaceText:
            self.contenu = self.contenu.replace(
                texaremplacer, textederemplacement)

    def convertEnumerate(self):
        """Agit sur les lignes.
        Converti les environnements enumerate en listes html"""
        level_enumerate = 0
        level_item = 0
        enumi = 0
        enumii = 0
        new_lines = []
        arabic = "abcdefghijklmnopqrstuvwxz"

        for line in self.lines:
            if r"\begin{enumerate}" in line:
                level_enumerate = level_enumerate + 1
                line = ""
            elif r"\end{enumerate}" in line:
                if level_enumerate == 2:
                    enumii = 0
                else:
                    enumi = 0
                level_enumerate = level_enumerate - 1
                line = ""
            elif r"\item" in line and level_enumerate !=0:
                if level_enumerate == 1:
                    enumi = enumi + 1
                    line = line.replace(r"\item", str(enumi)+". ")
                    line = "\n\n" + line
                else:
                    line = line.replace(r"\item", arabic[enumii]+") ")
                    enumii = enumii + 1
                    line = "\n\n" + line
            new_lines.append(line)
        self.lines = new_lines

    def convertItemize(self):
        """Agit sur les lignes.
        Converti les environnements itemize en listes html"""
        level_itemize = 0
        level_item = 0
        new_lines = []

        for line in self.lines:
            if r"\begin{itemize}" in line:
                line = "\n\n"
            elif r"\end{itemize}" in line:
                line = "\n\n"
            elif r"\item" in line:
                line = line.replace(r"\item", "\n\n+ ")
            new_lines.append(line)
        self.lines = new_lines

    def findPstricks(self):
        """Agit sur les lignes.
        Essaie de trouver les envir
        onnements Pstricks"""
        in_pstricks = False
        lignes_pstricks = []
        pstricks = []
        for line in self.lines:
            if in_pstricks:
                lignes_pstricks.append(line)
                if r"\end{pspicture" in line:
                    in_pstricks = False
                    pstricks.append("\n".join(lignes_pstricks))
                    lignes_pstricks = []
            else:
                if r"\psset" in line or r"\begin{pspicture" in line:
                    in_pstricks = True
                    lignes_pstricks.append(line)
        self.pstricks = pstricks

    def replacePstricks(self):
        if len(self.pstricks) == 0:
            return
        preamble = r"""\documentclass{standalone}
\usepackage{pst-plot,pst-tree,pstricks,pst-node,pst-text}
\usepackage{pst-eucl}
\usepackage{pstricks-add}
\usepackage[frenchb]{babel}
\newcommand{\vect}[1]{\overrightarrow{\,\mathstrut#1\,}}
\begin{document}

"""
        
        for figure in self.pstricks:
            self.nbfigure = self.nbfigure + 1
            total = preamble + figure + r"\end{document}"
            f = codecs.open("temp.tex", "w", "utf-8")
            f.write(total)
            f.close()
            os.system("latex temp.tex")
            os.system("dvisvgm temp")
            try:
                os.rename("temp.svg", "figure"+str(self.nbfigure)+".svg")
            except:
                print("Le fichier figure"+str(self.nbfigure)+".svg existe déjà")
            self.contenu = self.contenu.replace(
                figure,
                '![Image](./figure'+str(self.nbfigure)+".svg)")

    def process(self):
        """Effectue les taches de conversion"""
        # Opérations sur les lignes
        self.cleanSpace()
        self.convertEnumerate()
        # self.convertItemize()
        self.findPstricks()
        # Opérations sur le contenu
        self.contenu = self.contenu.replace("{}", "")
        self.collapseLines()
        self.replacePstricks()
        self.cleanCommand()
        self.replaceCommand()
        self.cleanLayout()
        self.replaceCommandSimple()
        self.replaceText()

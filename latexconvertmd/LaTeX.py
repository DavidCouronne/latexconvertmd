#!/usr/local/bin/python
# -*- coding:utf-8 -*-
# Auteur: David Couronné
# Convertion automatique de LaTeX en Markdown

import codecs
import os
import re

from latexconvertmd import LaTeXCommands, config
from slugify import slugify
from TexSoup import TexSoup


class Source:
    def __init__(self, original="", exportFolder=config.outputFolder, file=False):
        self.original = original  # On garde l'original pour développement
        self.contenu = original
        self.manipFiles = True # Manipulation de fichiers
        self.lines = self.contenu.splitlines()
        self.exportFolder = exportFolder
        self.nbfigure = 0
        self.exo = 0
        if file != False:
            self.outputFolder = slugify(file)

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

    def cleanRem(self):
        """Agit sur les lignes.
        Enlèves toutes les remarques %"""
        self.collapseLines()  # On commence par protégéer les \%
        self.contenu = self.contenu.replace("\\%", "!!rem!!")
        self.lines = self.contenu.splitlines()
        new_lines = []
        for line in self.lines:
            remarque = line.find("%")
            if remarque != -1:
                line = line[:remarque]
            new_lines.append(line)
        self.lines = new_lines
        self.collapseLines()
        self.contenu = self.contenu.replace("!!rem!!", "\\%")
        self.lines = self.contenu.splitlines()

    def cleanLines(self):
        """Agit sur le contenu.
        Supprime les lignes vides"""
        while "\n\n\n" in self.contenu:
            self.contenu = self.contenu.replace("\n\n\n", "\n\n")

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
            if r"\begin{enumerate}" in line or r"\begin{colenumerate}" in line:
                level_enumerate = level_enumerate + 1
                line = ""
            elif r"\end{enumerate}" in line or r"\end{colenumerate}" in line:
                if level_enumerate == 2:
                    enumii = 0
                else:
                    enumi = 0
                level_enumerate = level_enumerate - 1
                line = ""
            elif r"\item" in line and level_enumerate != 0:
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
    
    def findConvert(self):
        """Agit sur les lignes.
        Essaie de trouver les envir
        onnements Convert"""
        in_convert = False
        lignes_convert = []
        convert = []
        for line in self.lines:
            if in_convert:
                lignes_convert.append(line)
                if r"\end{convert}" in line:
                    in_convert = False
                    convert.append("\n".join(lignes_convert))
                    lignes_convert = []
            else:
                if r"\begin{convert}" in line:
                    in_convert = True
                    lignes_convert.append(line)
        self.convert = convert

    def findTikz(self):
        """Agit sur les lignes.
        Essaie de trouver les envir
        onnements Tikz"""
        in_tikz = False
        lignes_tikz = []
        tikz = []
        for line in self.lines:
            if in_tikz:
                lignes_tikz.append(line)
                if r"\end{tikz" in line:
                    in_tikz = False
                    tikz.append("\n".join(lignes_tikz))
                    lignes_tikz = []
            else:
                if r"\begin{tikz" in line:
                    in_tikz = True
                    lignes_tikz.append(line)
        self.tikz = tikz

    def findTab(self):
        """Agit sur les lignes.
        Essaie de trouver les envir
        onnements tab..."""
        in_tab = False
        lignes_tab = []
        tab = []
        for line in self.lines:
            if in_tab:
                lignes_tab.append(line)
                if r"\end{tab" in line:
                    in_tab = False
                    tab.append("\n".join(lignes_tab))
                    lignes_tab = []
            else:
                if r"\begin{tab" in line:
                    in_tab = True
                    lignes_tab.append(line)
        self.tab = tab

    def replacePstricks(self):
        if len(self.pstricks) == 0:
            return
        preamble = config.TEX_HEADER

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

    def replaceConvert(self):
        self.collapseLines()
        if len(self.convert) == 0:
            return
        preamble = config.TEX_HEADER

        for figure in self.convert:
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
            print(figure)
            self.contenu = self.contenu.replace(
                figure,
                '![Image](./figure'+str(self.nbfigure)+".svg)")
        self.lines = self.contenu.splitlines()

    def replaceTikz(self):
        if len(self.tikz) == 0:
            return
        preamble = config.TEX_HEADER

        for figure in self.tikz:
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

    def processGraphics(self):
        """Remplace les \includegraphics"""
        if "includegraphics" in self.contenu:
            graphic = self.contenu.split(r"\includegraphics")
            self.contenu = graphic[0]
            for i in range(len(graphic)-1):
                apres = graphic[i+1]
                #apres = apres[apres.find("{")+1:]
                commande = "\\includegraphics"+apres[:apres.find("}")+1]
                self.nbfigure = self.nbfigure + 1
                total = config.TEX_HEADER + commande + r"\end{document}"
                f = codecs.open("temp.tex", "w", "utf-8")
                f.write(total)
                f.close()
                os.system("xelatex temp.tex")
                os.system("magick convert temp.pdf temp.png")
                try:
                    os.rename("temp.png", "figure"+str(self.nbfigure)+".png")
                except:
                    print("Le fichier figure" +
                          str(self.nbfigure)+".png existe déjà")
                apres = apres[apres.find("}")+1:]
                self.contenu = self.contenu + \
                    ' ![Image](./figure'+str(self.nbfigure)+".png) "+apres

    def processTab(self, intab):
        """Convertit le contenu d'un tabular ou tabularx en Markdown"""
        tableau = ""
        delemiteur = ""

        intab = intab.replace("\\hline", '')
        lines = intab.split("\n")
        newlines = []
        for line in lines:
            if line == '':
                pass
            else:
                nbRow = line.count('&')
                line = line.replace("\\\\", '').replace("&", " | ")
                line = "| " + line + " |"
                newlines.append(line)
                delemiteur = ""
                for i in range(nbRow + 1):
                    delemiteur = delemiteur + "|---"
                delemiteur = delemiteur + "|"

        for i in range(len(newlines)):
            if i == 1:
                tableau = tableau + delemiteur + "\n"+newlines[1] + "\n"
            else:
                tableau = tableau + newlines[i] + "\n"
        return tableau

    def soupTab(self):
        """Utilise TexSoup pour tabular et tabularx"""
        soup = TexSoup(self.contenu)
        for tabu in soup.find_all('tabular'):
            print(tabu)
            arg = []
            for i in tabu.contents:
                arg.append(str(i))
            intab = "".join(arg)
            tableau = self.processTab(intab)
            self.contenu = self.contenu.replace(repr(tabu), tableau)

    def replaceTab(self):
        if len(self.tab) == 0:
            return
        preamble = config.TEX_HEADER

        for figure in self.tab:
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

    def checkEnv(self):
        for arg in config.listeEnv:
            begin = "\\begin{"+arg[0]+"}"
            end = "\\end{"+arg[0]+"}"
            self.contenu = self.contenu.replace(begin, arg[1])
            self.contenu = self.contenu.replace(end, arg[2])
    
    def convertExos(self):
        self.contenu = self.contenu.replace('\\end{exercice}',':::\n\n')
        self.lines = self.contenu.split('\n')
        newlines = []
        for line in self.lines:
            if "\\begin{exercice}" in line:
                self.exo = self.exo + 1
                line = line.replace('\\begin{exercice}','::: tip Exercice '+str(self.exo)+' ')
            newlines.append(line)
        self.lines = newlines
        self.collapseLines()

    def process(self):
        """Effectue les taches de conversion"""
        # Opérations sur les lignes
        self.cleanSpace()
        self.cleanRem()
        self.findConvert()
        if self.manipFiles:
            self.replaceConvert()
        self.findPstricks()
        self.findTikz()
        self.findTab()

        # Convertion tabular
        self.collapseLines()
        self.soupTab()
        # Convertion PsTricks TikZ Images
        if self.manipFiles:
            self.replacePstricks()
            self.replaceTikz()
            self.processGraphics()
        # Enumerate et Itemize
        self.lines = self.contenu.splitlines()
        self.convertEnumerate()
        self.convertItemize()

        # Opérations sur le contenu
        self.collapseLines()
        self.convertExos()
        self.checkEnv()
        self.cleanCommand()
        self.replaceCommand()
        self.cleanLayout()
        self.replaceCommandSimple()
        self.replaceText()
        self.contenu = self.contenu.replace("{}", "")
        self.contenu = self.contenu.replace("[ ]", "")
        #self.contenu = self.contenu.replace("\\\\", "\n\n")
        self.cleanLines()

#!/usr/local/bin/python
# -*- coding:utf-8 -*-
# Auteur: David Couronné
# Convertion automatique de LaTeX en Markdown

import re
import os

class LaTeXCommand:
    def __init__(self, nom, arg=1, optn=False):
        self.nom = nom
        self.arg = arg
        self.optn = optn
        if arg == 0:
            self.regex = re.compile(self.nom + r"\b")
        #if arg == 1:
        #    self.regex = re.compile(self.nom + r"\{([\d|\w|\.|-|,|\\]*)\}")
            

    def find(self, contenu):
        return contenu.find(self.nom)

    def findCommand(self, texte):
        index = texte.find(self.nom)
        avant = texte[:index]
        apres = texte[index+len(self.nom):]
        argOptn = ""
        listeArg = []
        if self.optn:
            if apres[0] == "[":
                i = 0
                while apres[i] != "]":
                    i = i + 1
                argOptn = apres[1:i]
                apres = apres[i+2:]
            else:
                apres = apres[1:]
        else:
            apres = apres[1:]
        argRest = self.arg
        avantManip = "{"+apres
        while argRest != 0:
            argRest = argRest - 1
            ouvert2 = apres.find("{")
            ferme1 = apres.find("}")
            if ouvert2 == -1:
                ouvert2 = ferme1
            while ouvert2 < ferme1:
                ouvert2 = apres.find("{", ferme1+1)
                ferme1 = apres.find("}", ferme1+1)
            listeArg.append(apres[:ferme1])
            apres = apres[ferme1+2:]
        longueurArgument = 0
        for argument in listeArg:
            longueurArgument = longueurArgument + len(argument)+2

        apres = avantManip[longueurArgument:]
        return index, avant, apres, argOptn, listeArg

    def cleanCommand(self, contenu):
        passe = 0
        while self.nom in contenu:
            #print(self.nom)
            passe = passe + 1
            index, avant, apres, argOptn, listeArg = self.findCommand(contenu)
            # print("Passe"+str(passe),apres)
            contenu = avant+apres
        return contenu

    def replaceCommand(self, contenu, listeReplace):
        while self.nom in contenu:
            index, avant, apres, argOptn, listeArg = self.findCommand(contenu)
            texte = ""
            for argument in listeReplace:
                if type(argument) is type("c"):
                    texte = texte + argument
                elif argument == 0:
                    texte = texte + "[" + argOptn + "]"
                else:
                    texte = texte  + listeArg[argument-1] 
            contenu = avant + texte + apres
        return contenu

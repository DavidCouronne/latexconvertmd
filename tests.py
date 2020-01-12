import codecs
import os

from latexconvertmd import LaTeX, config

print(os.path.join(os.getcwd(), "test"))
os.chdir(os.path.join(os.getcwd(), "tests"))
file = "cours.tex"

with codecs.open(file, "r", "utf-8") as f:
    data = f.read()

texheader, document = data.split("\\begin{document}")


latex = LaTeX.Source(document, file=file)

# Tests sans agir sur les fichiers
latex.manipFiles = True
# latex.process()
latex.cleanSpace()
latex.cleanRem()
latex.findConvert()
latex.replaceConvert()
latex.findPstricks()
latex.findTikz()
latex.findTab()
latex.collapseLines()
# #latex.soupTab()  #Probleme ici !
latex.replacePstricks()
latex.replaceTikz()
# Enumerate et Itemize
latex.lines = latex.contenu.splitlines()
latex.convertEnumerate()
latex.convertItemize()

# Opérations sur le contenu
latex.collapseLines()
latex.convertExos()
latex.checkEnv()
latex.cleanCommand()
latex.replaceCommand()
latex.cleanLayout()
latex.replaceCommandSimple()
latex.replaceText()
latex.contenu = latex.contenu.replace("{}", "")
latex.contenu = latex.contenu.replace("[ ]", "")
#self.contenu = self.contenu.replace("\\\\", "\n\n")
latex.cleanLines()
name = "README.md"
total = texheader + "\\begin{document}\n\n" + latex.contenu
contenu = """---
sidebar: auto
author: David Couronné
---
""" + latex.contenu
f = codecs.open(name, "w", "utf-8")
f.write(contenu)
f.close()

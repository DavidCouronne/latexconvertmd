from latexconvertmd import LaTeX, config
import codecs
import os

print(os.path.join(os.getcwd(),"test"))
os.chdir(os.path.join(os.getcwd(),"tests"))
file = "TS-Exos-Partie2.tex"

with codecs.open(file, "r", "utf-8") as f:
    data = f.read()

texheader, document = data.split("\\begin{document}")


latex = LaTeX.Source(document, file=file)

#Tests sans agir sur les fichiers
#latex.manipFiles = False
latex.process()

name = "README.md"
total = texheader + "\\begin{document}\n\n" + latex.contenu
contenu = """---
sidebar: auto
---
""" + latex.contenu
f = codecs.open(name, "w", "utf-8")
f.write(contenu)
f.close()

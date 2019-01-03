from latexconvertmd import LaTeX, config
import codecs

file = "Corrige_S_Nouvelle_Caledonie_27_nov_2018_FH.tex"

with codecs.open(file, "r", "utf-8") as f:
    data = f.read()

texheader, document = data.split("\\begin{document}")


latex = LaTeX.Source(document)
latex.process()

name = "export.md"
total = texheader + "\\begin{document}\n\n" + latex.contenu
f = codecs.open(name, "w", "utf-8")
f.write(latex.contenu)
f.close()

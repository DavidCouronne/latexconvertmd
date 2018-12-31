from latexconvertmd import LaTeX, setup
import codecs

file = "S_Nouvelle_Caledonie_27_nov_2018_FH.tex"

with codecs.open(file, "r","utf-8") as f: data = f.read()

texheader, document = data.split("\\begin{document}")
document = r"""\textbf{2cm}

\setlength\parindent{0mm}1
\rhead{\textbf{A. P{}. M. E. P{}.}2}

\lhead{\small Baccalauréat S}
\lfoot{\small{Nouvelle Calédonie}}
\rfoot{\small{27 novembre 2018}}
\addtolength{\headheight}{\baselineskip}
\pagestyle{fancy}
\thispagestyle{empty}
\marginpar{\rotatebox{90}{\textbf{A. P{}.  M. E. P{}.}}}
"""
latex = LaTeX.Source(document)
latex.process()

name = "export.md"
total = texheader + "\\begin{document}\n\n" + latex.contenu
f = codecs.open(name, "w", "utf-8")
f.write(latex.contenu)
f.close()
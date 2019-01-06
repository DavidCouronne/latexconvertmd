---
author: David Couronné
title: Guide katex
description: katex, latexconvertmd, utilisation katex, markdown
sidebar: auto
---

# Syntaxe de base

## Maths en ligne

```md
$\sqrt{2}$
```

$\sqrt{2}$

::: warning Attention
Il faut bien "coller" les $ à l'expression !
:::

Exemple:

``` md
$\sqrt{2} $
```

$\sqrt{2} $

La convertion automatique avec `latexconvertmd` ne gère pas (encore) ce genre de situation.

::: tip Astuce
On peut "passer à la ligne" !
:::

``` md
$f(x)=(x-1)(x+2)\\
\phantom{f(x)}=x^2+2x-x-2\\
\phantom{f(x)}=x^2+x-2$
```

$f(x)=(x-1)(x+2)\\
\phantom{f(x)}=x^2+2x-x-2\\
\phantom{f(x)}=x^2+x-2$

## Maths en block

```  md
$$\lim_{x \to +\infty} \frac{1}{x}=0$$
```

$$\lim_{x \to +\infty} \frac{1}{x}=0$$

::: warning Attention
Ne rien mettre avant ou après les $$
:::

Exemple:



```  md
$$\lim_{x \to +\infty} \frac{1}{x}=0$$.
```

\lim_{x \to +\infty }\frac{1}{x}=0$$.


Le problème vient du petit point après les $$ !!!


La convertion automatique avec `latexconvertmd` ne gère pas (encore) ce genre de situation.

## Problèmes rencontrés

::: danger
Katex n'est pas LaTeX !!!
:::

KaTeX est juste un moteur de rendu des environnements mathématiques en Markdown ou HTML. Mais ce n'est pas le compilateur LaTeX :)


1. Mieux vaut `matrix`que `array`
2. Katex n'aime pas le surplus d'accolades

```md
$\frac{{5}\pi}{{6}}}$
```
Ca fait planter Katex...

# markdown-it-katex

En fait ce n'est pas vraiment katex que nous utilisons en markdown, mais markdown-it-katex.

Le problème que j'ai rencontré avec markdown-it-katex est l'impossibilité de définir des commandes globales. Ca marche très bien avec katex en HTML, mais en markdown je n'ai pas trouvé le moyen de le faire de manière "simple".

## Hacker markdown-it-katex

On trouve la source sur [Github](https://github.com/waylonflinn/markdown-it-katex)

Pour l'utilsation Javascript la documentation donne:

```js
var md = require('markdown-it')(),
    mk = require('markdown-it-katex');

md.use(mk);
```

Pour pouvoir définir des \newcommand ou autre de manière globale, on va transformer un peu le fichier source de markdown-it-katex:

Dans un coin de votre projet, créer un dossier `param-katex` par exemple.

Dans ce dossier, créer trois fichiers: `index.js` , `macroskatex.js` et `newcommands.js`.

Le fichier `macroskatex.js` va contenir les macros avec la syntaxe katex:

```js
const macroskatex = {
    "\\RR": "\\mathbb{R}"
};
exports.macroskatex = macroskatex;
```

Le fichier `newcommands.js` va contenir les \newcommand avec la syntaxe LaTeX:

```js
const newcommand = "\\newcommand{\\vect}[1]{\\overrightarrow{#1}}";
newcommand = newcommand + "\\newcommand{\\C}{\\mathbb{C}}"
exports.newcommand = newcommand;
```

Il y a surement moyent de faire plus simple avec des listes, mais je ne suis pas spécialiste de JavaScript ;)

Le fichier `index.js`ve contenir le code de markdown-it-katex avec nos imports:

```js {13,15}
/* Process inline math */
/*
Like markdown-it-simplemath, this is a stripped down, simplified version of:
https://github.com/runarberg/markdown-it-math

It differs in that it takes (a subset of) LaTeX as input and relies on KaTeX
for rendering output.
*/

/*jslint node: true */
'use strict';

const { macroskatex } = require("./macroskatex");

const { newcommand } = require("./newcommand");

var katex = require('katex');
```


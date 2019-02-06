---
author: David Couronné
title: Guide katex
description: markdown-it-katex, katex, latexconvertmd, utilisation katex, markdown
sidebar: auto
---

# Syntaxe de base

## Maths en ligne

```md
$\sqrt{2}$
```

$\sqrt{2}$

::: warning Attention
Il faut bien "coller" les \$ à l'expression !
:::

Exemple:

```md
$\sqrt{2} $
```

$\sqrt{2} $

La convertion automatique avec `latexconvertmd` ne gère pas (encore) ce genre de situation.

::: tip Astuce
On peut "passer à la ligne" !
:::

```md
$f(x)=(x-1)(x+2)\\
\phantom{f(x)}=x^2+2x-x-2\\
\phantom{f(x)}=x^2+x-2$
```

$f(x)=(x-1)(x+2)\\
\phantom{f(x)}=x^2+2x-x-2\\
\phantom{f(x)}=x^2+x-2$

## Maths en block

```md
$$\lim_{x \to +\infty} \frac{1}{x}=0$$
```

$$\lim_{x \to +\infty} \frac{1}{x}=0$$

::: warning Attention
Ne rien mettre avant ou après les \$\$
:::

Exemple:

```md
$$\lim_{x \to +\infty} \frac{1}{x}=0$$.
```

\lim\_{x \to +\infty }\frac{1}{x}=0\$\$.

Le problème vient du petit point après les \$\$ !!!

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
var md = require("markdown-it")(),
  mk = require("markdown-it-katex");

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
newcommand = newcommand + "\\newcommand{\\C}{\\mathbb{C}}";
exports.newcommand = newcommand;
```

Il y a surement moyent de faire plus simple avec des listes, mais je ne suis pas spécialiste de JavaScript ;)

Le fichier `index.js`ve contenir le code de markdown-it-katex avec nos imports:

```js
/* Process inline math */
/*
Like markdown-it-simplemath, this is a stripped down, simplified version of:
https://github.com/runarberg/markdown-it-math

It differs in that it takes (a subset of) LaTeX as input and relies on KaTeX
for rendering output.
*/

/*jslint node: true */
"use strict";

const { macroskatex } = require("./macroskatex");

const { newcommand } = require("./newcommand");

var katex = require("katex");
// Test if potential opening or closing delimieter
// Assumes that there is a "$" at state.src[pos]
function isValidDelim(state, pos) {
  var prevChar,
    nextChar,
    max = state.posMax,
    can_open = true,
    can_close = true;

  prevChar = pos > 0 ? state.src.charCodeAt(pos - 1) : -1;
  nextChar = pos + 1 <= max ? state.src.charCodeAt(pos + 1) : -1;

  // Check non-whitespace conditions for opening and closing, and
  // check that closing delimeter isn't followed by a number
  if (
    prevChar === 0x20 /* " " */ ||
    prevChar === 0x09 /* \t */ ||
    (nextChar >= 0x30 /* "0" */ && nextChar <= 0x39) /* "9" */
  ) {
    can_close = false;
  }
  if (nextChar === 0x20 /* " " */ || nextChar === 0x09 /* \t */) {
    can_open = false;
  }

  return {
    can_open: can_open,
    can_close: can_close
  };
}

function math_inline(state, silent) {
  var start, match, token, res, pos, esc_count;

  if (state.src[state.pos] !== "$") {
    return false;
  }

  res = isValidDelim(state, state.pos);
  if (!res.can_open) {
    if (!silent) {
      state.pending += "$";
    }
    state.pos += 1;
    return true;
  }

  // First check for and bypass all properly escaped delimieters
  // This loop will assume that the first leading backtick can not
  // be the first character in state.src, which is known since
  // we have found an opening delimieter already.
  start = state.pos + 1;
  match = start;
  while ((match = state.src.indexOf("$", match)) !== -1) {
    // Found potential $, look for escapes, pos will point to
    // first non escape when complete
    pos = match - 1;
    while (state.src[pos] === "\\") {
      pos -= 1;
    }

    // Even number of escapes, potential closing delimiter found
    if ((match - pos) % 2 == 1) {
      break;
    }
    match += 1;
  }

  // No closing delimter found.  Consume $ and continue.
  if (match === -1) {
    if (!silent) {
      state.pending += "$";
    }
    state.pos = start;
    return true;
  }

  // Check if we have empty content, ie: $$.  Do not parse.
  if (match - start === 0) {
    if (!silent) {
      state.pending += "$$";
    }
    state.pos = start + 1;
    return true;
  }

  // Check for valid closing delimiter
  res = isValidDelim(state, match);
  if (!res.can_close) {
    if (!silent) {
      state.pending += "$";
    }
    state.pos = start;
    return true;
  }

  if (!silent) {
    token = state.push("math_inline", "math", 0);
    token.markup = "$";
    token.content = state.src.slice(start, match);
  }

  state.pos = match + 1;
  return true;
}

function math_block(state, start, end, silent) {
  var firstLine,
    lastLine,
    next,
    lastPos,
    found = false,
    token,
    pos = state.bMarks[start] + state.tShift[start],
    max = state.eMarks[start];

  if (pos + 2 > max) {
    return false;
  }
  if (state.src.slice(pos, pos + 2) !== "$$") {
    return false;
  }

  pos += 2;
  firstLine = state.src.slice(pos, max);

  if (silent) {
    return true;
  }
  if (firstLine.trim().slice(-2) === "$$") {
    // Single line expression
    firstLine = firstLine.trim().slice(0, -2);
    found = true;
  }

  for (next = start; !found; ) {
    next++;

    if (next >= end) {
      break;
    }

    pos = state.bMarks[next] + state.tShift[next];
    max = state.eMarks[next];

    if (pos < max && state.tShift[next] < state.blkIndent) {
      // non-empty line with negative indent should stop the list:
      break;
    }

    if (
      state.src
        .slice(pos, max)
        .trim()
        .slice(-2) === "$$"
    ) {
      lastPos = state.src.slice(0, max).lastIndexOf("$$");
      lastLine = state.src.slice(pos, lastPos);
      found = true;
    }
  }

  state.line = next + 1;

  token = state.push("math_block", "math", 0);
  token.block = true;
  token.content =
    (firstLine && firstLine.trim() ? firstLine + "\n" : "") +
    state.getLines(start + 1, next, state.tShift[start], true) +
    (lastLine && lastLine.trim() ? lastLine : "");
  token.map = [start, state.line];
  token.markup = "$$";
  return true;
}

module.exports = function math_plugin(md, options) {
  // Default options

  options = options || {};

  // set KaTeX as the renderer for markdown-it-simplemath
  var katexInline = function(latex) {
    options.displayMode = false;
    options.throwOnError = false;
    options.macros = macroskatex;
    latex = newcommand + latex;

    try {
      return katex.renderToString(latex, options);
    } catch (error) {
      if (options.throwOnError) {
        console.log(error);
      }
      return latex;
    }
  };

  var inlineRenderer = function(tokens, idx) {
    return katexInline(tokens[idx].content);
  };

  var katexBlock = function(latex) {
    options.displayMode = true;
    options.throwOnError = false;
    options.macros = macroskatex;
    latex = newcommand + latex;
    try {
      return "<p>" + katex.renderToString(latex, options) + "</p>";
    } catch (error) {
      if (options.throwOnError) {
        console.log(error);
      }
      return latex;
    }
  };

  var blockRenderer = function(tokens, idx) {
    return katexBlock(tokens[idx].content) + "\n";
  };

  md.inline.ruler.after("escape", "math_inline", math_inline);
  md.block.ruler.after("blockquote", "math_block", math_block, {
    alt: ["paragraph", "reference", "blockquote", "list"]
  });
  md.renderer.rules.math_inline = inlineRenderer;
  md.renderer.rules.math_block = blockRenderer;
};
```

Au passage j'ai mis `throwOnError = false` pour bien voir les erreurs de rendu.

Reste à l'implémenter:

```js
var md = require("markdown-it")(),
  mk = require("./param-katex"); //Chemin du dossier param-katex

md.use(mk);
```

Ne pas oublier d'ajouter katex au `package.json`

```bash
yarn add katex
```

Et le lien qui va bien pous le CSS:

```html
<link
  rel="stylesheet"
  href="https://cdn.jsdelivr.net/npm/katex@0.10.0/dist/katex.min.css"
  integrity="sha384-9eLZqc9ds8eNjO3TmqPeYcDj8n+Qfa4nuSiGYa6DjLNcv9BtN69ZIulL9+8CqC9Y"
  crossorigin="anonymous"
/>
```

Bien sûr on ne peut avoir les mises à jour de markdown-it-katex, mais comme la dernière date de 2016... :)

`Latest commit 81b84a7 on 10 Oct 2016`

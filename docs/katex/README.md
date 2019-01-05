---
sidebar: auto
title: Guide Katex
---

# Syntaxe de base

## Maths en ligne

```md
$\sqrt{2}$
```

$\sqrt{2}$

::: warning Attention
+ Il faut bien "coller" les $ à l'expression
+ Impossible de "passer à la ligne" si il y a du texte avant, ou après un $.
:::

Exemples:

``` md
$\sqrt{2} $
```

$\sqrt{2} $

``` md
On a $f(x)=(x+3)^2
=x^2+6x+9$
```

On a $f(x)=(x+3)^2
=x^2+6x+9$

La convertion automatique avec `latexconvertmd` ne gère pas (encore) ce genre de situations.
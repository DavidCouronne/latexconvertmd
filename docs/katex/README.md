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
Il faut bien "coller" les $ à l'expression !
:::

Exemple:

``` md
$\sqrt{2} $
```

On peut "passer à la ligne":
$\sqrt{2} $

``` md
$f(x)=(x-1)(x+2)
\phantom{f(x)}=x^2+2x-x-2
\phantom{f(x)}=x^2+x-2$
```

$f(x)=(x-1)(x+2)
\phantom{f(x)}=x^2+2x-x-2
\phantom{f(x)}=x^2+x-2$

La convertion automatique avec `latexconvertmd` ne gère pas (encore) ce genre de situations.
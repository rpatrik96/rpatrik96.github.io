---
title: 'LaTeX tricks'
date: 2022-05-22
permalink: /posts/2022/05/latex-tricks/
tags:
  - LaTeX
  - writing
  - materials
---

Improve typesetting and save space in your submissions, who does not want that?

# Preamble
An academic paper is not just a messenger of hopefully ground-breaking results, but also a story and a visual manifesto. If it's badly-formatted, there are dangling words in almost empty lines, inconsistent notation, readers might give up with reading. On the other side, if everything is nice but this results in a too-long article, then besides risking a desk-rejection (or the payment of extra fees for exceeding the page limit), readers will be less enthusiastic about facing so much text. Your results can be fascinating, if no one reads them, you failed your goal. 

There are several best practices to ensure that your submission looks professional, eases the reader's task, and fits into the page limit. I will assume that you are using LaTeX (you should), and provide my two cents on what I found especially useful. 

# Typesetting
You want that your text looks great and saves space. This is how you do it.

## Fighting almost-empty lines
When the last few words of a sentence start a new line, it will look awkward and will waste you a lot of space. The solution is to instruct LaTeX to squeeze the words together _a bit_. This can be done with the command `\looseness-1` what you place in front of a paragraph and enjoy the result.

## Keeping in-text equations together
Equations should be kept together, i.e., they should not be spread across lines when provided in-text. The easy fix is to but curly braces around them. So `$y=f(x)$` can be split, but `${y=f(x)}$` cannot.

## More compact fractions
In-text fractions can take up lot of space and destroy the homogeneity of the paragraph by requiring more space between lines. A possible solution is using `\usepackage{nicefrac} ` and the `\nicefrac{}{}` command, which will save you space.

## More compact lists
Both the `enumerate` and `itemize` environments waste a lot of space between lines by default. So much space also suggests less coherence of the items in the list. With the `nolistsep` option, the spacing between lines is reduced---the `leftmargin=*` option will save some more space by starting the items right at the left (pun intended).

```latex
\begin{itemize}
    % [nolistsep]
    [nolistsep,leftmargin=*]
    \item ...
    \item ...
\end{itemize}
```

# References
LaTeX has commands such as `\eqref{}, \autoref{}, \ref{}` that work fine, though what I started to like recently is the `cleveref` package with its `\cref{}` command. This will put the paragraph symbol "§" when referring to sections, saving a lot of space (and making it easier for the reader to find the cross-references in the paper).

All you need is include this script.
```latex
\usepackage{cleveref}

\crefname{section}{\S}{\S\S}
\crefname{subsection}{\S}{\S\S}
\crefname{subsubsection}{\S}{\S\S}
\crefname{figure}{Fig.}{Figs.}
\crefname{prop}{Prop.}{Props.}
\crefname{appendix}{Appx.}{Appxs.}
\crefname{theorem}{Thm.}{Thms.}
\crefname{equation}{Eq.}{Eqs.}
\crefname{figure}{Fig.}{Figs.}
\crefname{definition}{Defn.}{Defns.}
\crefname{corollary}{Corollary}{Corollaries}
\crefname{proposition}{Prop.}{Props.}
\crefname{theorem}{Thm.}{Thms.}
\crefname{remark}{Remark}{Remarks}
\crefname{principle}{Principle}{Principles}
\crefname{lemma}{Lemma}{Lemmas}
\crefname{claim}{Claim}{Claims}
\crefname{table}{Table}{Tabs.}
\crefname{assumption}{Assumption}{Assumptions}
\crefname{appendix}{Appendix}{Appendices}
\crefname{example}{Ex.}{Exs.}
```

# Figure placement
A single figure will waste a lot of placed if put into e.g. a `figure` environment. A possible solution is to use the `wrapfig` package, which lets LaTeX to arrange text _around_ the figure.

```latex
\usepackage{wrapfig}

\begin{wrapfigure}{r}{6.5cm}
\centering
    \includegraphics[height=7em,width=\textwidth
		]{figures/fig.png}
    \caption{Caption}
    \label{figure:fig}
\end{wrapfigure} 

```

# Notation, glossary
It's good practice to organize notation and abbreviation into a system. So if you need to change how you denote the input, you only need to do it at a central place.


## Notation
I have a separate `.tex` file for all my abbreviations including concepts such as KL Divergence or the ELBO. All these can be defined with the `\newacronym{}{}{}` command, where the three arguments are:
1. The name you refer to the abbreviation,
2. Abbreviation short form,
3. The abbreviation written out.

```latex
\newacronym{kld}{KL}{Kullback-Leibler Divergence}
\newacronym{elbo}{{\text{\upshape ELBO}}}{evidence lower bound}
\newacronym{pca}{PCA}{Principal Component Analysis}
```

From this point on, `\gls{pca}` will print out Principal Component Analysis(PCA) for the first use, then only PCA. 
- If you need the plural, use `\glspl{pca}`,
- For forcing the short version `\acrshort{pca}`,
- For forcing the long version `\acrlong{pca}`,
- For forcing the full (i.e., both the name spelled out and the abbreviation) version `\acrfull{pca}`.

Besides enforcing consistency, a list of acronyms can be created with the `\printacronyms` command---as a bonus, the acronyms will be cross-referenced, sop clicking on them will lead you to the list of acronyms. Handy, isn't it?

## Glossary
Notation is a crucial tool to refer to concepts in a short form and to formalize ideas. consistency is key here too. Fortunately, the `glossaries` package does this for us: we can organize notation into categories, then print them out such that the reader will be able to click on them and get reminded what we use the formula for.

This is what you need to include:
```latex
\usepackage[acronym, automake, toc, nomain, nopostdot, style=tree, nonumberlist]{glossaries}
\usepackage{glossary-mcols} % to have multiple columns
\setglossarystyle{mcolindex}


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Glossary
\newglossary{abbrev}{abs}{abo}{Nomeclature} %abs and abo are file extensions LaTeX will use internally for this set of formulas -- different glossaries should have different ones
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Top-level glossary entries
\newglossaryentry{obs}{
    name        = \ensuremath{\boldsymbol{x}} ,
    description = {observation vector} ,
    type        = abbrev,
}

\newglossaryentry{latent}{
    name        = \ensuremath{\boldsymbol{z}} ,
    description = {latent vector} ,
    type        = abbrev,
}


% A separate category for VAEs, this will render all related notation 
% under a VAE header
\newglossaryentry{vaes}{type=abbrev,name=\acrlong{vae},description={\nopostdesc}}


\newglossaryentry{q}{
    name        = \ensuremath{q(\gls{latent}|\gls{obs})} ,
    description = {variational posterior of the VAE, mapping $\gls{obs}\mapsto\gls{latent}$ parametrized by ${\phi}$} ,
    type        = abbrev,
    parent      = vaes,
}
```

For referencing the the above entries, the same `\gls{}` command is used as for acronyms. The list of notation can be included by invoking the `\printglossary[type=abbrev, style=tree]` command (this will use a hierarchical style).

The resulting structure will be:
```
Nomenclature
  - x observations
  - z latents
  VAEs
    - q variational posterior
````

### Fixing `hyperref` warnings
When using `\gls{}, \glspl{}, \acrshort{}, \acrlong{}, \acrfull{}` in a caption, `hyperref` will warn about `Token not allowed in a PDF string`. To fix this, we can redefine these commands as 
```latex
\pdfstringdefDisableCommands{%
  \def\gls#1{<#1>}%
  \def\glspl#1{<#1>}%
  \def\acrshort#1{<#1>}%
  \def\acrlong#1{<#1>}%
  \def\acrfull#1{<#1>}%
}
```
to get rid of the warning and have more meaningful bookmarks in the pdf.

# Acknowledgements
I learned lot of the tricks in this post from [Luigi Gresele](https://twitter.com/luigigres) and [Julius von Kügelgen](https://twitter.com/JKugelgen).
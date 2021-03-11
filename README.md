qed
===

[![very-preliminary](https://img.shields.io/badge/very-preliminary-yellow)]() [![super-hacky](https://img.shields.io/badge/super-hacky-orange)]() [![you've-been-warned](https://img.shields.io/badge/you've-been%20warned-red)]() [![tests](https://github.com/rodluger/qed/actions/workflows/tests.yml/badge.svg)](https://github.com/rodluger/qed/actions/workflows/tests.yml)

## Setup

To install, clone this package and run

```bash
python -m pip install .
```

In the directory containing your TeX document, run

```bash
qed-setup
```

This will add the package file ``qed.sty`` to the current directory.

## Usage

Here's a sample LaTeX document, which we'll call ``ms.tex``:

```latex
\documentclass{article}
\usepackage{qed}

\begin{document}

A true statement:

\begin{qed}
    \sin^2 x + \cos^2 x = 1
\end{qed}

A false statement:

\begin{qed}
    \sin\left(\frac{\pi}{2}\right) = 0
\end{qed}

An indeterminate statement:

\begin{qed}
    x = 2 y
\end{qed}

\end{document}
```

Assuming you're using `pdfTeX`, build the PDF by running

```bash
pdflatex ms.tex
qed
pdflatex ms.tex
```

This will generate ``ms.pdf``:

![example](.github/example.png)

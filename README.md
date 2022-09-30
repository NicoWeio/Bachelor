# TUDoThesis [![Build Thesis](https://github.com/maxnoe/tudothesis/actions/workflows/build.yml/badge.svg)](https://github.com/maxnoe/tudothesis/actions/workflows/build.yml)

LaTeX class file and template for a thesis written at TU Dortmund

The template is build for use with _lualatex_ and _biblatex_ with _biber_,
the class file can be used with the LaTeX engine of your choice, it is completely independent.

This is an unofficial document which was created from my bachelor thesis, which itself
was strongly influenced by the latex files which [@kdungs](https://github.com/kdungs) used for his bachelor's thesis.

All used packages and commands are explained
in depth in the materials of the PeP et al. LaTeX Workshop:

http://toolbox.pep-dortmund.de/notes.html


# Compiliation

compile with
```
$ latexmk
```

or
```
$ make
```

For more information, have a look into [example.pdf](https://github.com/maxnoe/TuDoThesis/blob/master/example.pdf)

# Style
- [APA Title Case Capitalization](https://apastyle.apa.org/style-grammar-guidelines/capitalization/title-case)
- Acronyms are written using the corresponding LaTeX command `\ac{}`.
  - This will be expanded to the full name in the first occurrence of the acronym in the text:
    > Conditional Ordinal Regression for Neural Networks (CORN)
- Figures **and tables** have their caption below
  - Though I've always heard „Abbildungen haben eine Unterschrift, Tabellen eine Überschrift.“

## Consistency
- re-weighting, not reweighting
- step size, not stepsize
- Wasserstein, not Vaseršteĭn
- box plot, not boxplot
- ordinality → ?
- TODO: data set, not dataset
- `\num{3}` vs. `three` for small numbers


# Future work
- add test metrics directly to PyTorch
  - for Wasserstein distance, see [here](https://github.com/t-vi/pytorch-tvmisc/blob/master/wasserstein-distance/Pytorch_Wasserstein.ipynb)

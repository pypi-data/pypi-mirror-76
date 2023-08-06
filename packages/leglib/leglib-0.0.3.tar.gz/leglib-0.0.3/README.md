# LegLib

Leglib is just a bunch of utility modules that I wrote and like to use. One very handy one is a rounding function that rounds to significant digits: `leglib.fmt.sigdig`.

## Installation

```zsh
$ pipenv install leglib
```

## Using

```python
>>> from leglib.fmt import sigdig
>>> sigdig(3.843718473821748732184732)
'3.84'
>>> sigdig(3.843718473821748732184732, 5)
'3.84372'
```

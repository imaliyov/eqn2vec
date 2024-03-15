# eqn2vec
Convert latex equations into SVG or PDF files.

# Installation

1. Clone the repository

2. cd eqn2vec
```
pip install .
```

# Usage

* as a library, e.g., when the library is installed, in a separate Python file:
```python
from eqn2vec import eqn2vec
eq_list = [ r'E = mc^2', r'g(x)=\frac{\partial f(x)}{\partial x}']
eqn2vec.eqn2vec(eq_list, format='pdf')
```

* as a command-line tool, in a terminal:
```bash
<path-to-repo>eqn2vec/eqn2vec/eqn2vec.py> --help
<path-to-repo>eqn2vec/eqn2vec/eqn2vec.py> --eq 'E = mc^2' 'S = \sum_{i=1}^n x_i'
```


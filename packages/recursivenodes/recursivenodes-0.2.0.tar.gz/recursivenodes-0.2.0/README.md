# `recursivenodes`: Recursive, parameter-free, explicitly defined interpolation nodes for simplices

This package includes one module level function, `recursive_nodes()`, which returns
nodes for polynomial interpolation on the simplex in arbitrary dimensions.

The nodes have a few nice properties: they are explicitly constructed and fully
symmetric, and their traces on edges are Lobatto-Gauss-Legendre nodes (or any
other node set you wish to use).  Among explicitly constructed nodes, they
appear to have the best interpolation properties.  You can find more details in
the [documentation](https://tisaac.gitlab.io/recursivenodes), and even more in the
[preprint](https://arxiv.org/abs/2002.09421).

```bibtex
@misc{isaac2020recursive,
    title={Recursive, parameter-free, explicitly defined interpolation nodes for simplices},
    author={Tobin Isaac},
    year={2020},
    eprint={2002.09421},
    archivePrefix={arXiv},
    primaryClass={math.NA}
}
```

## Requirements:

- Only `numpy` is needed for `recursive_nodes()`.
- The `lebesgue` submodules requires `scipy`.
- Testing requires `coverage`, `pytest` and `matplotlib`.
- Building documentation additionally requires `sphinx`, `sphinxcontrib-bibtex`, and `sphinxcontrib-tikz`.

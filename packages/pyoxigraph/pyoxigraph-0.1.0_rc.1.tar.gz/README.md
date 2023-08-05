Oxigraph for Python (`pyoxigraph`)
==================================

[![actions status](https://github.com/oxigraph/oxigraph/workflows/build/badge.svg)](https://github.com/oxigraph/oxigraph/actions)
[![Gitter](https://badges.gitter.im/oxigraph/community.svg)](https://gitter.im/oxigraph/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)

This Python package provides a Python API on top of Oxigraph named `pyoxigraph`.

It is distributed on Pypi using the `pyoxigraph` package.

Oxigraph is a graph database implementing the [SPARQL](https://www.w3.org/TR/sparql11-overview/) standard.

It offers two stores with [SPARQL 1.1 Query](https://www.w3.org/TR/sparql11-query/) capabilities.
One of the store is in-memory, and the other one is disk based.

It also provides a set of utility functions for reading, writing and processing RDF files.

The stores are also able to load and dump RDF data serialized in
[Turtle](https://www.w3.org/TR/turtle/), 
[TriG](https://www.w3.org/TR/trig/), 
[N-Triples](https://www.w3.org/TR/n-triples/),
[N-Quads](https://www.w3.org/TR/n-quads/) and
[RDF/XML](https://www.w3.org/TR/rdf-syntax-grammar/).

## Build the development version

To build and install the lastest version of pyoxigraph you need to clone this git repository
and to run `pip install .` in the `python` directory (the one this README is in).


## How to contribute

The Oxigraph bindings are written in Rust using [PyO3](https://github.com/PyO3/pyo3).

They are build using [Maturin](https://github.com/PyO3/maturin).
Maturin could be installed using the usual `pip install maturin`.
To install development version of Oxigraph just run `maturin develop`.

The Python bindings tests are written in Python.
To run them use the usual `python -m unittest` in the `tests` directory.

To release a new version of `pyoxigraph` run:
```bash
docker run --rm -v $(pwd):/io konstin2/maturin publish
```

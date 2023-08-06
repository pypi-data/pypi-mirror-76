# seeder

`seeder` is a library intended to make working with [CDRs](https://github.com/WorldModelers/Document-Schema)
and CDR-based analytics simpler.

## Install as a library

`seeder` is available on [PyPI](https://pypi.org/project/ceeder/).

## Build

[poetry](https://python-poetry.org/) is required to use the project.

Clone the project, then run:

```shell
poetry build
```

## Testing

[tox](https://tox.readthedocs.io/en/latest/index.html) is used for testing the
project.

``` shell
python -m pip install --upgrade tox
tox
```

## Usage

See [the examples](./examples) directory for usage information
in your analytic.

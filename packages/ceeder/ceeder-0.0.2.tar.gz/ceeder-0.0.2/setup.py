# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['seeder', 'seeder.schemas']

package_data = \
{'': ['*']}

install_requires = \
['falcon>=2.0.0,<3.0.0', 'jsonschema>=3.2.0,<4.0.0']

setup_kwargs = {
    'name': 'ceeder',
    'version': '0.0.2',
    'description': 'Library for working with CDR files and analytics.',
    'long_description': '# seeder\n\n`seeder` is a library intended to make working with [CDRs](https://github.com/WorldModelers/Document-Schema)\nand CDR-based analytics simpler.\n\n## Install as a library\n\n`seeder` is available on [PyPI](https://pypi.org/project/ceeder/).\n\n## Build\n\n[poetry](https://python-poetry.org/) is required to use the project.\n\nClone the project, then run:\n\n```shell\npoetry build\n```\n\n## Testing\n\n[tox](https://tox.readthedocs.io/en/latest/index.html) is used for testing the\nproject.\n\n``` shell\npython -m pip install --upgrade tox\ntox\n```\n\n## Usage\n\nSee [the examples](./examples) directory for usage information\nin your analytic.\n',
    'author': 'max thomas',
    'author_email': 'max@qntfy.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/qntfy/ceeder',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
}


setup(**setup_kwargs)

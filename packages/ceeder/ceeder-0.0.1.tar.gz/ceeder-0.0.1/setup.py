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
    'version': '0.0.1',
    'description': 'Library for working with CDR files and analytics.',
    'long_description': '# seeder\n\n`seeder` is a library intended to make working with [CDRs](https://github.com/WorldModelers/Document-Schema)\nand CDR-based analytics simpler.\n\n## Install as a library\n\nClone the project, then run:\n\n```shell\npython setup.py install\n```\n\n## Usage\n\nSee [the examples](./examples) directory for usage information\nin your analytic.\n',
    'author': 'max thomas',
    'author_email': 'max@qntfy.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/qntft/ceeder',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
}


setup(**setup_kwargs)

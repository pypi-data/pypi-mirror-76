# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['occuspytial',
 'occuspytial.gibbs',
 'occuspytial.gibbs.tests',
 'occuspytial.tests']

package_data = \
{'': ['*']}

install_requires = \
['arviz>=0.9.0,<0.10.0',
 'joblib>=0.14.0,<0.15.0',
 'libpysal',
 'numpy>=1.19.0,<2.0.0',
 'pypolyagamma>=1.2.3,<2.0.0',
 'scipy>=1.5.1,<2.0.0',
 'tqdm>=4.46.1,<5.0.0']

extras_require = \
{'docs': ['sphinx>=3,<4',
          'nbsphinx',
          'sphinx_rtd_theme',
          'numpydoc',
          'jupyter']}

setup_kwargs = {
    'name': 'occuspytial',
    'version': '0.1.0a0',
    'description': "'A package for bayesian analysis of spatial occupancy models'",
    'long_description': "# OccuSpytial\n\nA package for fast bayesian analysis of spatial occupancy models. OccuSpytial implements\nseveral samplers for the single season site spatial occupancy model using the Intrinsic Conditional Autoregressive (ICAR) model for spatial random effects.\n\n## Usage\n\nFor usage examples refer to the project's [documentation](https://occuspytial.readthedocs.io).\n\n\n## Installation\n\nThe package can be installed using [pip](https://pip.pypa.io).\n\n```shell\npip install occuspytial\n\n```\n\nAlternatively, it can be installed from source using [poetry](https://python-poetry.org)\n\n```shell\ngit clone https://github.com/zoj613/OccuSpytial.git\ncd OccuSpytial/\npoetry install\n\n```\nNote that installing this way requires that `Cython` is installed for a successful build.\n\n\n## Testing\n\nTo run tests after installation, the package `pytest` is required. Simply run\nthe following line from the terminal in this package's root directory.\n\n```shell\npython -m pytest\n```\n\nIf all tests pass, then you're good to go.\n\n\n## Licensing\n\nOccuSpytial is free software made available under the BSD License. For details\nsee the [LICENSE](https://github.com/zoj613/OccuSpytial/blob/master/LICENSE) file.",
    'author': 'Zolisa Bleki',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/zoj613/OccuSpytial/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['neato_coding_challenge_tcp_client']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0']

entry_points = \
{'console_scripts': ['neato-coding-challenge-tcp-client = '
                     'neato_coding_challenge_tcp_client.__main__:main']}

setup_kwargs = {
    'name': 'neato-coding-challenge-tcp-client',
    'version': '0.0.1',
    'description': 'Neato Coding Challenge - TCP Client',
    'long_description': "Neato Coding Challenge - TCP Client\n===================================\n\n|PyPI| |Python Version| |License|\n\n|Read the Docs| |Tests| |Codecov|\n\n|pre-commit| |Black|\n\n.. |PyPI| image:: https://img.shields.io/pypi/v/neato-coding-challenge-tcp-client.svg\n   :target: https://pypi.org/project/neato-coding-challenge-tcp-client/\n   :alt: PyPI\n.. |Python Version| image:: https://img.shields.io/pypi/pyversions/neato-coding-challenge-tcp-client\n   :target: https://pypi.org/project/neato-coding-challenge-tcp-client\n   :alt: Python Version\n.. |License| image:: https://img.shields.io/pypi/l/neato-coding-challenge-tcp-client\n   :target: https://opensource.org/licenses/MIT\n   :alt: License\n.. |Read the Docs| image:: https://img.shields.io/readthedocs/neato-coding-challenge-tcp-client/latest.svg?label=Read%20the%20Docs\n   :target: https://neato-coding-challenge-tcp-client.readthedocs.io/\n   :alt: Read the documentation at https://neato-coding-challenge-tcp-client.readthedocs.io/\n.. |Tests| image:: https://github.com/neato-coding-challenge/tcp-client/workflows/Tests/badge.svg\n   :target: https://github.com/neato-coding-challenge/tcp-client/actions?workflow=Tests\n   :alt: Tests\n.. |Codecov| image:: https://codecov.io/gh/neato-coding-challenge/tcp-client/branch/master/graph/badge.svg\n   :target: https://codecov.io/gh/neato-coding-challenge/tcp-client\n   :alt: Codecov\n.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white\n   :target: https://github.com/pre-commit/pre-commit\n   :alt: pre-commit\n.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n   :target: https://github.com/psf/black\n   :alt: Black\n\n\nFeatures\n--------\n\n* TODO\n\n\nRequirements\n------------\n\n* TODO\n\n\nInstallation\n------------\n\nYou can install *Neato Coding Challenge - TCP Client* via pip_ from PyPI_:\n\n.. code:: console\n\n   $ pip install neato-coding-challenge-tcp-client\n\n\nUsage\n-----\n\n* TODO\n\n\nContributing\n------------\n\nContributions are very welcome.\nTo learn more, see the `Contributor Guide`_.\n\n\nLicense\n-------\n\nDistributed under the terms of the MIT_ license,\n*Neato Coding Challenge - TCP Client* is free and open source software.\n\n\nIssues\n------\n\nIf you encounter any problems,\nplease `file an issue`_ along with a detailed description.\n\n\nCredits\n-------\n\nThis project was generated from `@cjolowicz`_'s `Hypermodern Python Cookiecutter`_ template.\n\n\n.. _@cjolowicz: https://github.com/cjolowicz\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _MIT: http://opensource.org/licenses/MIT\n.. _PyPI: https://pypi.org/\n.. _Hypermodern Python Cookiecutter: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n.. _file an issue: https://github.com/neato-coding-challenge/tcp-client/issues\n.. _pip: https://pip.pypa.io/\n.. github-only\n.. _Contributor Guide: CONTRIBUTING.rst\n",
    'author': 'Michele Cardone',
    'author_email': 'michele.cardone82@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/neato-coding-challenge/tcp-client',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)

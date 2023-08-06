# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['jmopenorders', 'jmopenorders.api', 'jmopenorders.core']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'openpyxl>=3.0.4,<4.0.0']

entry_points = \
{'console_scripts': ['jmopenorders = jmopenorders.__main__:main']}

setup_kwargs = {
    'name': 'jmopenorders',
    'version': '0.2.4',
    'description': 'a generator to generate infos for the affected persons',
    'long_description': "jmopenorders\n============\n\n.. image:: https://api.codacy.com/project/badge/Grade/6af827d12e264ff3bafee6b879dab554\n   :alt: Codacy Badge\n   :target: https://app.codacy.com/manual/jmuelbert/jmopenorders?utm_source=github.com&utm_medium=referral&utm_content=jmuelbert/jmopenorders&utm_campaign=Badge_Grade_Dashboard\n\n|Gitpod| |Tests| |LGTM|\xa0|Codecov| |PyPI| |Python Version| |Read the Docs| |License| |Black| |pre-commit| |Dependabot|\n\n\nFeatures\n--------\n\njmopenorders is a generator to generate infos for the affected persons.\n\nGenerate from a excel-output for each service person a seperated excel file. You must the excel-file save as csv-file.\n\njmopenorders is written in [Python](https://www.python.org).\npython does run on almosts known platforms.\n\nRequirements\n------------\n\n* TODO\n\n\nInstallation\n------------\n\nYou can install *jmopenorders* via pip_ from PyPI_:\n\n.. code:: console\n\n   $ pip install jmopenorders\n\n\nThe master branch represents the latest pre-release code.\n\n-   [Releases](https://github.com/jmuelbert/jmopenorders/releases).\n\n-   [Milestones](https://github.com/jmuelbert/jmopenorders/milestones).\n\nUsage\n-----\n\n* TODO\n\n\nContributing\n------------\n\nContributions are very welcome.\nTo learn more, see the `Contributor Guide`_.\n\n\nLicense\n-------\n\nDistributed under the terms of the EUPL-1.2_ license,\n*jmopenorders* is free and open source software.\n\n\nIssues\n------\n\nIf you encounter any problems,\nplease `file an issue`_ along with a detailed description.\n\n\nCredits\n-------\n\nThis project was generated from `@cjolowicz`_'s `Hypermodern Python Cookiecutter`_ template.\n\n\n.. _@cjolowicz: https://github.com/cjolowicz\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _EUPL-1.2: http://opensource.org/licenses/EUPL-1.2\n.. _PyPI: https://pypi.org/\n.. _Hypermodern Python Cookiecutter: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n.. _file an issue: https://github.com/jmuelbert/jmopenorders/issues\n.. _pip: https://pip.pypa.io/\n.. github-only\n.. _Contributor Guide: CONTRIBUTING.rst\n\n.. |Gitpod| image:: https://img.shields.io/badge/Gitpod-Ready--to--Code-blue?logo=gitpod\n    :target: https://gitpod.io/#https://github.com/jmuelbert/jmopenorders\n    :alt: Gitpod-Ready-Code\n.. |Tests| image:: https://github.com/jmuelbert/jmopenorders/workflows/Tests/badge.svg\n   :target: https://github.com/jmuelbert/jmopenorders/actions?workflow=Tests\n   :alt: Tests\n.. |LGTM| image:: https://img.shields.io/lgtm/alerts/g/jmuelbert/jmopenorders.svg?logo=lgtm&logoWidth=18\n    :target: https://lgtm.com/projects/g/jmuelbert/jmopenorders/alerts/\n    :alt: LGTM\n.. |Codecov| image:: https://codecov.io/gh/jmuelbert/jmopenorders/branch/master/graph/badge.svg\n   :target: https://codecov.io/gh/jmuelbert/jmopenorders\n   :alt: Codecov\n.. |PyPI| image:: https://img.shields.io/pypi/v/jmopenorders.svg\n   :target: https://pypi.org/project/jmopenorders/\n   :alt: PyPI\n.. |Python Version| image:: https://img.shields.io/pypi/pyversions/jmopenorders\n   :target: https://pypi.org/project/jmopenorders\n   :alt: Python Version\n.. |Read the Docs| image:: https://readthedocs.org/projects/jmopenorders/badge/\n   :target: https://jmopenorders.readthedocs.io/\n   :alt: Read the Docs\n.. |License| image:: https://img.shields.io/pypi/l/jmopenorders\n   :target: LICENSE.rst\n   :alt: Project License\n.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n   :target: https://github.com/psf/black\n   :alt: Black\n.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white\n   :target: https://github.com/pre-commit/pre-commit\n   :alt: pre-commit\n.. |Dependabot| image:: https://api.dependabot.com/badges/status?host=github&repo=jmuelbert/jmopenorders\n   :target: https://dependabot.com\n   :alt: Dependabot\n",
    'author': 'Jürgen Mülbert',
    'author_email': 'juergen.muelbert@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jmuelbert/jmopenorders',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)

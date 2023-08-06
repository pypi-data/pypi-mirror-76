# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['libvcs']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'libvcs',
    'version': '0.5.0',
    'description': 'vcs abstraction layer',
    'long_description': '``libvcs`` - abstraction layer for vcs, powers `vcspull`_.\n\n|pypi| |docs| |build-status| |coverage| |license|\n\nSetup\n-----\n\n.. code-block:: sh\n\n   $ pip install libvcs\n\nOpen up python:\n\n.. code-block:: sh\n\n   $ python\n\n   # or for nice autocomplete and syntax highlighting\n   $ pip install ptpython\n   $ ptpython\n\nUsage\n-----\nCreate a `Repo`_ object of the project to inspect / checkout / update:\n\n.. code-block:: python\n\n   >>> from libvcs.shortcuts import create_repo_from_pip_url, create_repo\n\n   # repo is an object representation of a vcs repository.\n   >>> r = create_repo(url=\'https://www.github.com/vcs-python/libtmux\',\n   ...                 vcs=\'git\',\n   ...                 repo_dir=\'/tmp/libtmux\')\n\n   # or via pip-style URL\n   >>> r = create_repo_from_pip_url(\n   ...         pip_url=\'git+https://www.github.com/vcs-python/libtmux\',\n   ...         repo_dir=\'/tmp/libtmux\')\n\nUpdate / clone repo:\n\n.. code-block:: python\n\n   # it may or may not be checked out/cloned on the system yet\n   >>> r.update_repo()\n\nGet revision:\n\n.. code-block:: python\n\n   >>> r.get_revision()\n   u\'5c227e6ab4aab44bf097da2e088b0ff947370ab8\'\n\nDonations\n---------\nYour donations fund development of new features, testing and support.\nYour money will go directly to maintenance and development of the project.\nIf you are an individual, feel free to give whatever feels right for the\nvalue you get out of the project.\n\nSee donation options at https://www.git-pull.com/support.html.\n\nMore information \n----------------\n- Python support: Python 2.7, >= 3.4, pypy\n- VCS supported: git(1), svn(1), hg(1)\n- Source: https://github.com/vcs-python/libvcs\n- Docs: https://libvcs.git-pull.com\n- Changelog: https://libvcs.git-pull.com/history.html\n- API: https://libvcs.git-pull.com/api.html\n- Issues: https://github.com/vcs-python/libvcs/issues\n- Test Coverage: https://codecov.io/gh/vcs-python/libvcs\n- pypi: https://pypi.python.org/pypi/libvcs\n- Open Hub: https://www.openhub.net/p/libvcs\n- License: `MIT`_.\n\n.. _MIT: https://opensource.org/licenses/MIT\n.. _Documentation: https://libvcs.git-pull.com/\n.. _API: https://libvcs.git-pull.com/api.html\n.. _pip: http://www.pip-installer.org/en/latest/\n.. _vcspull: https://www.github.com/vcs-python/vcspull/\n.. _Repo: https://libvcs.git-pull.com/api.html#creating-a-repo-object\n\n.. |pypi| image:: https://img.shields.io/pypi/v/libvcs.svg\n    :alt: Python Package\n    :target: http://badge.fury.io/py/libvcs\n\n.. |docs| image:: https://github.com/vcs-python/libvcs/workflows/Publish%20Docs/badge.svg\n   :alt: Docs\n   :target: https://github.com/vcs-python/libvcs/actions?query=workflow%3A"Publish+Docs"\n\n.. |build-status| image:: https://github.com/vcs-python/libvcs/workflows/tests/badge.svg\n   :alt: Build Status\n   :target: https://github.com/vcs-python/libvcs/actions?query=workflow%3A"tests"\n\n.. |coverage| image:: https://codecov.io/gh/vcs-python/libvcs/branch/master/graph/badge.svg\n    :alt: Code Coverage\n    :target: https://codecov.io/gh/vcs-python/libvcs\n    \n.. |license| image:: https://img.shields.io/github/license/vcs-python/libvcs.svg\n    :alt: License \n',
    'author': 'Tony Narlock',
    'author_email': 'tony@git-pull.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'http://github.com/vcs-python/libvcs/',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
}


setup(**setup_kwargs)

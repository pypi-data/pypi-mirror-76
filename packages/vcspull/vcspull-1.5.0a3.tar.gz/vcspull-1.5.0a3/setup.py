# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vcspull']

package_data = \
{'': ['*']}

install_requires = \
['click>=7', 'colorama>=0.3.9', 'kaptan', 'libvcs==0.5.0a1']

entry_points = \
{'console_scripts': ['vcspull = vcspull:cli.cli']}

setup_kwargs = {
    'name': 'vcspull',
    'version': '1.5.0a3',
    'description': 'synchronize your projects via yaml / json files',
    'long_description': '``vcspull`` - synchronize your repos. built on `libvcs`_\n\n|pypi| |docs| |build-status| |coverage| |license|\n\nManage your commonly used repos from YAML / JSON manifest(s).\nCompare to `myrepos`_.\n\nGreat if you use the same repos at the same locations across multiple\nmachines or want to clone / update a pattern of repos without having\nto ``cd`` into each one.\n\n* clone  /update to the latest repos with ``$ vcspull``\n* use filters to specify a location, repo url or pattern\n  in the manifest to clone / update\n* supports svn, git, hg version control systems\n* automatically checkout fresh repositories\n* `Documentation`_  and `Examples`_.\n* supports `pip`_-style URL\'s (`RFC3986`_-based `url scheme`_)\n\n.. _myrepos: http://myrepos.branchable.com/\n\nhow to\n------\n\ninstall\n"""""""\n\n.. code-block:: sh\n\n    $ pip install --user vcspull\n\nconfigure\n"""""""""\n\nadd repos you want vcspull to manage to ``~/.vcspull.yaml``.\n\n*vcspull does not currently scan for repos on your system, but it may in\nthe future*\n\n.. code-block:: yaml\n   \n    ~/code/:\n      flask: "git+https://github.com/mitsuhiko/flask.git"\n    ~/study/c:\n      awesome: \'git+git://git.naquadah.org/awesome.git\'\n    ~/study/data-structures-algorithms/c:\n      libds: \'git+https://github.com/zhemao/libds.git\'\n      algoxy: \n        repo: \'git+https://github.com/liuxinyu95/AlgoXY.git\'\n        remotes:\n          tony: \'git+ssh://git@github.com/tony/AlgoXY.git\'\n\n(see the author\'s `.vcspull.yaml`_, more `examples`_.)\n\nnext, on other machines, copy your ``$HOME/.vcspull.yaml`` file\nor ``$HOME/.vcspull/`` directory them and you can clone your repos\nconsistently. vcspull automatically handles building nested\ndirectories. Updating already cloned/checked out repos is done\nautomatically if they already exist.\n\nclone / update your repos\n"""""""""""""""""""""""""\n\n.. code-block:: bash\n    \n    $ vcspull\n\nkeep nested VCS repositories updated too, lets say you have a mercurial or\nsvn project with a git dependency:\n\n``external_deps.yaml`` in your project root, (can be anything):\n\n.. code-block:: yaml\n\n   ./vendor/:\n     sdl2pp: \'git+https://github.com/libSDL2pp/libSDL2pp.git\'\n\nclone / update repos::\n\n    $ vcspull -c external_deps.yaml\n\nSee the `Quickstart`_ for more.\n\npulling specific repos\n""""""""""""""""""""""\n\nhave a lot of repos?\n\nyou can choose to update only select repos through `fnmatch`_ patterns.\nremember to add the repos to your ``~/.vcspull.{json,yaml}`` first.\n\nThe patterns can be filtered by by directory, repo name or vcs url.\n\n.. code-block:: bash\n\n    # any repo starting with "fla"\n    $ vcspull "fla*"\n    # any repo with django in the name\n    $ vcspull "*django*"\n\n    # search by vcs + url\n    # since urls are in this format <vcs>+<protocol>://<url>\n    $ vcspull "git+*"\n\n    # any git repo with python in the vcspull\n    $ vcspull "git+*python*\n\n    # any git repo with django in the vcs url\n    $ vcspull "git+*django*"\n\n    # all repositories in your ~/code directory\n    $ vcspull "$HOME/code/*"\n\n.. image:: https://raw.github.com/vcs-python/vcspull/master/doc/_static/vcspull-demo.gif\n    :scale: 100%\n    :width: 45%\n    :align: center\n\nDonations\n---------\n\nYour donations fund development of new features, testing and support.\nYour money will go directly to maintenance and development of the project.\nIf you are an individual, feel free to give whatever feels right for the\nvalue you get out of the project.\n\nSee donation options at https://git-pull.com/support.html.\n\nMore information \n----------------\n- Python support: Python 2.7, >= 3.4, pypy\n- VCS supported: git(1), svn(1), hg(1)\n- Source: https://github.com/vcs-python/vcspull\n- Docs: https://vcspull.git-pull.com\n- Changelog: https://vcspull.git-pull.com/history.html\n- API: https://vcspull.git-pull.com/api.html\n- Issues: https://github.com/vcs-python/vcspull/issues\n- Test Coverage: https://codecov.io/gh/vcs-python/vcspull\n- pypi: https://pypi.python.org/pypi/vcspull\n- Open Hub: https://www.openhub.net/p/vcspull\n- License: `MIT`_.\n\n.. _MIT: https://opensource.org/licenses/MIT\n.. _Documentation: https://vcspull.git-pull.com/\n.. _Quickstart: https://vcspull.git-pull.com/quickstart.html\n.. _pip: http://www.pip-installer.org/\n.. _url scheme: http://www.pip-installer.org/logic.html#vcs-support\n.. _libvcs: https://github.com/vcs-python/libvcs\n.. _RFC3986: http://tools.ietf.org/html/rfc3986.html\n.. _.vcspull.yaml: https://github.com/tony/.dot-config/blob/master/.vcspull.yaml\n.. _examples: https://vcspull.git-pull.com/examples.html\n.. _fnmatch: http://pubs.opengroup.org/onlinepubs/009695399/functions/fnmatch.html\n\n.. |pypi| image:: https://img.shields.io/pypi/v/vcspull.svg\n    :alt: Python Package\n    :target: http://badge.fury.io/py/vcspull\n\n.. |docs| image:: https://github.com/vcs-python/vcspull/workflows/Publish%20Docs/badge.svg\n   :alt: Docs\n   :target: https://github.com/vcs-python/vcspull/actions?query=workflow%3A"Publish+Docs"\n\n.. |build-status| image:: https://github.com/vcs-python/vcspull/workflows/tests/badge.svg\n   :alt: Build Status\n   :target: https://github.com/vcs-python/vcspull/actions?query=workflow%3A"tests"\n\n.. |coverage| image:: https://codecov.io/gh/vcs-python/vcspull/branch/master/graph/badge.svg\n    :alt: Code Coverage\n    :target: https://codecov.io/gh/vcs-python/vcspull\n    \n.. |license| image:: https://img.shields.io/github/license/vcs-python/vcspull.svg\n    :alt: License \n',
    'author': 'Tony Narlock',
    'author_email': 'tony@git-pull.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://vcspull.git-pull.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
}


setup(**setup_kwargs)

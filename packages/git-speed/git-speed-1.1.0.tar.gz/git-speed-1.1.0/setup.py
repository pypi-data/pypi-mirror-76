# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['git_speed']

package_data = \
{'': ['*']}

install_requires = \
['typer>=0.1.1,<0.2.0']

entry_points = \
{'console_scripts': ['git-speed = git_speed.cli:main']}

setup_kwargs = {
    'name': 'git-speed',
    'version': '1.1.0',
    'description': 'Installs Git aliases.',
    'long_description': '# git-speed\n\nGit aliases to speed you up.\n\nSee https://www.gitscientist.com for more.\n\n## Install\n\nInstall from pip:\n\n```bash\npip install git-speed\n```\n\nThen install your Git aliases.\n`git-speed` will ask if you want to update your bash prompt to include information about your Git\nrepo (the current branch name and whether the repo contains uncommitted changes).\nWe recommend you update your bash prompt.\n\n```bash\ngit-speed install\n```\n\n## Uninstall\n\n```bash\ngit-speed uninstall\n```\n',
    'author': 'Daniel Tipping',
    'author_email': 'daniel@gitscientist.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://www.gitscientist.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['git_networkx']

package_data = \
{'': ['*']}

install_requires = \
['flake8', 'networkx>=2.4,<3.0']

setup_kwargs = {
    'name': 'git-networkx',
    'version': '2.0.0',
    'description': 'Git graph to networkx',
    'long_description': '# Git-NetworkX\n\n### Port of https://github.com/hoduche/git-graph to NetworkX\n___\n\n## Install\n\n### PyPi\n`pip install git-graph`\n### Git\n`pip install git+https://github.com/CircArgs/git-networkx.git`\n\n## Demo\n\n```python\nfrom networkx.drawing.nx_pydot import write_dot\nimport git_networkx.git_networkx as gnx\n#everything\nAll = gnx.GitNX(\'my/repo/path/that/has/a/.git\')\nwrite_dot(All, "myrepo.dot")\n\n#Commits\nCommits = gnx.GitNX(\'my/repo/path/that/has/a/.git\', "c")\nwrite_dot(Commits, "mycommits.dot")\n\n```\n\n## Node Types\n| Node Type      | Letter |  Node Type      | Letter |\n| -------------- | :----: |  -------------- | :----: |\n| blob           | b      |  remote branch  | r      |\n| tree           | t      |  remote head    | d      |\n| commit         | c      |  remote server  | s      |\n| local branch   | l      |  annotated tag  | a      |\n| local head     | h      |  tag            | g      |\n| upstream link  | u      | \n\nBy default all nodes are added to the DiGraph.\n```python\n# you can get your commits, branches and the head of your local repo simply with lch\nG=gnx.GitNX(\'../git_networkx_test/\', "lch")\n\n```\n',
    'author': 'Henri-Olivier Duché',
    'author_email': 'hoduche@yahoo.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/CircArgs/git-graph',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

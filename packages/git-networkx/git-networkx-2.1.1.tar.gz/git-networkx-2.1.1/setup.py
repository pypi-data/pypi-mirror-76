# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['git_networkx']

package_data = \
{'': ['*']}

install_requires = \
['networkx>=2.4,<3.0']

setup_kwargs = {
    'name': 'git-networkx',
    'version': '2.1.1',
    'description': 'Git graph to networkx',
    'long_description': '# Git-NetworkX\n\n### Port of https://github.com/hoduche/git-graph to NetworkX\n\n---\n\n## Install\n\n### PyPi\n\n`pip install git-networkx`\n\n### Git\n\n`pip install git+https://github.com/CircArgs/git-networkx.git`\n\n## Demo\n\n```python\nfrom networkx.drawing.nx_pydot import write_dot\nfrom git_networkx import GitNX, Commit\n#everything\nAll = GitNX(\'my/repo/path/that/has/a/.git\')\nwrite_dot(All, "myrepo.dot")\n\n#Commits\nCommits = GitNX(\'my/repo/path/that/has/a/.git\', "c")\nwrite_dot(Commits, "mycommits.dot")\n\n#which is equivalent to the subgraph obtained by (not in terms of ops)\n[n for n in All if isinstance(n, Commit)]\n\n```\n\n#### Suppose you had a log like the following:\n\n```\ncommit 9a99a4d85cb14005ca829e2cab8f626b4034b981 (HEAD -> master, dev)\nAuthor: CircArgs <quebecname@gmail.com>\nDate:   Fri Aug 14 22:05:30 2020 -0400\n\n    I like dogs\n\ncommit 80798c310455976e08fedd9b367794692ebb54a6\nAuthor: CircArgs <quebecname@gmail.com>\nDate:   Fri Aug 14 22:04:58 2020 -0400\n\n    add file2 with text\n\ncommit 8c7f9cea1f6323d793cd035e2178636d6ebf0a36\nAuthor: CircArgs <quebecname@gmail.com>\nDate:   Fri Aug 14 22:04:28 2020 -0400\n\n    add file 1\n\n```\n\nthen\n\n```python\nG=GitNX(".", "lch")\n\nprint(list(G.neighbors(Commit("80798c310455976e08fedd9b367794692ebb54a6"))))\n# [Commit(\'8c7f9cea1f6323d793cd035e2178636d6ebf0a36\')]\n\nprint(list(G.predecessors(Commit("80798c310455976e08fedd9b367794692ebb54a6"))))\n# [Commit(\'9a99a4d85cb14005ca829e2cab8f626b4034b981\')]\n\nprint(list(G.predecessors(Commit(\'9a99a4d85cb14005ca829e2cab8f626b4034b981\'))))\n# [LocalBranch(\'dev\'), LocalBranch(\'master\')]\n```\n\n## Node Types\n\n| Node Type     | Letter | Node Type     | Letter |\n| ------------- | :----: | ------------- | :----: |\n| blob          |   b    | remote branch |   r    |\n| tree          |   t    | remote head   |   d    |\n| commit        |   c    | remote server |   s    |\n| local branch  |   l    | annotated tag |   a    |\n| local head    |   h    | tag           |   g    |\n| upstream link |   u    |\n\nBy default all nodes are added to the DiGraph.\n\n```python\n# you can get your commits, branches and the head of your local repo simply with lch\nG=GitNX(\'../git_networkx_test/\', "lch")\n\n```\n',
    'author': 'Nick Ouellet',
    'author_email': 'nick@ouellet.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/CircArgs/git-graph',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

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
    'version': '1.2',
    'description': 'Git graph to networkx',
    'long_description': '# Git-graph\n\n### Learn (or teach) Git fast and well - *by visualizing the inner graph of your Git repositories*\n___\n\n![full](doc/sample_full.dot.svg)\n\n> [Git is a fast, scalable, distributed revision control system with an unusually rich command set\nthat provides both high-level operations and full access to internals.](https://git-scm.com/docs/git)\n\nAs wonderful as it may be, there is a downside coming with this "unusually rich command set", a kind of anxiety that affects beginners in particular and can be summed up in one question:\n> "What the hell is going to happen to my repository if I launch this Git command ?"\n\nA good way to overcome this difficulty is to experiment.\nThis is made easy thanks to Git lightness and the fact it is immediately up and running in any directory with `git init`.\n\nGit-graph is a Git plugin, written in Python, that displays your Git repository inner content as a [Directed Acyclic Graph](https://en.wikipedia.org/wiki/Directed_acyclic_graph) (DAG).\nThis structured visual representation of Git internal data demystifies the impact of each Git command and considerably improves the learning curve.\n\n## Install\n\n#### From PyPI\nTo install Git-graph from PyPI:\n1. You first need to install [Graphviz](https://www.graphviz.org/download/) and check that the dot binary is correctly set in you system\'s path.  \n2. Then run: \n    ```\n    pip install git-graph\n    ```\n\n#### From GitHub\nTo install Git-graph from GitHub:\n1. You first need to install [Graphviz](https://www.graphviz.org/download/) and check that the dot binary is correctly set in you system\'s path.  \n2. Then run:\n    ```\n    git clone https://github.com/hoduche/git-graph\n    ```\n3. Finally, inside the newly created git-graph folder, run (with Python 3 and setuptools):\n    ```\n    python setup.py install\n    ```\n\n## Run\n\n#### As a Git plugin\nGit-graph is a Git plugin that is run from a Git repository with the command:\n```\ngit graph\n```\n\nRunning `git graph` from a Git repository will:\n1. scan your `.git` folder\n2. build and save a graph representation of the `.git` folder internals as text (`.dot`) and image (PDF by default) in a `.gitGraph` folder\n3. popup a window that displays the image of your graph\n\nA color code helps in distinguishing in the graph the different kinds of object Git is using in its implementation:\n\n| Object kind    | Letter | Representation                                     | Object kind    | Letter | Representation                                     |\n| -------------- | :----: | -------------------------------------------------- | -------------- | :----: | -------------------------------------------------- |\n| blob           | b      | ![blob](doc/sample_blob.dot.svg)                   | remote branch  | r      | ![remote_branch](doc/sample_remote_branch.dot.svg) |\n| tree           | t      | ![tree](doc/sample_tree.dot.svg)                   | remote head    | d      | ![remote_head](doc/sample_remote_head.dot.svg)     |\n| commit         | c      | ![commit](doc/sample_commit.dot.svg)               | remote server  | s      | ![remote_server](doc/sample_remote_server.dot.svg) |\n| local branch   | l      | ![local_branch](doc/sample_local_branch.dot.svg)   | annotated tag  | a      | ![annotated_tag](doc/sample_annotated_tag.dot.svg) |\n| local head     | h      | ![local_head](doc/sample_local_head.dot.svg)       | tag            | g      | ![tag](doc/sample_tag.dot.svg)                     |\n| upstream link  | u      | ![upstream](doc/sample_upstream.dot.svg)           |\n\nBy default all nodes are displayed in the output graph when running `git graph`.\nIt is possible to only display a user selection of object kinds using the `-n` or `--nodes` option and picking the letters corresponding to your choice.   \nFor instance to only display blobs, trees and commits:\n```\ngit graph -n btc\n```\n\nBy default Git-graph considers it is launched from a Git repository.\nIt is possible to indicate the path to another Git repository with the `-p` or `--path` option:\n```\ngit graph -p examples/demo\n```\n\nThe default output format is PDF.\nOther output graphics formats (either vector or raster) can be set with the `-f` or `--format` option:  \n(the full list of possible formats can be found on the [Graphviz documentation website](https://graphviz.gitlab.io/_pages/doc/info/output.html))\n```\ngit graph -f svg\n```\n\nFinally it is possible to prevent the graph image from poping up once constructed, with the `-c` or `--conceal` option:\n```\ngit graph -c\n```\n\n#### As a Python program\n```\npython git_graph/cli.py -p examples/demo -n btc -f svg\n```\nor\n```\n./git_graph/cli.py -p examples/demo -n btc -f svg\n```\n\n#### As a Python module\n\n```python\nimport git_graph.dot_graph as dg\ndg.DotGraph(\'..\').persist()\ndg.DotGraph(\'../examples/demo\', nodes=\'btc\').persist(form=\'svg\', conceal=True)\n```\n',
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

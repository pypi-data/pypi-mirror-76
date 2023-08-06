# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mercs',
 'mercs.algo',
 'mercs.composition',
 'mercs.core',
 'mercs.graph',
 'mercs.utils',
 'mercs.visuals']

package_data = \
{'': ['*'], 'mercs.utils': ['data/*']}

install_requires = \
['catboost>=0.24,<0.25',
 'dask[delayed]>=2.23.0,<3.0.0',
 'decision-tree-morfist>=0.3.3,<0.4.0',
 'ipython>=7.17.0,<8.0.0',
 'joblib>=0.16.0,<0.17.0',
 'lightgbm>=2.3.1,<3.0.0',
 'networkx>=2.4,<3.0',
 'numpy>=1.19.1,<2.0.0',
 'pydot>=1.4.1,<2.0.0',
 'scikit-learn>=0.23.2,<0.24.0',
 'shap>=0.35.0,<0.36.0']

setup_kwargs = {
    'name': 'mercs-mixed',
    'version': '0.0.45',
    'description': 'MERCS: Multi-Directional Ensembles of Regression and Classification treeS',
    'long_description': '# MERCS\n\nMERCS stands for **multi-directional ensembles of classification and regression trees**. It is a novel ML-paradigm under active development at the [DTAI-lab at KU Leuven](https://dtai.cs.kuleuven.be/).\n\n## Installation\n\nEasy via pip:\n\n```\npip install mercs-mixed\n```\n\n## Website\n\nCf. [https://systemallica.github.io/mercs/](https://systemallica.github.io/mercs/)\n\n## Tutorials\n\nCf. the quickstart section of the website, [https://systemallica.github.io/mercs/quickstart](https://systemallica.github.io/mercs/quickstart).\n\n## Code\n\nMERCS is fully open-source cf. our [github-repository](https://github.com/systemallica/mercs/)\n\n## Publications\n\nMERCS is an active research project, hence we periodically publish our findings;\n\n### MERCS: Multi-Directional Ensembles of Regression and Classification Trees\n\n**Abstract**\n*Learning a function f(X) that predicts Y from X is the archetypal Machine Learning (ML) problem. Typically, both sets of attributes (i.e., X,Y) have to be known before a model can be trained. When this is not the case, or when functions f(X) that predict Y from X are needed for varying X and Y, this may introduce significant overhead (separate learning runs for each function). In this paper, we explore the possibility of omitting the specification of X and Y at training time altogether, by learning a multi-directional, or versatile model, which will allow prediction of any Y from any X. Specifically, we introduce a decision tree-based paradigm that generalizes the well-known Random Forests approach to allow for multi-directionality. The result of these efforts is a novel method called MERCS: Multi-directional Ensembles of Regression and Classification treeS. Experiments show the viability of the approach.*\n\n**Authors**\nElia Van Wolputte, Evgeniya Korneva, Hendrik Blockeel\n\n**Open Access**\nA pdf version can be found at [AAAI-publications](https://www.aaai.org/ocs/index.php/AAAI/AAAI18/paper/viewFile/16875/16735)\n\n## People\n\nPeople involved in this project:\n\n* [Elia Van Wolputte](https://eliavw.github.io/)\n* Evgeniya Korneva\n* [Prof. Hendrik Blockeel](https://people.cs.kuleuven.be/~hendrik.blockeel/)\n* [Andrés Reverón Molina](https://andres.reveronmolina.me)\n',
    'author': 'Andrés Reverón Molina',
    'author_email': 'andres@reveronmolina.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/systemallica/mercs',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.0,<4.0.0',
}


setup(**setup_kwargs)

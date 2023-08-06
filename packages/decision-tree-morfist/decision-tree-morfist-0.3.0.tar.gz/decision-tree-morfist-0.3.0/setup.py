# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['morfist', 'morfist.algo', 'morfist.core']

package_data = \
{'': ['*']}

install_requires = \
['numba>=0.50.1,<0.51.0', 'numpy>=1.19.1,<2.0.0', 'scipy>=1.5.2,<2.0.0']

setup_kwargs = {
    'name': 'decision-tree-morfist',
    'version': '0.3.0',
    'description': 'Multi-target Random Forest implementation that can mix both classification and regression tasks.',
    'long_description': "# morfist: mixed-output-rf\nMulti-target Random Forest implementation that can mix both classification and regression tasks.\n\nMorfist implements the Random Forest algorithm (Breiman, 2001)\nwith support for mixed-task multi-task learning, i.e., it is possible to train the model on any number\nof classification tasks and regression tasks, simultaneously. Morfist's mixed multi-task learning implementation follows that proposed by Linusson (2013). \n\n* [Breiman, L. (2001). Random forests. Machine learning, 45(1), 5-32](https://link.springer.com/article/10.1023%2FA%3A1010933404324).\n* [Linusson, H. (2013). Multi-output random forests](https://pdfs.semanticscholar.org/4219/f87ed41c558d43cf78f63976cf87bcd7ebb0.pdf).\n\n## Installation\n\nWith pip:\n```\npip install decision-tree-morfist\n```\nWith conda:\n```\nconda install -c systemallica decision-tree-morfist\n```\n## Usage\n\n### Initialising the model\n\n- Similarly to a scikit-learn [RandomForestClassifier](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html), a MixedRandomForest can be initialised in this way:\n```\nfrom morfist import MixedRandomForest\n\nmrf = MixedRandomForest(\n    n_estimators=n_trees,\n    min_samples_leaf=1,\n    classification_targets=[0]\n)\n```\n- The available parameters are:\n    - **n_estimators(int)**: the number of trees in the forest. Optional. Default value: 10.\n    \n    - **max_features(int | float | str)**: the number of features to consider when looking for the best split. Optional. Default value: 'sqrt'.\n        - If int, then consider max_features features at each split.\n        - If float, then max_features is a fraction and int(max_features * n_features) features are considered at each split.\n        - If “sqrt”, then max_features=sqrt(n_features) (same as “auto”).\n        - If “log2”, then max_features=log2(n_features).\n        - If None, then max_features=n_features.\n    \n        Note: the search for a split does not stop until at least one valid partition of the node samples is found, even if it requires to effectively inspect more than max_features features.\n    \n    - **min_samples_leaf(int)**: the minimum number of samples required to be at a leaf node. Optional. Default value: 5.\n    \n        Note: A split point at any depth will only be considered if it leaves at least min_samples_leaf training samples in each of the left and right branches. This may have the effect of smoothing the model, especially in regression.\n        \n    - **choose_split(str)**: method used to find the best split. Optional. Default value: 'mean'.\n    \n        By default, the mean information gain will be used.\n        \n        - Possible values:\n            - 'mean': the mean information gain is used.\n            - 'max': the maximum information gain is used.\n        \n    - **classification_targets(int[])**: features that are part of the classification task. Optional. Default value: None.\n    \n        If no classification_targets are specified, the random forest will treat all variables as regression variables.\n\n### Training the model\n\n- Once the model is initialised, it can be fitted like this:\n    ```\n    mrf.fit(X, y)\n    ```\n    Where X are the training examples and Y are their respective labels(if they are categorical) or values(if they are numerical)\n\n### Prediction\n\n- The model can be now used to predict new instances.\n    - Class/value:\n    ```\n    mrf.predict(x)\n    ```\n    - Probability:\n    ```\n    mrf.predict_proba(x)\n    ```\n  \n## TODO:\n* Speed up the learning algorithm implementation (morfist is currently **much** slower than the Random Forest implementation available in scikit-learn) \n",
    'author': 'Andrés Reverón Molina',
    'author_email': 'andres@reveronmolina.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/systemallica/morfist',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.0,<4.0.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['biasedclassifier']

package_data = \
{'': ['*']}

install_requires = \
['scikit-learn>=0.23.2,<0.24.0']

setup_kwargs = {
    'name': 'biasedclassifier',
    'version': '0.1.1',
    'description': '',
    'long_description': "# Biased Classifier\n\nBiased Classifier\n\n## Install\n\nDirectly from `PyPi` servers:\n\n```\npip install BiasedClassifier\n```\n\n## Use\n\nExample using Random Forests from `scikit-learn`.\n\nAssume `X, y` is a training set with three classes and two heavily inbalanced classes. In this case, we'd like to bias two classifiers into these subsets. We've decided that `0.3` and `0.2` proportions are enough for the minority classes (from smaller up)\n\n```\nfrom biasedclassifier import BiasedClassifier\nfrom sklearn.ensemble import RandomForestClassifier\n\nclf = BiasedClassifier(\n    k=5, \n    p=[0.3, 0.2], \n    unbiased_classifier=RandomForestClassifier(), \n    knn_jobs=1\n)\n\n# Train\nclf.fit(X,y)\n\n# Obtain probabilities for each class\nprob = clf.predict_proba(X)\n\n# Predicted values\ny_pred = clf.predict(X)\n\n# Average accuracy score\nscore = clf.score(X, y)\n```",
    'author': 'Rodrigo Parra',
    'author_email': 'contact@rodrigo-parra.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rparraca/BiasedClassifier',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

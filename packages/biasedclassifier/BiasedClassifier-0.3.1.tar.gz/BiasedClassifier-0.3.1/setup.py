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
    'version': '0.3.1',
    'description': '',
    'long_description': "# Biased Classifier\n\nBiased Classifier\n\nCurrent version: 0.3.0\n\n## Install\n\nDirectly from `PyPi` servers:\n\n```\npip install biasedclassifier\n```\n\n## Interface\n\nEstimator's constructor:\n\n```\nBiasedClassifier(\n    p=[0.0],\n    unbiased_estimator=None,\n    knn=None\n)\n```\nwhere `unbiased_estimator` is the base estimator to use (and to biased towards critical set). We pass a `k-NearestNeighbor` object directly via the paramter `knn`.\n\n\n## Use\n\nExample using Random Forests from `scikit-learn`.\n\nAssume `X, y` is a training set with three classes and two heavily inbalanced classes. In this case, we'd like to bias two classifiers into these subsets. We've decided that `0.3` and `0.2` proportions are enough for the minority classes (from smaller up) and `k=10` neighbors to collect for critical set. Our unbiased estimator will be a random forest of size 200.\n\n```\nfrom biasedclassifier import BiasedClassifier\nfrom sklearn.neighbors import NearestNeighbors\nfrom sklearn.ensemble import RandomForestClassifier\n\nclf = BiasedClassifier(\n    p=[0.3, 0.2], \n    unbiased_classifier=RandomForestClassifier(n_estimators=200), \n    knn=NearestNeighbors(n_neighbors=10)\n)\n\n# Train\nclf.fit(X,y)\n\n# Obtain probabilities for each class\nprob = clf.predict_proba(X)\n\n# Predicted values\ny_pred = clf.predict(X)\n\n# Average accuracy score\nscore = clf.score(X, y)\n```\n\nIt is important to note that `BiasedEstimator` does not change the state of both objects `unbiased_classifier` and `knn`. Instead, it uses clones internally to do its operations.\n\n## Compatibility\n\nThis model is compatible with all of the capabilities offered by `scikit-learn` requiring `get_params` and `score` methods.",
    'author': 'Rodrigo Parra',
    'author_email': 'contact@rodrigo-parra.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://rparraca.github.io/BiasedClassifier/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

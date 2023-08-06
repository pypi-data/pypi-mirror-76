# Biased Classifier

Biased Classifier

## Install

Directly from `PyPi` servers:

```
pip install BiasedClassifier
```

## Use

Example using Random Forests from `scikit-learn`.

Assume `X, y` is a training set with three classes and two heavily inbalanced classes. In this case, we'd like to bias two classifiers into these subsets. We've decided that `0.3` and `0.2` proportions are enough for the minority classes (from smaller up)

```
from biasedclassifier import BiasedClassifier
from sklearn.ensemble import RandomForestClassifier

clf = BiasedClassifier(
    k=5, 
    p=[0.3, 0.2], 
    unbiased_classifier=RandomForestClassifier(), 
    knn_jobs=1
)

# Train
clf.fit(X,y)

# Obtain probabilities for each class
prob = clf.predict_proba(X)

# Predicted values
y_pred = clf.predict(X)

# Average accuracy score
score = clf.score(X, y)
```
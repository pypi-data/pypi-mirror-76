import numpy as np
from sklearn.base import BaseEstimator, clone
from sklearn.neighbors import NearestNeighbors
from sklearn.utils.validation import check_X_y, check_array, check_is_fitted
from sklearn.utils.multiclass import unique_labels
from sklearn.metrics import accuracy_score

__version__ = "0.1.1"


class BiasedClassifier(BaseEstimator):
    def __init__(self, k=5, p=[0.5], unbiased_classifier=None, knn_jobs=1):
        """
        BiasedClassifier constructor.

        Parameters
        ----------
        k : positive integer
            Number of neighbors to be used by k-Nearest Neighbor

        p : array-like, shape = (n_critical_sets,)
            Array of proportions to weight biased classifiers.

        unbiased_classifier : estimator object
            The estimator to be used for full training set and critical sets. 
            It must be clonable.

        knn_jobs : positive integer
            The number of jobs to run in parallel when training k-Nearest 
            Neighbor algorithm.

        Returns
        -------
        score : float
            Mean accuracy of self.predict(X) wrt. y.
        """
        super(BiasedClassifier, self).__init__()
        self.k = k
        self.p = p
        self.unbiased_classifier = unbiased_classifier
        self.knn_jobs = knn_jobs

    def fit(self, X, y):
        """
        Build biased classifier(s) from critical sets

        Parameters
        ----------
        X : array-like, shape = (n_samples, n_features)
            Training samples.

        y : array-like, shape = (n_samples,)
            True labels for X.

        Returns
        -------
        self : object
            A reference to itself.
        """
        # Check parameter correctness
        assert self.k > 0 and (self.k - int(self.k)) == 0
        assert sum(self.p) < 1.0
        for p_i in self.p:
            assert p_i > 0.0 and p_i < 1.0
        assert self.unbiased_classifier is not None
        assert self.knn_jobs > 0 and (self.knn_jobs - int(self.knn_jobs)) == 0

        # Check that X and y have correct shape
        X, y = check_X_y(X, y)

        # Store the classes seen during fit
        self.classes_ = unique_labels(y)
        self.X_ = X
        self.y_ = y

        indexes = []
        for target in self.classes_:
            this_idx = np.where(self.y_ == target)
            indexes.append(
                {"target": target, "index": this_idx, "size": len(this_idx[0])}
            )

        # Setup relevant models
        self.kNN_ = NearestNeighbors(n_neighbors=self.k, n_jobs=self.knn_jobs)
        self.kNN_.fit(self.X_)

        self.unbiased_classifier_crit_ = []
        for p_i in self.p:
            self.unbiased_classifier_crit_.append(clone(self.unbiased_classifier))

        indexes = sorted(indexes, key=lambda x: x["size"])
        for i in range(0, len(self.p)):
            crit_idx = np.unique(
                self.kNN_.kneighbors(
                    X=self.X_[indexes[i]["index"]], return_distance=False
                ).ravel()
            )
            # When splitting critical sets, nothing prevents the split
            # to completely miss a class. To further assure that all
            # classes are seen by all classifiers, we require to have
            # at least one class of each
            for check_class in self.classes_:
                check_idx = np.where(self.y_[crit_idx] == check_class)
                if len(check_idx[0]) == 0:
                    crit_idx = np.append(
                        crit_idx, np.where(self.y_ == check_class)[0][0]
                    )

            self.unbiased_classifier_crit_[i].fit(self.X_[crit_idx], self.y_[crit_idx])

        self.unbiased_classifier.fit(X=self.X_, y=self.y_)

        return self

    def predict_proba(self, X):
        """
        The class probabilities of the input samples.

        Parameters
        ----------
        X : array-like, shape = (n_samples, n_features)
            Training samples.

        Returns
        -------
        p : array-like, shape = (n_samples,)
             The class probabilities of the input samples.
        """
        prob = self.unbiased_classifier.predict_proba(X) * (1 - sum(self.p))
        for i in range(0, len(self.p)):
            prob = np.add(
                prob, self.p[i] * self.unbiased_classifier_crit_[i].predict_proba(X)
            )

        return prob

    def predict(self, X):
        """
        The predicted class of an input sample.

        Parameters
        ----------
        X : array-like, shape = (n_samples, n_features)
            Test samples.

        Returns
        -------
        y : array-like, shape = (n_samples,)
            The predicted classes.
        """

        # Check is fit had been called
        check_is_fitted(self)

        # Input validation
        X = check_array(X)

        return self.classes_[np.argmax(self.predict_proba(X), axis=1)]

    def score(self, X, y, sample_weight=None):
        """
        Returns the mean accuracy on the given test data and labels.

        Parameters
        ----------
        X : array-like, shape = (n_samples, n_features)
            Test samples.

        y : array-like, shape = (n_samples,)
            True labels for X.

        sample_weight : array-like, shape = [n_samples], optional
            Sample weights.

        Returns
        -------
        score : float
            Mean accuracy of self.predict(X) wrt. y.
        """
        # Check that X and y have correct shape
        X, y = check_X_y(X, y)
        return accuracy_score(
            y_true=y, y_pred=self.predict(X), sample_weight=sample_weight
        )

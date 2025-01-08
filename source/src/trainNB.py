import numpy as np
class SimpleMultinomialNB:
    def __init__(self):
        self.class_log_prior_ = {}
        self.feature_log_prob_ = {}
        self.classes_ = []
    def fit(self, X, y):
        self.classes_ = np.unique(y)
        feature_count = np.zeros((len(self.classes_), len(X[0])))
        class_count = np.zeros(len(self.classes_))
        for xi, label in zip(X, y):
            class_idx = np.where(self.classes_ == label)[0][0]
            feature_count[class_idx] += xi
            class_count[class_idx] += 1
        self.class_log_prior_ = np.log(class_count / class_count.sum()) # Prior probability
        smoothed_fc = feature_count + 1  # Laplace smoothing
        smoothed_cc = smoothed_fc.sum(axis=1, keepdims=True)
        self.feature_log_prob_ = np.log(smoothed_fc / smoothed_cc) # Likelihood
    def predict_log_proba(self, X):
        return [self.class_log_prior_ + (x @ self.feature_log_prob_.T) for x in X] # Posterior 
    def predict(self, X):
        log_proba = self.predict_log_proba(X)
        return [self.classes_[np.argmax(lp)] for lp in log_proba]
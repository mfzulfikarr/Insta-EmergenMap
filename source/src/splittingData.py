import pandas as pd
import random
import numpy as np
import re
def train_test_split(X, y, test_size=0.3, random_state=None, stratify=None):
    if random_state is not None:
        random.seed(random_state)
        np.random.seed(random_state)
    data = list(zip(X, y))
    random.shuffle(data)
    X, y = zip(*data)
    if stratify is None:
        classes, counts = np.unique(y, return_counts=True) # Calculate class distribution
        stratify = y
    idx = np.arange(len(y)) # Shuffle indices for stratified sampling
    if stratify is not None:
        idx = np.random.permutation(idx)
    split_idx = int(len(y) * (1 - test_size))
    train_idx = idx[:split_idx]
    test_idx = idx[split_idx:]

    X_train = [X[i] for i in train_idx]
    X_test = [X[i] for i in test_idx]
    y_train = [y[i] for i in train_idx]
    y_test = [y[i] for i in test_idx]

    return X_train, X_test, y_train, y_test
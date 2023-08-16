"""

========================================================

"""
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_boston
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
import pickle


data = load_boston()

X_train, X_test, y_train, y_test = train_test_split(data.data, data.target)

clf = GradientBoostingRegressor()
clf.fit(X_train, y_train)

predicted = clf.predict(X_test)
expected = y_test

print("RMS: %r " % np.sqrt(np.mean((predicted - expected) ** 2)))


# export pickle file
pickle.dump(clf, open('model.pkl', 'wb'))



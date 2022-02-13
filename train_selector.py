import os
import json
import pickle
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

'''
Load Data
'''
data_algo = pd.read_csv("data_algo.csv")
f_algo = np.array(data_algo["FID"])

os.chdir("./Feature_values")
function_files = os.listdir()

X_learn = []
y_learn = []
for f in f_algo:
    algo = data_algo[data_algo["FID"] == f]["AlgID"].values[0]
    fd = open("function_"+f+"_all.json")
    data_phi = json.load(fd)
    for i in range(len(data_phi)):
        y_learn.append(algo)
        tmp = np.fromiter(data_phi[str(i)].values(), dtype=float)
        X_learn.append(tmp)

'''
Create selector
'''
clf = RandomForestClassifier()
clf.fit(X_learn, y_learn)
pickle.dump(clf, open("selector.p", "wb"))

import os
import json
import argparse
import numpy as np
from ioh import get_problem
from pflacco.pflacco import create_feature_object, calculate_feature_set


def compute_one_set(feature_set):
    # Create feature object
    feat_object = create_feature_object(points, obj_values, lower = the.lower_bound, upper = the.upper_bound)
    # Calculate feature set
    features = calculate_feature_set(feat_object, feature_set)
    feat_eval = feature_set+".costs_fun_evals"
    feat_runtime = feature_set+".costs_runtime"
    del features[feat_eval]
    del features[feat_runtime]
    return features

def compute_all_sets():
    phi_sets = ["disp", "ela_meta", "ela_distr", "nbc","ic", "pca"]
    # Create feature object
    feat_object = create_feature_object(points, obj_values, lower = the.lower_bound, upper = the.upper_bound)
    features_full = {}
    # Calculate feature sets
    for phi in phi_sets:
        features = calculate_feature_set(feat_object, phi)
        feat_eval = phi+".costs_fun_evals"
        feat_runtime = phi+".costs_runtime"
        del features[feat_eval]
        del features[feat_runtime]
        features_full.update(features)
    return features_full

'''
Argument parser
'''

can = argparse.ArgumentParser()

can.add_argument("-d", "--dimension", default=5, type=int, help="Dimension of the objective function")

can.add_argument("-nb", "--sampling_ID", default=0, type=int, help="ID of the sample file")

can.add_argument("-f", "--feature_set", default='ela_meta', help="Feature set to compute")

can.add_argument("-fid", "--functionID", default=1, help="Function ID")

can.add_argument("-iid", "--instanceID", default=1, help="Instance ID")

can.add_argument("-func_set", "--function_set", default='BBOB', help="Function set")

the = can.parse_args()
the.functionID = int(the.functionID)
the.instanceID = int(the.instanceID)


'''
Load samples
'''

points = np.genfromtxt("./Sampling/sampling_sobol"+str(the.sampling_ID)+".csv", delimiter=',')


'''
Create and evaluate function
'''
if the.function_set == "BBOB":
    function_name = "FID_"+str(the.functionID)+"_IID_"+str(the.instanceID)
    f = get_problem(the.functionID, the.instanceID, the.dimension, problem_type="BBOB")
    obj_values = np.array([])
    for i in range(len(points)):
        obj_values = np.append(obj_values, f(points[i]))

else:
    print('TODO')#TODO

'''
Compute features
'''
if not os.path.exists("./Feature_values"):
    os.mkdir("./Feature_values")
os.chdir("./Feature_values")

if the.feature_set == "all":
    features = compute_all_sets()
    features_file = {the.sampling_ID : features}
    if not os.path.exists("function_"+function_name+"_"+the.feature_set+".json"):
        with open("function_"+function_name+"_"+the.feature_set+".json", "w") as fd:
            json.dump(features_file, fd)
    else:
        with open("function_"+function_name+"_"+the.feature_set+".json", "r+") as fd:
            data = json.load(fd)
            data.update(features_file)
            fd.seek(0)
            json.dump(data, fd)
else:
    features = compute_one_set(the.feature_set)
    features_file = {the.sampling_ID : features}
    if not os.path.exists("function_"+function_name+"_"+the.feature_set+".json"):
        with open("function_"+function_name+"_"+the.feature_set+".json", "w") as fd:
            json.dump(features_file, fd)
    else:
        with open("function_"+function_name+"_"+the.feature_set+".json", "r+") as fd:
            data = json.load(fd)
            data.update(features_file)
            fd.seek(0)
            json.dump(data, fd)

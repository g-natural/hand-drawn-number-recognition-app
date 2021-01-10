import numpy as np
import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import CRNNetwork as cn
import pickle
import pdb
from pathlib import Path

def test_on_sets(nnet: cn.CRNNetwork, limit: int=None):
    # these labels are used for all test sets
    label_file = os.path.join('assets', 'mnist', "testing10000_labels.csv")
    mnist_test_labels = np.loadtxt(open(label_file, 'rb'), delimiter=",")

    test_dir = os.path.join('assets', "test_sets")
    test_sets = list(Path(test_dir).glob('*.csv'))
    
    if limit is not None:
        if (limit < 1) or (limit > len(test_sets)):
            raise IndexError("Specified limit not within test set size")
            return
    else:
        limit = len(test_sets)
        if limit == 0:
            raise RuntimeError("Testing set directory is empty")

    corr_avg = 0
    for i in range(limit):
        set_file = test_sets[i]
        input_matrix = np.loadtxt(open(set_file, 'rb'), delimiter=",")
        corr_avg += nnet.test_network(input_matrix, mnist_test_labels ,set_file)

    corr_avg /= limit
    print(f"Correct % Avg: {corr_avg}")
    return corr_avg


def main():
    model_name = "CRNNet_45Nodes_.pkl"
    model_file = os.path.join(os.path.dirname(os.getcwd()), "model", model_name)
    nnetwork = pickle.load(open(model_file, 'rb'))
    test_on_sets(nnetwork)

if __name__ == '__main__':
    main()


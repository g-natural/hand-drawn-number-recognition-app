import numpy as np
import os
import sys
import test_network as testnet
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import CRNNetwork as cn
import pickle
import argparse
from pathlib import Path
import pdb

def train_on_sets(nnet: cn.CRNNetwork, limit: int=None,
                  test_step: int=10):
    # these labels are used for all train sets
    label_file = os.path.join('assets', 'mnist', "training60000_labels.csv")
    mnist_train_labels = np.loadtxt(open(label_file, 'rb'), delimiter=",")

    train_dir = os.path.join('assets', "train_sets")
    train_sets = list(Path(train_dir).glob('*.csv'))
#    train_sets = [f.name for f in path.glob('*.csv')]

    if limit is not None:
        if (limit < 1) or (limit > len(train_sets)):
            raise IndexError("specified limit not within train set size")
            return
    else:
        limit = len(train_sets)
        if limit == 0:
            raise RuntimeError("Training set directory is empty")

    if test_step <= 0: # if <= 0 only run test at beginning
        test_step = limit + 1

    # initial test on sets to gauge progress
    last_avg = testnet.test_on_sets(nnet)
    corr_avg = last_avg
    for i in range(limit):
        print(f"Training set: {i}/{limit-1}")
        set_file = train_sets[i]
        input_matrix = np.loadtxt(open(set_file, 'rb'), delimiter=",")
        nnet.train_network(input_matrix, mnist_train_labels, set_file)

        if (i+1 % test_step) == 0:
            last_avg = corr_avg
            corr_avg = testnet.test_on_sets(nnet)
            print(f"% Correct Increase: {corr_avg - last_avg}\n")

    if (limit % test_step) != 0:
        testnet.test_on_sets(nnet)

def main():
    parser = argparse.ArgumentParser(description="Train new or existing neural network on character sets. By default will create new network.")
    parser.add_argument("--existing", metavar="MODEL_NAME", type=str, help="train on an existing model")
    parser.add_argument("--hnodes", type=int, help="specify amount of hidden nodes in network.")
    parser.add_argument("--model_name", type=int, help="specify the name to save model as (do not include file suffix).")
    args = parser.parse_args()

    HNODES = 48 # default amount of hidden nodes for new networks

    pdb.set_trace()
    if args.existing is not None:
        model_name = args.existing
        model_file = os.path.join(os.path.dirname(os.getcwd()), "model", model_name)
        nnetwork = pickle.load(open(model_file, 'rb'))
    else:
        if args.hnodes is not None:
            HNODES = args.hnodes
        nnetwork = cn.CRNNetwork(784, HNODES, 10)
    try:
        train_on_sets(nnetwork)
    except Exception as error:
        error
    finally:
        model_name = f"NNet_{nnetwork.hidden_ncount}Nodes_"
        if args.model_name is not None:
            model_name = args.model_name

        model_name = f"{model_name}.pkl"
        save_location = os.path.join("model", model_name)
        pickle.dump(nnetwork, open(save_location, 'wb'), protocol=4)

if __name__ == '__main__':
    main()


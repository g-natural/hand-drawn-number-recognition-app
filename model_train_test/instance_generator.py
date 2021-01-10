import random
import numpy as np
import os
import argparse
import sys
import pdb
import copy
from pathlib import Path

class InstanceTransform():
    def __init__(self, xdim=28, ydim=28):
        self.xdim = xdim
        self.ydim = ydim

    # functions return row or column given
    # location (index) from instance vector
    # (note rows, cols and locs are all 0 indexed)
    def _get_row(self, loc):
        return int(loc / self.xdim)

    def _get_col(self, loc):
        return loc % self.ydim

    def _get_loc(self, row, col):
        return (row*self.ydim) + col

    # functions to make instances series of only
    # values 0 and 0.99
    @staticmethod
    def _make_number_thin(vector):
        for i in range(len(vector)):
            if(vector[i] < .9):
                vector[i] = 0
            else:
                vector[i] = 0.99

    @staticmethod
    def _make_number_thick(vector):
        for i in range(len(vector)):
            if(vector[i] > .1):
                vector[i] = 0.99
            else:
                vector[i] = 0

    # scanning from left-to-right up-to-down
    # get the row of the first non-zero character
    def _get_upper_bound(self, vector):
        for i in range(len(vector)):
            if(vector[i] > 0):
                return self._get_row(i)
        return -1

    # scan from right-to-left down-to-up
    def _get_lower_bound(self, vector):
        for i in range(len(vector)-1, -1, -1):
            if(vector[i] > 0):
                return (self.ydim-1) - self._get_row(i)
        return -1

    # scan the grid up-to-down, left-to-right
    def _get_left_bound(self, vector):
        for col in range(self.xdim):
            for row in range(self.ydim):
                loc = self._get_loc(row, col)
                if(vector[loc] > 0):
                    return col
        return -1

    # scan the grid up-to-down, right to left
    def _get_right_bound(self, vector):
        for col in range(self.xdim-1, -1, -1):
            for row in range(self.ydim):
                loc = self._get_loc(row, col)
                if(vector[loc] > 0):
                    return (self.xdim-1) - col
        return -1

    def _translate_number(self, vector, d_row, d_col):
        # d_row and d_col speciy what will be added to
        # current row and column position of each colored pixel
        # (note +d_row translates 'down' -d_row 'up',
        # +d_col 'right' -d_col 'left')
        if(d_row == 0 and d_col == 0):
            return

        if(d_row < 0):  # translating up
            r_start = 0
            r_stop = self.ydim
            r_incr = 1
        else:  # translating down
            r_start = self.ydim-1
            r_stop = -1
            r_incr = -1
        if(d_col < 0):  # translating left
            c_start = 0
            c_stop = self.xdim
            c_incr = 1
        else:  # translating right
            c_start = self.xdim-1
            c_stop = -1
            c_incr = -1

        for row in range(r_start, r_stop, r_incr):
            for col in range(c_start, c_stop, c_incr):
                loc = self._get_loc(row, col)
                if(vector[loc] > 0):
                    new_loc = self._get_loc(row + d_row, col + d_col)
                    vector[new_loc] = vector[loc]
                    vector[loc] = 0

    def transform_number(self, vector, all_thick=False, all_thin=False):
        use_thick = random.getrandbits(1)
        if(all_thick):
            self._make_number_thick(vector)
        elif(all_thin):
            self._make_number_thin(vector)
        elif(use_thick):
            self._make_number_thick(vector)
        else:
            self._make_number_thin(vector)

        t_up = random.getrandbits(1)
        t_left = random.getrandbits(1)
        d_row = 0
        d_col = 0

        if(t_up):  # translate up
            upper_bound = (-1)*self._get_upper_bound(vector)
            if(upper_bound != 0):
                d_row = random.randint(upper_bound, -1)
        else:  # translate down
            lower_bound = self._get_lower_bound(vector)
            if(lower_bound != 0):
                d_row = random.randint(1, lower_bound)
        if(t_left):  # translate left
            left_bound = (-1)*self._get_left_bound(vector)
            if(left_bound != 0):
                d_col = random.randint(left_bound, -1)
        else:  # translate right
            right_bound = self._get_right_bound(vector)
            if(right_bound != 0):
                d_col = random.randint(1, right_bound)

        self._translate_number(vector, d_row, d_col)


def main():
    parser = argparse.ArgumentParser(description="Use existing MNIST data sets to generate " +
                                     "more sets with the numbers transformed on the canvas")
    parser.add_argument("--test_sets", metavar=("GEN_COUNT", "INPUT_FILE"), nargs='*',
                        help="Specify file to generate test sets with and amount to generate")
    parser.add_argument("--train_sets", metavar=("GEN_COUNT", "INPUT_FILE"), nargs='*',
                        help="Specify file to generate train sets with and amount to generate")
    args = parser.parse_args()

    # default parameters
    testfile = os.path.join('assets', "mnist", "testing10000.csv")
    trainfile = os.path.join('assets', "mnist", "training60000.csv")
    test_dir = os.path.join('assets', "test_sets")
    train_dir = os.path.join('assets', "train_sets")
    test_save_file = os.path.join(test_dir,"testing_10k")
    train_save_file = os.path.join(train_dir,"training_60k")
    test_gen_count =  3#5
    train_gen_count =  5#40
    gen_train_sets = True
    gen_test_sets = True

    # if no args are specified, both sets will generate, if only one
    # is, only that set will be generated
    if (args.test_sets is not None) and (args.train_sets is None):
        gen_train_sets = False
    elif (args.train_sets is not None) and (args.test_sets is None):
        gen_test_sets = False

    def check_set(argset, set_type):
        setfile = None
        gen_count = None
        if(argset is not None):
            if len(argset) > 2:
                sys.exit(f"{set_type} option takes max of 2 args.")
            if len(argset) >= 1:
                try:
                    gen_count = int(argset[0])
                except ValueError:
                    setfile = argset[0]
            if len(argset) == 2:
                setfile = argset[1]
        return setfile, gen_count
    
    setfile, gen_count = check_set(args.test_sets, "test_sets")
    if setfile is not None:
        testfile = setfile
    if gen_count is not None:
        test_gen_count = gen_count

    setfile, gen_count = check_set(args.train_sets, "train_sets")
    if setfile is not None:
        trainfile = setfile
    if gen_count is not None:
        train_gen_count = gen_count

    transformer = InstanceTransform(xdim=28, ydim=28)
    def gen_set(setfile, setdir, gen_count, save_file_name):
        input_matrix = np.loadtxt(setfile, delimiter=",", ndmin=2)
        
        # get count of files in set dir
        # (all files generated will be added to directory)
        fcount = len(list(Path(setdir).glob('*.csv')))
        start = fcount
        for i in range(start, gen_count+start, 1):
            # since transforms are in-place, a copy must be made
            # for all transformations to be done on original set 
            imatrix_copy  = copy.deepcopy(input_matrix)
            for vector in imatrix_copy:
                transformer.transform_number(vector)

            save_file = f"{save_file_name}_{i}.csv"
            np.savetxt(save_file, imatrix_copy, fmt='%1.2f', delimiter=",")

    if(gen_test_sets):
        gen_set(testfile, test_dir, test_gen_count, test_save_file)

    if(gen_train_sets):
        gen_set(trainfile, train_dir, train_gen_count, train_save_file)


if __name__ == '__main__':
    main()

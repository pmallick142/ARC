#!/usr/bin/python
'''

Student Name: Pradip Mallick
Student Id: 20236170

'''

import os, sys
import json
import numpy as np
import re

### YOUR CODE HERE: write at least three functions which solve
### specific tasks by transforming the input x and returning the
### result. Name them according to the task ID as in the three
### examples below. Delete the three examples. The tasks you choose
### must be in the data/training directory, not data/evaluation.

color_code = {'black': 0, 'blue': 1, 'red': 2, 'green': 3, 'yellow': 4, 'gray': 5, 'magenta': 6, 'orange': 7, 'sky': 8, 'brown': 9}

def solve_007bbfb7(x):
    resample_x = x.repeat(3, axis=0)
    resample_x = resample_x.repeat(3, axis=1)
    tile_x = np.tile(x, (3, 3))
    x = resample_x & tile_x
    return x

def solve_05269061(x):
    colors = np.repeat(color_code['black'], 3)
    dimens, elems = x.shape
    
    for dimen in range(dimens):
        for elem in range(elems):
            color = x[dimen, elem]
            if color != 0:
                colors[(dimen + elem) % 3] = color
    
    x = x.copy()
    for dimen in range(dimens):
        for elem in range(elems):
            x[dimen, elem] = colors[(dimen + elem) % 3]
    return x

def solve_08ed6ac7(x):
    dimens, elems = x.shape
    x = x.copy()    
    colors = [color_code['blue'], color_code['red'], color_code['green'], color_code['yellow']]
    colors_idx = 0
    for dimen in range(dimens):
        for elem in range(elems):
            if x[dimen, elem] == color_code['gray']:
                for y in range(dimen, dimens):
                    x[y, elem] = colors[colors_idx]
                colors_idx += 1
    return x

def main():
    # Find all the functions defined in this file whose names are
    # like solve_abcd1234(), and run them.

    # regex to match solve_* functions and extract task IDs
    p = r"solve_([a-f0-9]{8})" 
    tasks_solvers = []
    # globals() gives a dict containing all global names (variables
    # and functions), as name: value pairs.
    for name in globals(): 
        m = re.match(p, name)
        if m:
            # if the name fits the pattern eg solve_abcd1234
            ID = m.group(1) # just the task ID
            solve_fn = globals()[name] # the fn itself
            tasks_solvers.append((ID, solve_fn))

    for ID, solve_fn in tasks_solvers:
        # for each task, read the data and call test()
        directory = os.path.join("..", "data", "training")
        json_filename = os.path.join(directory, ID + ".json")
        data = read_ARC_JSON(json_filename)
        test(ID, solve_fn, data)
    
def read_ARC_JSON(filepath):
    """Given a filepath, read in the ARC task data which is in JSON
    format. Extract the train/test input/output pairs of
    grids. Convert each grid to np.array and return train_input,
    train_output, test_input, test_output."""
    
    # Open the JSON file and load it 
    data = json.load(open(filepath))

    # Extract the train/test input/output grids. Each grid will be a
    # list of lists of ints. We convert to Numpy.
    train_input = [np.array(data['train'][i]['input']) for i in range(len(data['train']))]
    train_output = [np.array(data['train'][i]['output']) for i in range(len(data['train']))]
    test_input = [np.array(data['test'][i]['input']) for i in range(len(data['test']))]
    test_output = [np.array(data['test'][i]['output']) for i in range(len(data['test']))]

    return (train_input, train_output, test_input, test_output)


def test(taskID, solve, data):
    """Given a task ID, call the given solve() function on every
    example in the task data."""
    print(taskID)
    train_input, train_output, test_input, test_output = data
    print("Training grids")
    for x, y in zip(train_input, train_output):
        yhat = solve(x)
        show_result(x, y, yhat)
    print("Test grids")
    for x, y in zip(test_input, test_output):
        yhat = solve(x)
        show_result(x, y, yhat)

        
def show_result(x, y, yhat):
    print("Input")
    print(x)
    print("Correct output")
    print(y)
    print("Our output")
    print(yhat)
    print("Correct?")
    # if yhat has the right shape, then (y == yhat) is a bool array
    # and we test whether it is True everywhere. if yhat has the wrong
    # shape, then y == yhat is just a single bool.
    print(np.all(y == yhat))

if __name__ == "__main__": main()


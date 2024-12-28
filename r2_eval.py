import os
import pickle
import numpy as np
from sympy import lambdify, symbols, expand

# Define task
task = "1_base"
input_dir = './results/dso_models/'

for filename in os.listdir(input_dir):
    
    if filename.endswith('.pkl'):
        print(filename)
        # Load formula
        try:
            with open(os.path.join(input_dir, filename), 'rb') as f:
                formula = pickle.load(f)
        except EOFError:
            print(f"Error: Unable to load formula, file {filename} may be empty or corrupted.")
            continue  # Skip the current file, continue processing the next file
        print("Formula:", formula)
        print("Formula type:", type(formula))
        
        # Extract the key part of the real equation file name
        clean_name = filename.split('.txt')[0]
        # Read data
        data_file_path = f'./resource/datasets/srsd/{task}/test/{clean_name}.txt'
        
        if not os.path.exists(data_file_path):
            print(f"Error: Data file {data_file_path} not found.")
            continue
        
        data = np.loadtxt(data_file_path)
        X = data[:, :-1]
        y_true = data[:, -1]
        # Create lambdify function, expand formula
        variables = symbols('x0:{}'.format(X.shape[1]))
        expanded_formula = expand(formula)  # Expand formula
        f = lambdify(variables, expanded_formula, modules='numpy')  # Add modules='numpy'

        # Calculate predicted values
        try:
            y_pred = f(*[X[:, i] for i in range(X.shape[1])])
        except NameError as e:
            print(f"Error: {e}, skipping file {filename}.")
            continue  # Skip the current file, continue processing the next file

        # Calculate R^2
        ss_res = np.sum((y_true - y_pred) ** 2)
        ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
        r_squared = 1 - (ss_res / ss_tot)
        print(f"{filename}: R^2 value: {r_squared}")
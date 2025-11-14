# Name: Atahan Evintan
# ID: 820230334

import numpy as np
import os

def get_data_path(filename):
    """Constructs the absolute path to a data file regardless of CWD."""
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    parent_dir = os.path.dirname(script_dir)
    

    return os.path.join(parent_dir, 'data', filename)


prior_file = get_data_path('prior.csv')
conditional_file = get_data_path('conditional.csv')

Prior = np.genfromtxt(prior_file, delimiter=',', dtype=float)
Likelihood = np.genfromtxt(conditional_file, delimiter=',', dtype=float)


P_L = Prior.flatten()
P_O_given_L = Likelihood.flatten()


P_O_intersect_L = P_O_given_L * P_L
P_O = np.sum(P_O_intersect_L)


Posterior_flat = P_O_intersect_L / P_O

Posterior = Posterior_flat.reshape((4, 4))


max_prob = np.max(Posterior)
max_index_flat = np.argmax(Posterior_flat)
max_row = max_index_flat // 4
max_col = max_index_flat % 4
max_cell_info = f"Cell (Row {max_row + 1}, Col {max_col + 1})"


print("Marginal Likelihood P(O):", P_O)
print("\nPosterior Probabilities P(L_i | O):")
print(Posterior)
print("\nHighest Probable Cell:")
print(f"Probability: {max_prob}")
print(f"Location: {max_cell_info}")
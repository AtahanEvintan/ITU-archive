# Name: Atahan Evintan
# ID: 820230334


import numpy as np
import os

def get_data_path(filename):
    """Constructs the absolute path to a data file regardless of CWD."""
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    
    parent_dir = os.path.dirname(script_dir)
    
  
    return os.path.join(parent_dir, 'data', filename)


data_file = get_data_path('bats.csv')
GENE_COLS = list(range(5))
TRAIT_COL = 5
GENE_NAMES = ['G0', 'G1', 'G2', 'G3', 'G4']
TOLERANCE = 1e-4 


try:
    
    data_str = np.genfromtxt(data_file, delimiter=',', dtype=str, skip_header=1)
    
   
    data = (data_str == 'True').astype(int)
    N = data.shape[0]

    print(f"Data successfully loaded. Number of bats: {N}")
    print("-" * 50)

except Exception as e:
    print(f"Error loading data: {e}")
    
    exit() 


def calculate_marginal_probabilities(D):
    """Calculates P(X) for all 6 variables (5 genes + 1 trait)."""
   
    probabilities = np.mean(D, axis=0)
    return probabilities


def calculate_conditional_probabilities(D, trait_col, gene_cols):
    """Calculates P(T | Gi) for each gene Gi."""
    conditional_probs = np.empty(len(gene_cols))
    
    for i, g_col in enumerate(gene_cols):
       
        D_conditioned = D[D[:, g_col] == 1]
        
        if D_conditioned.shape[0] == 0:
            P_T_given_Gi = 0.0
        else:
           
            P_T_given_Gi = np.mean(D_conditioned[:, trait_col])
            
        conditional_probs[i] = P_T_given_Gi
        
    return conditional_probs


P_X = calculate_marginal_probabilities(data)
P_T = P_X[TRAIT_COL]
P_T_given_Gi = calculate_conditional_probabilities(data, TRAIT_COL, GENE_COLS)



print("--- a) Marginal Probabilities P(X) ---")
results_a = np.empty(6)
for i in range(6):
    name = GENE_NAMES[i] if i < TRAIT_COL else 'T'
    prob = P_X[i]
    results_a[i] = prob
    print(f"P({name}) = {prob:.5f}")
print(f"Function Return (P(G0), ..., P(G4), P(T)):\n{results_a}")
print("-" * 50)



print("--- b) Conditional Probabilities P(T | Gi) ---")
results_b = np.empty(5)
for i in range(5):
    name = GENE_NAMES[i]
    prob = P_T_given_Gi[i]
    results_b[i] = prob
    print(f"P(T | {name}) = {prob:.5f}")
print(f"Function Return (P(T|G0), ..., P(T|G4)):\n{results_b}")
print("-" * 50)



print("--- c) Independence/Dependence Decision ---")
print(f"Marginal P(T) = {P_T:.5f}")

for i in range(5):
    name = GENE_NAMES[i]
    P_T_Gi = P_T_given_Gi[i]
    
    
    if abs(P_T_Gi - P_T) < TOLERANCE:
        dependence_status = "INDEPENDENT"
    else:
        dependence_status = "DEPENDENT"
        
    print(f"Gene {name}: P(T | {name}) = {P_T_Gi:.5f}. Diff: {abs(P_T_Gi - P_T):.5f}. Status: {dependence_status}")
print("-" * 50)



print("--- d) Conditional Probabilities P(T | Gi and Gj) and Dependency Check ---")


representative_pairs = [(0, 1), (0, 2)] 

for i, j in representative_pairs:
    G_i_name = GENE_NAMES[i]
    G_j_name = GENE_NAMES[j]
    
    
    denominator_mask = (data[:, i] == 1) & (data[:, j] == 1)
    count_denominator = np.sum(denominator_mask)
    
    P_T_given_Gi_prev = P_T_given_Gi[i]
    
    if count_denominator == 0:
        P_T_given_Gi_Gj = 0.0
    else:

        numerator_mask = denominator_mask & (data[:, TRAIT_COL] == 1)
        count_numerator = np.sum(numerator_mask)
        P_T_given_Gi_Gj = count_numerator / count_denominator
    
    
    
    if abs(P_T_given_Gi_Gj - P_T_given_Gi_prev) < TOLERANCE:
        conditional_dependence_status = "CONDITIONALLY INDEPENDENT"
    else:
        conditional_dependence_status = "CONDITIONALLY DEPENDENT"
        
    
    print(f"P(T | {G_i_name}, {G_j_name}) = {P_T_given_Gi_Gj:.5f}")
    print(f"  P(T | {G_i_name}) = {P_T_given_Gi_prev:.5f}. Diff: {abs(P_T_given_Gi_Gj - P_T_given_Gi_prev):.5f}.")
    print(f"  Decision: T is {conditional_dependence_status} of {G_j_name} given {G_i_name}.")
    print("-" * 20)
print("-" * 50)



print("--- e) Calculate E[K] ---")


P_genes = P_X[GENE_COLS]
E_K = np.sum(P_genes)

print(f"E[K] = P(G0) + P(G1) + P(G2) + P(G3) + P(G4)")
print(f"E[K] = {P_genes[0]:.5f} + {P_genes[1]:.5f} + {P_genes[2]:.5f} + {P_genes[3]:.5f} + {P_genes[4]:.5f}")
print(f"E[K] = {E_K:.5f}")
print("-" * 50)
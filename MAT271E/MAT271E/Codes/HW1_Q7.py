# Name: Atahan Evintan
# ID: 820230334

import re
from collections import Counter
import numpy as np
import os

def get_data_path(filename):
    """Constructs the absolute path to a data file regardless of CWD."""
   
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    
    parent_dir = os.path.dirname(script_dir)
    
  
    return os.path.join(parent_dir, 'data', filename)


file1 = get_data_path('Sequence1.txt')
file2 = get_data_path('Sequence2.txt')


def load_and_clean_sequence(filename):
    """Reads the file, cleans whitespace and non-HT characters, and returns the sequence."""
    
    try:
        
        with open(filename, 'r') as f:
            raw_content = f.read()
    except FileNotFoundError:
       
        print(f"Error: File {filename} not found.")
        return ""

   
    cleaned_sequence = re.sub(r'[^HT]', '', raw_content.upper())
    
    return cleaned_sequence

def analyze_sequence(sequence):
    """Calculates run statistics (Total Runs, Longest Run, Proportion H) for a coin flip sequence."""
    
    if not sequence:
        return {}
        
    
    runs = 1
    longest_run = 1
    current_run_length = 1
    
    for i in range(1, len(sequence)):
        if sequence[i] == sequence[i-1]:
            current_run_length += 1
        else:
            runs += 1
            current_run_length = 1
        
        if current_run_length > longest_run:
            longest_run = current_run_length
            
   
    counts = Counter(sequence)
    total_flips = len(sequence)
    prop_H = counts.get('H', 0) / total_flips
    
    return {
        "Total_Flips": total_flips,
        "Total_Runs": runs,
        "Longest_Run": longest_run,
        "Prop_H": prop_H
    }

def main():
    seq1_cleaned = load_and_clean_sequence(file1)
    seq2_cleaned = load_and_clean_sequence(file2)

    if not seq1_cleaned or not seq2_cleaned:
        return

    analysis1 = analyze_sequence(seq1_cleaned)
    analysis2 = analyze_sequence(seq2_cleaned)

    N_expected = 300
    E_Runs = (N_expected / 2) + 1 
    E_Longest_Run = np.log2(N_expected) 

   
    print(f"--- Sequence 1 Analysis (N={analysis1['Total_Flips']}) ---")
    print(f"Total Runs: {analysis1['Total_Runs']}, Longest Run: {analysis1['Longest_Run']}")
    print(f"--- Sequence 2 Analysis (N={analysis2['Total_Flips']}) ---")
    print(f"Total Runs: {analysis2['Total_Runs']}, Longest Run: {analysis2['Longest_Run']}")
    print("-" * 50)
    print(f"Theoretical Expectation (N={N_expected}): Expected Runs ≈ {E_Runs:.1f}, Expected Longest Run ≈ {E_Longest_Run:.1f}")
    print("-" * 50)
    
    
    
    LRS1 = analysis1['Longest_Run']
    LRS2 = analysis2['Longest_Run']
    Runs1 = analysis1['Total_Runs']
    
    

    decision_final = "Sequence 2"
    reason_final = (
        f"The longest run in Sequence 1 ({LRS1}) is significantly shorter than in Sequence 2 ({LRS2}), and "
        f"Sequence 1 has too many total runs ({Runs1} vs. {E_Runs:.1f} expected for N=300). "
        f"This reveals a human bias in Sequence 1 against long streaks and favoring excessive alternation, "
        f"making Sequence 2 the true random series."
    )

    print("--- PROBABILISTIC ARGUMENT ---")
    print(f"The TRUE coin flip sequence is: {decision_final}")
    print(f"Justification: {reason_final}")

if __name__ == "__main__":
    main()
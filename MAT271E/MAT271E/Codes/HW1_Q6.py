# Name: Atahan Evintan
# ID: 820230334


import numpy as np
import matplotlib.pyplot as plt
from numpy.random import rand


def simulate_bernoulli(p=0.4):
    """X ~ Ber(p). Returns 1 for success, 0 for failure."""
    if rand() < p:
        return 1
    return 0


def simulate_binomial(n=20, p=0.4):
    """Simulates X ~ Bin(n, p)."""
    success_count = 0
    for _ in range(n):
        if rand() < p:
            success_count += 1
    return success_count


def simulate_geometric(p=0.03):
    """Simulates X ~ Geo(p)."""
    trials = 0
    while True:
        trials += 1
        if rand() < p:
            return trials
            

def simulate_negative_binomial(r=5, p=0.03):
    """Simulates X ~ NegBin(r, p)."""
    successes_needed = r
    trials = 0
    while successes_needed > 0:
        trials += 1
        if rand() < p:
            successes_needed -= 1
    return trials


def simulate_poisson(lamb=3.1):
    """Simulates X ~ Poi(lamb) (Approximate)."""
    N = 60000 
    p = lamb / N 
    
    success_count = 0
    for _ in range(N):
        if rand() < p:
            success_count += 1
    return success_count


def simulate_exponential(lamb=3.1):
    """Simulates X ~ Exp(lamb) (Approximate)."""
    N_intervals_per_unit_time = 60000
    p = lamb / N_intervals_per_unit_time
    
    time_unit = 1.0 / N_intervals_per_unit_time
    
    intervals = 0
    while True:
        intervals += 1
        if rand() < p:
            return intervals * time_unit



def main():
    
   
    print("Bernoulli:", simulate_bernoulli())

   
    NUM_CALLS = 1000

    binom_results = [simulate_binomial() for _ in range(NUM_CALLS)]
    geom_results = [simulate_geometric() for _ in range(NUM_CALLS)]
    nbin_results = [simulate_negative_binomial() for _ in range(NUM_CALLS)]
    poisson_results = [simulate_poisson() for _ in range(NUM_CALLS)]
    exp_results = [simulate_exponential() for _ in range(NUM_CALLS)]

    
    fig, axes = plt.subplots(3, 2, figsize=(12, 12))
    fig.suptitle(f'Simulations of Random Variables ({NUM_CALLS} Calls Each)', fontsize=16)

    
    axes[0, 0].hist(binom_results, bins=np.arange(np.min(binom_results)-0.5, np.max(binom_results)+1.5), density=True, rwidth=0.8, color='skyblue', edgecolor='black')
    axes[0, 0].set_title(r'$X \sim Bin(n=20, p=0.4)$')
    axes[0, 0].set_xlabel("Number of Successes (K)")

    
    axes[0, 1].hist(geom_results, bins=np.arange(np.min(geom_results)-0.5, np.max(geom_results)+1.5), density=True, rwidth=0.8, color='lightcoral', edgecolor='black')
    axes[0, 1].set_title(r'$X \sim Geo(p=0.03)$')
    axes[0, 1].set_xlabel("Number of Trials (K)")

  
    axes[1, 0].hist(nbin_results, bins=np.arange(np.min(nbin_results)-0.5, np.max(nbin_results)+1.5), density=True, rwidth=0.8, color='lightgreen', edgecolor='black')
    axes[1, 0].set_title(r'$X \sim NegBin(r=5, p=0.03)$')
    axes[1, 0].set_xlabel("Number of Trials (K)")

   
    axes[1, 1].hist(poisson_results, bins=np.arange(np.min(poisson_results)-0.5, np.max(poisson_results)+1.5), density=True, rwidth=0.8, color='gold', edgecolor='black')
    axes[1, 1].set_title(r'$X \sim Poi(\lambda=3.1)$ (Approx)')
    axes[1, 1].set_xlabel("Number of Events (K)")

    
    axes[2, 0].hist(exp_results, bins=50, density=True, color='mediumpurple', edgecolor='black')
    axes[2, 0].set_title(r'$X \sim Exp(\lambda=3.1)$ (Approx)')
    axes[2, 0].set_xlabel("Time until Next Event (T)")
    axes[2, 0].set_ylabel("Probability Density")

    
    axes[2, 1].axis('off')

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig('HW1_Q6_Histograms.png')

    print("-" * 50)
    print("Histograms saved to HW1_Q6_Histograms.png")
    print("Simulation Means (Verification of E[X]):")
    print(f"Binomial (E=8.0): {np.mean(binom_results):.4f}")
    print(f"Geometric (E≈33.33): {np.mean(geom_results):.4f}")
    print(f"NegBinomial (E≈166.67): {np.mean(nbin_results):.4f}")
    print(f"Poisson (E=3.1): {np.mean(poisson_results):.4f}")
    print(f"Exponential (E≈0.322): {np.mean(exp_results):.4f}")


if __name__ == "__main__":
    main()
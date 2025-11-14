# Name: Atahan Evintan
# ID: 820230334

"""
Hints:
- Notice the strict inequality in the looping condition
  (until Sum > 100, and Sum > 200)
- The function np.random.randint(low, high) is INCLUSIVE of low
  and EXCLUSIVE of high. Hence, we should have low=1 and high=101.
- Player 2 wins if and only if y > x, not when y >= x.
- Player 2 resumes adding from Player 1's sum.
  Player 2 does NOT start over at 0.
"""


import numpy as np



def simulate_game():
    """Simulates a single round of the two-player sum game."""
    
   
    current_sum = 0
    while True:
       
        r = np.random.randint(1, 101) 
        current_sum += r
        if current_sum > 100:
            r1 = r  
            break
            
   
    while True:
        r = np.random.randint(1, 101)
        current_sum += r
        if current_sum > 200:
            r2 = r  
            break
            
    
    return 1 if r2 > r1 else 0

NUM_SIMULATIONS = 100000


results = np.array([simulate_game() for _ in range(NUM_SIMULATIONS)])


player2_wins = np.sum(results)
player1_wins = NUM_SIMULATIONS - player2_wins


P_P2_win = player2_wins / NUM_SIMULATIONS
P_P1_win = player1_wins / NUM_SIMULATIONS


print(f"Total Simulations: {NUM_SIMULATIONS}")
print("-" * 35)
print(f"Player 1 Wins: {player1_wins}")
print(f"Player 2 Wins: {player2_wins}")
print("-" * 35)
print(f"Estimated Probability (Player 1 Wins): {P_P1_win:.4f}")
print(f"Estimated Probability (Player 2 Wins): {P_P2_win:.4f}")


# Name: Atahan Evintan
# ID: 820230334

import random
import re


OPPONENT_CARDS = 2
TABLE_CARDS = 7
NUM_SIMULATIONS = 100000


P_TELL_GIVEN_LOSE = 0.5  
P_TELL_GIVEN_WIN = 0.1  

def create_card():
    """Creates a standard 52-card deck represented as a list of strings."""
    cards = []
    for suit in   [r'D',r'C',r'H',r'S']:
        for card in  ['A','2','3','4','5','6','7','8','9','10','J','Q','K']:
            cards.append(card+suit)
    return cards

def create_board_and_hand():
    """Simulates dealing the cards, determines the game outcome, and generates the tell."""
    cards = create_card()
    random.shuffle(cards)
    
   
    [cards.pop(0) for _ in range(TABLE_CARDS)]
    

    opponent_hand = [cards.pop(0) for _ in range(OPPONENT_CARDS)]
    

    is_loss = False
    

    for i in [0,1]:
      
        a = random.randint(0, len(opponent_hand)-1) 
        
        
        s = opponent_hand[a]
        
      
        ll = bool(re.search(r'[A]', s[0]))
        
        if ll:
            is_loss = True
            break
        
   
    
    win_status = 1 if not is_loss else 0 

    
    if is_loss: 
        tell_prob = P_TELL_GIVEN_LOSE
    else: 
        tell_prob = P_TELL_GIVEN_WIN
        
    tell_status = 1 if random.random() < tell_prob else 0 
        
   
    return win_status, tell_status




Wins = []
Tells = []

for _ in range(NUM_SIMULATIONS):
    win, tell = create_board_and_hand()
    Wins.append(win)
    Tells.append(tell)


W_T_count = 0  
L_T_count = 0  
W_N_count = 0  

for i in range(NUM_SIMULATIONS):
    if Wins[i] == 1 and Tells[i] == 1:
        W_T_count += 1
    elif Wins[i] == 0 and Tells[i] == 1:
        L_T_count += 1
    elif Wins[i] == 1 and Tells[i] == 0:
        W_N_count += 1


P_T_sim = (W_T_count + L_T_count) / NUM_SIMULATIONS
P_N_sim = 1.0 - P_T_sim


P_W_given_T = (W_T_count / NUM_SIMULATIONS) / P_T_sim if P_T_sim > 0 else 0.0


P_W_given_N = (W_N_count / NUM_SIMULATIONS) / P_N_sim if P_N_sim > 0 else 0.0



print(f"Total Simulations: {NUM_SIMULATIONS}")
print("-" * 50)


print(f"Calculated Probability of Winning (Opponent does not have an ace) under the condition:")
print(f"  If there is a tell:   {P_W_given_T:.5f}")
print(f"  If there is no tell:  {P_W_given_N:.5f}")
print("-" * 50)


final_win, final_tell = create_board_and_hand()
tell_output = "TELL" if final_tell == 1 else "NO TELL"

print(f"Algorithm Result for One Simulated Round:")
print(f"Printed Result: {tell_output}")
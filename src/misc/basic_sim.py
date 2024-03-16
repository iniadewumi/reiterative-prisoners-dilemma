# from models import *

def prisoners_dilemma(player1_action, player2_action):
    if player1_action == 'cooperate' and player2_action == 'cooperate':
        return 3, 3
    elif player1_action == 'cooperate' and player2_action == 'defect':
        return 0, 5
    elif player1_action == 'defect' and player2_action == 'cooperate':
        return 5, 0
    else:
        return 1, 1

        
def run_simulation(player1, player2, rounds=10):
    results = []
    for _ in range(rounds):
        p1_action = player1.next_move()
        p2_action = player2.next_move()
        p1_score, p2_score = prisoners_dilemma(p1_action, p2_action)
        results.append((p1_score, p2_score))
    return results

player1 = AlwaysCooperate()
player2 = AlwaysDefect()
results = run_simulation(player1, player2)
analysis = analyze_results(results)
print("Player 1 Total Score:", analysis[0])
print("Player 2 Total Score:", analysis[1])

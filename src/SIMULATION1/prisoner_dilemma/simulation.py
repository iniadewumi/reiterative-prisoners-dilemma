import itertools
import pandas as pd
from prisoner_dilemma.analysis import plot_results

class Simulation:
    def __init__(self, agents, payoffs=None):
        self.agents = agents
        self.results = []
        self.round_count = 0
        self.payoffs = payoffs if payoffs else {
            ('C', 'C'): (1, 1),
            ('C', 'D'): (-1, 1),
            ('D', 'C'): (1, -1),
            ('D', 'D'): (0, 0)
        }

    def run_simulation(self, rounds=5, verbose=True):
        for r in range(rounds):
            if verbose: print(f"\nRound {r}")
            for agent1, agent2 in itertools.combinations(self.agents, 2):
                if verbose: print(f"\t{agent1.name} vs {agent2.name}")
                self.play_round(agent1, agent2, r, verbose)
            self.round_count = r

    def play_round(self, agent1, agent2, round_no, verbose=True):
        decision1 = agent1.decide(agent2)
        decision2 = agent2.decide(agent1)
        payoff1, payoff2 = self.payoffs[(decision1, decision2)]

        agent1.update_history(decision1, decision2)
        agent2.update_history(decision2, decision1)
        agent1.score += payoff1
        agent2.score += payoff2
        if verbose: print(f"\t{decision1} vs {decision2}")
        self.results.append({
            'Round': round_no,
            'Agent1': agent1.name,
            'Agent2': agent2.name,
            'Agent1_Score': agent1.score,
            'Agent2_Score': agent2.score,
            'Decision1': decision1,
            'Decision2': decision2,
            'Payoff1': payoff1,
            'Payoff2': payoff2
        })

    def analyze_results(self):
        self.results_df = pd.DataFrame(self.results)
        scores_data = []
        for agent in self.agents:
            scores_data.append([agent.name, agent.strategy, agent.score])
        
        self.scores_df = pd.DataFrame(data=scores_data, columns=["Name", "Strategy", "Score"]).sort_values('Score', inplace=True)
        plot_results(self.scores_df)
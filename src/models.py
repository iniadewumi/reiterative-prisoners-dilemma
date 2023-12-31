
import random
import itertools 
import pandas as pd

class Simulation:
    def __init__(self, agents):
        self.agents = agents
        self.results = []
        self.payoffs = {
            ('C', 'C'): (3, 3),  # Both cooperate
            ('C', 'D'): (0, 5),  # Player 1 cooperates, Player 2 defects
            ('D', 'C'): (5, 0),  # Player 1 defects, Player 2 cooperates
            ('D', 'D'): (1, 1)   # Both defect
        }

    def run_simulation(self, rounds=5):
        for r in range(rounds):
            print(f"Round {r}")
            for agent1, agent2 in itertools.combinations(self.agents, 2):
                self.play_round(agent1, agent2)

        self.results_df = pd.DataFrame(self.results)
        self.scores_df  = pd.DataFrame()
        score_results = [{"Name", "Strategy", "Score", "Round"}]
        for agent in agents:
            {}
            self.scores_df.append()

    def analyze_results(self):
        return 
            
    def play_round(self, agent1, agent2, round_no):
        decision1 = agent1.decide(agent2)
        decision2 = agent2.decide(agent1)
        payoff1, payoff2 = self.payoffs[(decision1, decision2)]

        agent1.update_history(decision1, decision2)
        agent2.update_history(decision2, decision1)
        agent1.score+=payoff1
        agent2.score+=payoff2

        self.results.append({
            'Round'; round_no,
            'Agent1': agent1.name,
            'Agent2': agent2.name,
            'Agent1_Score': agent1.score,
            'Agent2_Score': agent2.score,
            'Decision1': decision1,
            'Decision2': decision2,
            'Payoff1': payoff1,
            'Payoff2': payoff2
        })

class Agent:
    def __init__(self, name, strategy, model=None):
        if strategy=='adaptive' and not model:
            raise ValueError("Model must be provided if adaptive strategy")
        self.name = name
        self.strategy = strategy
        self.history = []
        self.model = model
        self.score = 0
        

    def decide(self, opponent):
        # Implement strategy logic here
        if self.strategy == 'random':
            return random.choice(['C', 'D'])
        elif self.strategy == "tit-for-tat":
            if not opponent.history:  # If no history yet, start with cooperation
                return 'C'
            else:
                return opponent.history[-1][1]  # Mirror the opponent's last decision
        elif self.strategy == "always-cooperate":
            return 'C'
        elif self.strategy == "always-defect":
            return 'D'
        elif self.strategy == "adaptive":
            return 
            # self.model.
        else:
            raise NotImplementedError


        # Additional strategies can be added here
    def update_history(self, own_decision, opponent_decision):
        self.history.append((own_decision, opponent_decision))


agents = [
        Agent(name="Cooper", strategy="always-cooperate"), 
        Agent(name="Devin", strategy="always-defect"), 
        Agent(name="Randy", strategy="random"), 
        Agent(name="Titi", strategy="tit-for-tat")
        # agent5 = Agent(name="Groot", strategy="adaptive", model=)
        # agent6 = Agent(name="Forrest", strategy="adaptive", model=)


]


simulation = Simulation(agents)
simulation.run_simulation(1)




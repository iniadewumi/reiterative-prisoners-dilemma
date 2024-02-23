
import random
import itertools 
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from creme import tree
import matplotlib.pyplot as plt
import seaborn as sns

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
        import pandas as pd
        self.results_df = pd.DataFrame(self.results)
        scores_data = []
        for agent in self.agents:
            scores_data.append([agent.name, agent.strategy, agent.score])
        
        self.scores_df = pd.DataFrame(data=scores_data, columns=["Name", "Strategy", "Score"]).sort_values('Score', inplace=True)
        plot_results(self.scores_df)

def plot_results(df):
    plt.figure(figsize=(10, 6))
    sns.barplot(x="Score", y="Name", data=df.sort_values("Score", ascending=True), hue="Strategy", dodge=False)
    plt.title("Scores of Agents by Strategy in the Iterative Prisoner's Dilemma")
    plt.xlabel("Score")
    plt.ylabel("Agent")
    plt.legend(title="Strategy", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(axis='x')
    plt.show()


class Agent:
    def __init__(self, name, strategy):
        self.name = name
        self.strategy = strategy
        self.history = []
        self.score = 0

    def decide(self, opponent):
        if self.strategy == 'random':
            return random.choice(['C', 'D'])
        elif self.strategy == "tit-for-tat":
            return 'C' if not opponent.history else opponent.history[-1][1]
        elif self.strategy == "always-cooperate":
            return 'C'
        elif self.strategy == "always-defect":
            return 'D'
        elif self.strategy == "tit-for-2-tat":
            if len(opponent.history) >= 2 and opponent.history[-1][1] == 'D' and opponent.history[-2][1] == 'D':
                return 'D'
            return 'C'
        else:
            raise NotImplementedError("Unknown strategy")

    def update_history(self, own_decision, opponent_decision):
        self.history.append((own_decision, opponent_decision))

class HeuristicAgent(Agent):
    def __init__(self, name):
        super().__init__(name, strategy="heuristic")

    def decide(self, opponent):
        if len(opponent.history) >= 5:
            last_five = [action[1] for action in opponent.history[-5:]]
            defections = last_five.count('D')
            return 'D' if defections > 2 else 'C'
        return 'C'

class ProbabilisticAgent(Agent):
    def __init__(self, name):
        super().__init__(name, strategy="probabilistic")

    def decide(self, opponent):
        if len(opponent.history) >= 5:
            cooperation_probability = sum(action[1] == 'C' for action in opponent.history[-5:]) / 5
            return 'D' if cooperation_probability < 0.6 else 'C'
        return 'D'

class DecisionTreeAgent(Agent):
    def __init__(self, name, decision_tree_model=None):
        super().__init__(name, strategy="decision-tree")
        self.model = decision_tree_model or DecisionTreeClassifier()

    def decide(self, opponent):
        if len(opponent.history) < 2:
            return random.choice(['C', 'D'])

        history_df = pd.DataFrame(opponent.history, columns=['Own_Decision', 'Opponent_Decision'])
        history_df.replace({'C': 1, 'D': 0}, inplace=True)

        if not hasattr(self, 'model_fitted'):
            self.model.fit(history_df[['Opponent_Decision']], history_df['Own_Decision'])
            self.model_fitted = True

        last_decision = [{'C': 1, 'D': 0}[opponent.history[-1][1]]]
        prediction = self.model.predict([last_decision])[0]
        return ['C', 'D'][prediction]

class AdaptiveAgent(Agent):
    def __init__(self, name, model=None):
        super().__init__(name, strategy="adaptive")
        self.model = model or DecisionTreeClassifier()
        self.initialized = False

    def decide(self, opponent):
        if self.initialized:
            features = self.extract_features(opponent)
            decision = self.model.predict([features])[0]
            return 'C' if decision == 1 else 'D'
        return random.choice(['C', 'D'])

    def update_model(self, opponent):
        if len(self.history) >= 2:
            self.initialized = True
            features = self.extract_features(opponent)
            label = 1 if self.history[-1][0] == 'C' else 0
            self.model.fit([features], [label])

    def extract_features(self, opponent):
        last_five = opponent.history[-5:]
        coop_count = sum(1 for _, action in last_five if action == 'C')
        def_count = sum(1 for _, action in last_five if action == 'D')
        return [coop_count, def_count]


agents = [
        Agent(name="Cooper", strategy="always-cooperate"), 
        Agent(name="Devin", strategy="always-defect"), 
        Agent(name="Randy", strategy="random"), 
        Agent(name="Titi", strategy="tit-for-tat"),
        Agent(name="Tata", strategy="tit-for-2-tat"),
        AdaptiveAgent(name="Groot"),
        ProbabilisticAgent(name="Prosper"),
        HeuristicAgent(name='Eureka'),
        DecisionTreeAgent(name="Destiny")
]


simulation = Simulation(agents)
simulation.run_simulation(5000)







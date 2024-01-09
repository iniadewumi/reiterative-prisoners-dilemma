
import random
import itertools 
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from creme import tree

class Simulation:
    def __init__(self, agents):
        self.agents = agents
        self.results = []
        self.payoffs = {
            ('C', 'C'): (1, 1),  # Both cooperate
            ('C', 'D'): (-1, 1),  # Player 1 cooperates, Player 2 defects
            ('D', 'C'): (1, -1),  # Player 1 defects, Player 2 cooperates
            ('D', 'D'): (0, 0)   # Both defect
        }
        # self.payoffs = {
        #     ('C', 'C'): (3, 3),  # Both cooperate
        #     ('C', 'D'): (0, 5),  # Player 1 cooperates, Player 2 defects
        #     ('D', 'C'): (5, 0),  # Player 1 defects, Player 2 cooperates
        #     ('D', 'D'): (1, 1)   # Both defect
        # }

    def run_simulation(self, rounds=5):
        for r in range(rounds):
            print(f"\nRound {r}")
            for agent1, agent2 in itertools.combinations(self.agents, 2):
                print(f"\t{agent1.name} vs {agent2.name}")
                self.play_round(agent1, agent2, r)
        self.analyze_results()

    def analyze_results(self):
        self.results_df = pd.DataFrame(self.results)
        scores_data = []
        for agent in self.agents:
            scores_data.append([agent.name, agent.strategy, agent.score])
        
        self.scores_df  = pd.DataFrame(data=scores_data, columns=["Name", "Strategy", "Score"])
            

    def play_round(self, agent1, agent2, round_no):
        decision1 = agent1.decide(agent2)
        decision2 = agent2.decide(agent1)
        payoff1, payoff2 = self.payoffs[(decision1, decision2)]

        agent1.update_history(decision1, decision2)
        agent2.update_history(decision2, decision1)
        agent1.score+=payoff1
        agent2.score+=payoff2
        print(f"\t{decision1} vs {decision1}")
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
        elif self.strategy == "tit-for-2-tat":
            if opponent.history[-1][1]+opponent.history[-2][1]=='DD':
                return 'D'
            else:
                return 'C'
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
        elif self.strategy == "tit-for-2-tat":
            if opponent.history[-1][1]+opponent.history[-2][1]=='DD':
                return 'D'
            else:
                return 'C'
        else:
            raise NotImplementedError


        # Additional strategies can be added here
    def update_history(self, own_decision, opponent_decision):
        self.history.append((own_decision, opponent_decision))



class HeuristicAgent(Agent):
    def __init__(self, name):
        super().__init__(name, strategy="heuristic")

    def decide(self, opponent):
        # Heuristic based on opponent's last 5 actions
        if len(opponent.history) >= 5:
            last_five = [action[1] for action in opponent.history[-5:]]
            defections = last_five.count('D')
            if defections > 2:  # More defections than cooperations
                return 'D'
            else:
                return 'C'
        else:
            return 'C'  # Default to cooperation if not enough history


class ProbabilisticAgent(Agent):
    def __init__(self, name):
        super().__init__(name, strategy="probabilistic")

    def decide(self, opponent):
        if opponent.history:
            cooperation_probability = (opponent.history[-5:].count('C')/5)
            return 'D' if cooperation_probability<0.6 else 'C'
        else:
            return 'D'

class DecisionTreeAgent(Agent):
    def __init__(self, name, decision_tree_model=None):
        super().__init__(name, strategy="decision-tree")
        self.model = decision_tree_model or DecisionTreeClassifier()

    def decide(self, opponent):
        # Use the decision tree model to make a decision
        # Example: Use the last round as input to the model
        if not opponent.history:
            return random.choice(['C', 'D'])  # Random choice if no history
        temp_df = pd.DataFrame(opponent.history)
        temp_df.replace({'C':1, 'D':0}, inplace=True)
        self.model.fit(X=temp_df[1].values.reshape(-1,1), y=temp_df[0])
        last_round = opponent.history[-1][0]
        prediction = self.model.predict([[{'C':1, 'D':0}.get(last_round)]])[0]
        return ['D', 'C'][prediction]



class AdaptiveAgent(Agent):
    def __init__(self, name):
        self.model = tree.DecisionTreeClassifier()
        super().__init__(name, strategy="adaptive", model=self.model)
        self.initialized = False

    def decide(self, opponent):
        # Extract features and predict
        if self.initialized:
            features = self.extract_features(opponent)
            decision = self.model.predict_one(features)
            return 'C' if decision else 'D'
        else:
            return random.choice(['C', 'D'])  # Random choice before model is initialized

    def update_model(self, opponent):
        if not self.initialized:
            self.initialized = True
        features = self.extract_features(opponent)
        label = 1 if self.history[-1][0] == 'C' else 0  # Last action as label
        self.model.fit_one(features, label)

    def extract_features(self, opponent):
        # Define feature extraction logic here
        # Example: Features could be the count of cooperations and defections in the last few rounds
        features = {}
        features['opponent_coop_count'] = sum(1 for _, action in opponent.history[-5:] if action == 'C')
        features['opponent_def_count'] = sum(1 for _, action in opponent.history[-5:] if action == 'D')
        return features

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
simulation.run_simulation(10000)







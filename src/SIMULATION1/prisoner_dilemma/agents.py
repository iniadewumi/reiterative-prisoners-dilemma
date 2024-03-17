import random
import pandas as pd
from sklearn.tree import DecisionTreeClassifier

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
    def __init__(self, name, model=None):
        super().__init__(name, strategy="decision-tree")
        self.model = model or DecisionTreeClassifier()

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
        self.update_model(opponent)
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


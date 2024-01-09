from sklearn.tree import DecisionTreeClassifier
from creme import tree

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
    def __init__(self, name, cooperation_probability=0.5):
        super().__init__(name, strategy="probabilistic")
        self.cooperation_probability = cooperation_probability

    def decide(self, opponent):
        if opponent.history:
            
            return 'C'
        else:
            return 'D'

class DecisionTreeAgent(Agent):
    def __init__(self, name, decision_tree_model=None):
        super().__init__(name, strategy="decision-tree")
        self.model = decision_tree_model or DecisionTreeClassifier()

    def decide(self, opponent):
        # Use the decision tree model to make a decision
        # Example: Use the last round as input to the model
        if not self.history:
            return random.choice(['C', 'D'])  # Random choice if no history
        last_round = self.history[-1]
        prediction = self.model.predict([last_round])
        return prediction[0]



class AdaptiveAgent(Agent):
    def __init__(self, name):
        super().__init__(name, strategy="adaptive")
        self.model = tree.DecisionTreeClassifier()
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

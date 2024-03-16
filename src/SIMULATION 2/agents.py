import random
# from sklearn.tree import DecisionTreeClassifier
from creme import tree

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
        
    def analyze_opponent_history(self, opponent):
        if len(opponent.history) < 2 or self.strategy in ["always-cooperate", "always-defect"]:
            return None

        last_two_actions = [action[1] for action in opponent.history[-2:]]
        if last_two_actions == ['D', 'D']:
            return 'D'
        elif last_two_actions == ['C', 'C']:
            return 'C'
        else:
            return None

class HeuristicAgent(Agent):
    def __init__(self, name, defection_threshold=0.6):
        super().__init__(name, strategy="heuristic")
        self.defection_threshold = defection_threshold

    def analyze_action_sequence(self, last_five):
        if len(last_five) == 0:
            return 'C'
        
        if len(last_five) < 3:
            return 'D' if last_five[-1] == 'D' else 'C'

        last_three_actions = last_five[-3:]
        if last_three_actions == ['D', 'C', 'C']:
            return 'C'
        elif last_three_actions == ['C', 'D', 'D']:
            return 'D'  
        return None

    def decide(self, opponent):
        """Make a decision based on the opponent's history."""
        last_five = [action[1] for action in opponent.history[-5:]]
        pattern_decision = self.analyze_action_sequence(last_five)
        
        if pattern_decision is not None:
            return pattern_decision
        else:
            defections = last_five.count('D')
            proportion_of_def = defections/len(last_five) if last_five else 0
            return 'D' if proportion_of_defections > self.defection_threshold else 'C'


class PunisherAgent(HeuristicAgent):
    def __init__(self, name, defection_threshold=0.6):
        super().__init__(name, defection_threshold=defection_threshold)
        self.the_punished = {}

    def analyze_action_sequence(self, last_five, opponent):
        if len(last_five) >= 3 and last_five[-3:] == ['D', 'D', 'D']:
            self.the_punished[opponent.name] = 5
            return 'D'        
        return super().analyze_action_sequence(last_five, opponent)

    def decide(self, opponent):
        """Make a decision based on the opponent's history."""
        # Check if the opponent is currently being punished
        if opponent.name in self.the_punished:
            if self.the_punished[opponent.name] <= 1:
                del self.the_punished[opponent.name]  # Remove from punishment if period is over
            else:
                self.the_punished[opponent.name] -= 1 
                return 'D'  # Continue punishing

        return super().decide(opponent)



class ProbabilisticAgent(Agent):
    def __init__(self, name, initial_threshold=0.6):
        super().__init__(name, strategy="probabilistic")
        self.cooperation_threshold = initial_threshold
        self.opponent_scores = {}

    def adjust_threshold_based_on_performance(self, opponent):
        if opponent.name in self.opponent_scores:
            wins, losses = self.opponent_scores[opponent.name]
            if wins > losses:
                self.cooperation_threshold = max(0.5, self.cooperation_threshold - 0.1)  # cooperative if winning
            else:
                self.cooperation_threshold = min(0.7, self.cooperation_threshold + 0.1)  # less cooperative if losing
        else:
            self.opponent_scores[opponent.name] = (0, 0)

    def update_performance(self, opponent, result):
        wins, losses = self.opponent_scores.get(opponent.name, (0, 0))
        if result == 'W':
            wins += 1
        else:
            losses += 1
        self.opponent_scores[opponent.name] = (wins, losses)

    def decide(self, opponent):
        self.adjust_threshold_based_on_performance(opponent)
        cooperation_probability = sum(action[1] == 'C' for action in opponent.history[-5:]) / 5 if opponent.history else 0
        decision = 'D' if cooperation_probability < self.cooperation_threshold else 'C'

        # Assume a win if deciding to cooperate and opponent's cooperation probability is high, else assume a loss
        self.update_performance(opponent, 'W' if decision == 'C' and cooperation_probability >= 0.5 else 'L')
        return decision


class IncremDecisionTreeAgent(Agent):
    def __init__(self, name, model=None):
        super().__init__(name, strategy="decision-tree")
        self.model = decision_tree_model or tree.DecisionTreeClassifier()

    def decide(self, opponent):
        if len(opponent.history) < 1:
            return random.choice(['C', 'D'])
        
        last_decision = {'C':1, 'D':0}[opponent.history[-1][1]]
        prediction = self.model.predict_one()

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


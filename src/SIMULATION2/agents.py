import random
# from sklearn.tree import DecisionTreeClassifier
from creme import tree
import numpy as np
import pandas as pd

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
        if len(last_five) == 0: return 'C'
        if len(last_five) < 3: return 'D' if last_five[-1] == 'D' else 'C'

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
            proportion_of_defections = defections/len(last_five) if last_five else 0
            return 'D' if proportion_of_defections > self.defection_threshold else 'C'


class PunisherAgent(Agent):
    def __init__(self, name, defection_threshold=0.6):
        super().__init__(name, strategy="punisher")
        self.defection_threshold = defection_threshold
        self.the_punished = {}

    def analyze_action_sequence(self, last_five, opponent):
        if not last_five: return 'C'
        if len(last_five) < 3: return 'D' if last_five[-1] == 'D' else 'C'

        last_three_actions = last_five[-3:]
        if last_three_actions == ['D', 'C', 'C']:
            return 'C'
        elif last_three_actions == ['C', 'D', 'D']:
            return 'D'
        elif last_three_actions == ['D', 'D', 'D']:
            self.the_punished[opponent.name] = 5
            return 'D'

        return None

    def decide(self, opponent):
        if opponent.name in self.the_punished:
            if self.the_punished[opponent.name] <= 1:
                del self.the_punished[opponent.name]
            else:
                self.the_punished[opponent.name] -= 1
                return 'D'  # Keep punishing

        last_five = [action[1] for action in opponent.history[-5:]]
        pattern_decision = self.analyze_action_sequence(last_five, opponent)
        
        if pattern_decision is not None:
            return pattern_decision
        else:
            defections = last_five.count('D')
            proportion_of_defections = defections / len(last_five) if last_five else 0
            return 'D' if proportion_of_defections > self.defection_threshold else 'C'


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
        self.model = model or tree.DecisionTreeClassifier()
        self.opponent_cols = {}

    def decide(self, opponent):
        if len(opponent.history) < 2:
            self.opponent_cols[opponent.name] = 0
            return 'C'
        
        # collect last 2 decisions to get training data (2nd to last decision)
        # Use last decision as target, then, fit.
        last_two_decisons = opponent.history[-2:]
        features_to_train = self.opponent_cols | {opponent.name:1, 'Last_Decision':{'C':1, 'D':0}[last_two_decisons[-2][1]]}
        target = {'C':1, 'D':0}[last_two_decisons[-1][1]]
        self.model.fit_one(features_to_train, target)
        
        # Use last decision as feature, then, predict.
        features_to_predict = self.opponent_cols | {opponent.name:1, 'Last_Decision':{'C':1, 'D':0}[last_two_decisons[-1][1]]}
        prediction = self.model.predict_one(features_to_predict)
        
        if 'CD' in [i+j for i,j in opponent.history]:
            return 'D'
        else:
            return ['D', 'C'][prediction]




# As provided by Claude
class QLearningAgent(Agent):
    def __init__(self, name, alpha=0.1, gamma=0.9, epsilon=0.2, epsilon_decay=0.99, min_epsilon=0.01):
        super().__init__(name, strategy="q-learning")
        self.q_table = {}
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.min_epsilon = min_epsilon

    def get_state(self, opponent):
        # Enhanced state representation: Use the last two moves
        history = opponent.history[-2:]
        return ''.join([str(h[1]) for h in history]) or "initial"

    def update_q_value(self, state, action, reward, next_state):
        old_value = self.q_table.get((state, action), 0.0)
        future_rewards = max(self.q_table.get((next_state, a), 0.0) for a in ['C', 'D'])
        new_value = old_value + self.alpha * (reward + self.gamma * future_rewards - old_value)
        self.q_table[(state, action)] = new_value


    def decide(self, opponent):
        state = self.get_state(opponent)
        if np.random.uniform() < self.epsilon:
            action = np.random.choice(['C', 'D'])
        else:
            q_values = {a: self.q_table.get((state, a), 0.0) for a in ['C', 'D']}
            action = max(q_values, key=q_values.get)
        self.last_state = state
        self.last_action = action
        return action

    def update(self, opponent, reward):
        next_state = self.get_state(opponent)
        self.update_q_value(self.last_state, self.last_action, reward, next_state)
        # Apply epsilon decay
        self.epsilon = max(self.min_epsilon, self.epsilon * self.epsilon_decay)

    def log_info(self):
        # Example logging function to monitor agent's performance and learning
        print(f"Current Q-Table: {self.q_table}")
        print(f"Current Epsilon: {self.epsilon}")

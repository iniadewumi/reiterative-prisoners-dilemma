# Improving Agent Strategies in the Iterative Prisoner's Dilemma Simulation

## Problem 1: Unsuitable Learning Algorithm
- The `DecisionTreeClassifier` from scikit-learn is not well-suited for online learning in the Prisoner's Dilemma context.

### Solution: Transition to Incremental Learning Algorithms
- Use incremental learning algorithms like `creme.tree.DecisionTreeClassifier` from the Creme library.

### Code Changes:
- Install Creme library: `pip install creme`
- Import necessary modules: `from creme import tree`
- Replace `DecisionTreeClassifier` with `creme.tree.DecisionTreeClassifier` in `DecisionTreeAgent` and `AdaptiveAgent` classes
- Modify `decide` and `update_history` methods to use `predict_one` and `fit_one` methods of Creme classifier

## Problem 2: Limited Exploitation of Opponent's History
- Agents do not fully utilize the rich history of interactions with opponents to inform decision-making.

### Solution: Implement Custom Decision-Making Logic
- Analyze patterns in opponent's behavior, such as sequences of defections and cooperations, to make more informed decisions.
- Uses recency bias which is expected in real-life, regardless of overarching strategy, the most recent decisions made by others tends to affect our decisions.

### Code Changes:
- Add `analyze_opponent_history` method to agent classes to identify patterns in opponent's history
- Modify `decide` method to use the output of `analyze_opponent_history` for decision-making

## Problem 3: Static Cooperation Threshold in ProbabilisticAgent
- The fixed cooperation probability threshold of 0.6 limits the exploration of different strategic behaviors.

### Solution: Make the Threshold Adjustable
- Parameterize the cooperation probability threshold to allow for experimentation with different strategies.

### Code Changes:
- Modify `ProbabilisticAgent` class to accept a `threshold` parameter in its constructor
- Update `decide` method to use the `threshold` parameter when comparing cooperation probability

## Problem 4: Simplistic Decision-Making in HeuristicAgent
- The `HeuristicAgent` uses a simplistic count of opponent's defections, ignoring the significance of action sequences.

### Solution: Refine the Strategy to Consider Action Sequences
- Analyze the sequence of opponent's actions to identify patterns and make more informed decisions.

### Code Changes:
- Modify `HeuristicAgent` class to store opponent's history as a list of actions
- Implement `analyze_action_sequence` method to identify patterns in the sequence of actions
- Update `decide` method to use the output of `analyze_action_sequence` for decision-making
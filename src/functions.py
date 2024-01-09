from sklearn.tree import DecisionTreeClassifier

# Example function to create a training dataset
def create_training_data(agent_history):
    # Transform the history into a format suitable for training the decision tree
    # This is a simplified example; you'd want to use more sophisticated feature engineering
    features = []
    labels = []
    for i in range(1, len(agent_history)):
        features.append(agent_history[i-1])  # Previous round
        labels.append(agent_history[i][0])   # Agent's action in the current round
    return features, labels

# Training the decision tree
# Assuming `agent_history` is available from the simulation
features, labels = create_training_data(agent_history)
decision_tree_model = DecisionTreeClassifier()
decision_tree_model.fit(features, labels)



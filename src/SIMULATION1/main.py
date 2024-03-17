from prisoner_dilemma.agents import Agent, HeuristicAgent, ProbabilisticAgent, DecisionTreeAgent, AdaptiveAgent
from prisoner_dilemma.simulation import Simulation

# Simulation 1
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
simulation.analyze_results()
simulation.results_df.to_csv("results.csv",index=False)
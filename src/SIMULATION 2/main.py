from agent import Agent, HeuristicAgent, ProbabilisticAgent, DecisionTreeAgent, AdaptiveAgent
from simulation import Simulation
from analysis import plot_results

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


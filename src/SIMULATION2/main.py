from agents import Agent, HeuristicAgent, ProbabilisticAgent, IncremDecisionTreeAgent, PunisherAgent, QLearningAgent
from simulation import Simulation

# Simulation 1
agents = [
    Agent(name="Cooper", strategy="always-cooperate"), 
    Agent(name="Devin", strategy="always-defect"), 
    Agent(name="Randy", strategy="random"), 
    Agent(name="Titi", strategy="tit-for-tat"),
    Agent(name="Tata", strategy="tit-for-2-tat"),
    ProbabilisticAgent(name="Prosper"),
    HeuristicAgent(name='Eureka'),
    PunisherAgent(name='FrankCastle'),
    IncremDecisionTreeAgent(name="Destiny"),
    QLearningAgent(name="Quincy")
]

simulation = Simulation(agents)
simulation.run_simulation(5000)


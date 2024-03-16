In the updated simulation, we are introducing significant enhancements to the strategies of both the Probabilistic and Heuristic agents, aiming to increase their adaptability and effectiveness based on the dynamic nature of opponent interactions.

Probabilistic Agent (Prosper): The key improvement involves making the cooperation-defection threshold dynamic, allowing it to adjust based on the agent's performance against individual opponents. This change is designed to enable the agent to adapt its strategy to the emergent reputations of its opponents. In the initial rounds of the previous simulation, agents did not modify their behavior based on the specific actions of their opponents, leading to potential exploitation. By allowing the cooperation threshold to vary from round to round, the Prosper can become more or less cooperative based on its ongoing interactions, promoting a more nuanced and responsive strategy.

NOTE: Prosper cannot predict for sure that its decision will be correct, so, it assuemes. Assume a win if deciding to cooperate and opponent's cooperation probability is high, else assume a loss.
       

Heuristic Agent (Eureka-Castle): Similar to the Prosper (probabilistic), Eureka (Heuristic Agent) will also use a dynamic threshold in the updated simulation. However, rather than adjusting based on performance metrics, this threshold will change based on the proportion of defections observed in the opponent's recent history. The initial benchmark for this proportion is set at 60%, rather than a fixed count of 2. Unlike Prosper, however, the only thing that changes from round to round is the proportion of defections (based on observed tendencies of its opponents), the initial threshold to benchmark against (60%) will remain the same.

Eureka will also look at patterns that can override the above. If the opponent defected against it twice after cooperating, this might suggest exploitation and it will immediately punish by defecting (Simulation rules suggest a win/neutral outcome here). On the other hand, if it opponent cooperates twice in a row after defecting, it may suggest an attempt at goodwill and Eureka will choose to cooperate.

Finally, one new change is the addition of the Castle Personality (The Punisher). Once she detects defection 3 times in a row, she will punish that agent for the next 5 rounds.


Non-Adaptive Strategies:
Always Defect (Devin): This was almost a winning strategy. In static scenarios where agents do not adapt, it could be an effective strategy in the long run. In the testing phase, Devin outperformed drastically, but the law of large numbers alongside adaptive agents caught up to it. If the simulation had continued for much longer, I suspect a plateau in the rate of score increase.
Always Cooperate (Cooper): Cooper was exploited by everyone that couldd (Devin and Destiny mostly)
Random Agent (Randy): No strategy, poor performance as expected.

These agents serve as important baselines to evaluate the performance of other strategies. The will continue to be benchmarks to measure the effectiveness of more advanced agents in promoting cooperation or exploiting simple strategies. But for Randy, I want to explore letting the random strategy benefit from the basic recency effect as well. (reference the `analyze_opponent_history` method in the Agent class).
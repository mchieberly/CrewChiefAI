# CrewChiefAI
#### By Malachi Eberly

Reinforcement Learning project to create an agent that can make pit stop decisions during a NASCAR race based on current conditions.

## Race Simulation Details
The simulated race has been simplified to help generalize the model. Complexity will be added later to make the model less generalzed and to consider more variables.

### Goal: Minimum Time to Complete All Laps
Number of laps: 400
Full tank of fuel lasts: 100 laps (18 gallons)
Set of four tires lasts: 100 laps

Lap time equation: y = 0.95x + 22.5  
  -> y = The lap time in seconds  
  -> x = The number of laps since new tires

Note: If the most recent pit stop was 2 tires, x is calculated with the following:

x = (0.5 * a) + (0.5 * b)  
  -> a = The number of laps since replacing the older tires  
  -> b = The number of laps since replacing the newer tires

### Pit stop times:

#### Caution:
Fuel and No Tires: y = 0.1x + 2  
  -> y = The number of seconds the pit stop takes  
  -> x = The number of laps since completely refueling  
Two Tires: 7 seconds  
Four Tires: 12 seconds

#### Green Flag:
Fuel and No Tires: y = 0.1x + 10  
  -> y = The number of seconds the pit stop takes  
  -> x = The number of laps since completely refueling  
Two Tires: 35 seconds  
Four Tires: 40 seconds

Note that green flag pit stops take significantly longer than caution pit stops. This is to account for the fact that pit stops are ideally taken during cautions to minimize risk of losing positions to other drivers. There will be 1-5 randomly placed cautions during the race, and the laps of the cautions will be unknown to the agent.

import gymnasium
from gymnasium import spaces
import numpy as np
from src.car import Car

class RaceEnv(gymnasium.Env):
    metadata = {"render_modes": ["human"], "render_fps": 4}

    def __init__(self):
        super(RaceEnv, self).__init__()
        
        self.car = Car()

        # Define action space: 5 discrete actions
        self.action_space = spaces.Discrete(5)

        # Initial state
        self.state = np.zeros(6)
        self.state[5] = Car.NUM_LAPS

    def step(self, action):
        # Apply the action to the environment
        lap_time = self.car.get_lap_time()
        self.state[0] = lap_time
        self.state[1] = self.car.current_lap

        if action == 0:  # race a lap
            self.car.race_lap()
        elif action == 1:  # Pit stop for only fuel
            self.car.fuel_no_tires()
            self.state[1] = self.car.current_lap
        elif action == 2:  # left tires pit stop
            self.car.change_left_tires()
            self.state[2] = self.car.current_lap
        elif action == 3:  # right tires pit stop
            self.car.change_right_tires()
            self.state[2] = self.car.current_lap
        elif action == 4:  # 4-tire pit stop
            self.car.change_four_tires()
            self.state[2] = self.car.current_lap
            self.state[3] = self.car.current_lap

        truncated = self.car.race_over()
        terminated = self.car.race_failed()
        
        if terminated:
            reward = -1000  # Huge negative reward for failure
        else:
            reward = -((lap_time - 23) / 5)  # Normalize lap time reward

        return self.state, reward, terminated, truncated, {}

    def reset(self):
        self.car = Car()
        self.state = np.zeros(6)
        self.state[5] = Car.NUM_LAPS
        return self.state

    def render(self, mode='human', close=False):
        print(f"Lap: {self.car.current_lap}, State: {self.state}")

# # Example usage
# env = RaceEnv()
# state = env.reset()
# terminated = False
# truncated = False
# while not (terminated or truncated):

#     need_fuel = (env.car.current_lap - env.car.last_lap_fueled) == 95
#     need_left_tires = (env.car.current_lap - env.car.last_lap_left_tires) == 95
#     need_right_tires = (env.car.current_lap - env.car.last_lap_right_tires) == 95

#     if need_left_tires and need_right_tires:
#         action = 4
#     elif need_left_tires:
#         action = 2
#     elif need_right_tires:
#         action = 3
#     elif need_fuel:
#         action = 1
#     else:
#         action = 0

#     state, reward, terminated, truncated, info = env.step(action)
#     env.render()

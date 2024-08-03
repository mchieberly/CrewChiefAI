import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'

# Imports
import random, datetime
from pathlib import Path

from src.metrics import MetricLogger
from src.agent import CrewChief
from src.race_env import RaceEnv

def format_time(seconds):
    if seconds <= 60:
        return f"{round(seconds, 2)} seconds"
    minutes, seconds = divmod(seconds, 60)
    if minutes <= 60:
        return f"{int(minutes)} minutes and {round(seconds, 2)} seconds"
    hours, minutes = divmod(minutes, 60)
    return f"{int(hours)} hours, {int(minutes)} minutes, and {round(seconds, 2)} seconds"

def main():
    # Initialize environment
    env = RaceEnv()

    # Reset
    env.reset()

    save_dir = Path('checkpoints') / datetime.datetime.now().strftime('%Y-%m-%dT%H-%M-%S')
    save_dir.mkdir(parents=True)

    checkpoint = None 
    # Initialize Crew Chief agent
    crew_chief = CrewChief(state_dim=6, action_dim=env.action_space.n, save_dir=save_dir, checkpoint=checkpoint)

    logger = MetricLogger(save_dir)

    # Number of episodes
    episodes = 50000

    for e in range(episodes):

        # Reset the state
        state = env.reset()
        
        # Race time list
        race_time = []

        while True:
            # Choose an action based on the state
            action = crew_chief.act(state)

            # Step through the environment
            next_state, reward, terminated, truncated, info = env.step(action)

            # Save the results of that step in memory buffer
            crew_chief.cache(state, next_state, action, reward, terminated, truncated)

            # Learn from memory buffer
            q, loss = crew_chief.learn()

            # Log the step
            logger.log_step(reward, loss, q)

            # Move to the next state
            state = next_state

            # Break if we ran out of fuel, lost tires, or the race is over
            if terminated or truncated:
                if truncated:
                    race_time.append(env.car.current_time)
                break

        # Log the episode
        logger.log_episode()
        
        if e % 20 == 0:
            logger.record(
                episode=e,
                epsilon=crew_chief.exploration_rate,
                step=crew_chief.curr_step
            )
            # Print the race time
            print(f"Average race time: {format_time(sum(race_time) / len(race_time))}")

if __name__ == "__main__":
    main()

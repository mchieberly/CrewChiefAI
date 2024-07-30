class RaceEnv(gym.Env):
    metadata = {"render_modes": ["human"], "render_fps": 4}

    def __init__(self, render_mode = None):
        self.race = Race()
        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Box(low=0, high=5, shape=(54,), dtype=np.int64)

        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode

    def _get_obs(self):
        return self.race.get_observation()

    def _get_info(self):
        return self.race.get_info()

    def step(self, action):
        obs, reward, terminated, truncated, info = self.race.step(action)
        if self.render_mode == "human":
            self._render_frame()
        return obs, reward, terminated, truncated, info

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        if self.render_mode == "human":
            self._render_frame()
        return self.race.reset(), self._get_info()

    def render(self, mode='human'):
        if mode == 'human':
            return self._render_frame()
        
    def _render_frame(self):
        # TODO: Implement 3D render vs print render
        print(self.race)

    def close(self):
        return super().close()

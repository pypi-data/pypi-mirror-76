import numpy as np
import gym.spaces as spaces
from gym import ObservationWrapper


class FlatEnv(ObservationWrapper):
    r"""Observation wrapper that flattens the observation."""

    def __init__(self, env):
        super().__init__(env)

        dim = spaces.flatdim(env.observation_space)
        self.observation_space = spaces.Box(low=-float('inf'), high=float('inf'), shape=(dim,), dtype=np.float32)

    def observation(self, observation):
        return spaces.flatten(self.env.observation_space, observation)

from .dummy_vec_env import DummyVecEnv
from .subproc_vec_env import SubprocVecEnv


def make_env(env_id, seed, *wrappers):
    def _thunk():
        import gym

        env = gym.make(env_id)
        for w in wrappers:
            env = w(env)
        env.seed(seed)
        return env

    return _thunk

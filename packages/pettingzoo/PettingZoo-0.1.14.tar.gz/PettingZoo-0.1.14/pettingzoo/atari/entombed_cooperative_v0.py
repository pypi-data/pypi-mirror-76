from .base_atari_env import BaseAtariEnv, base_env_wrapper_fn


def raw_env(**kwargs):
    return BaseAtariEnv(game="entombed", num_players=2, mode_num=3, **kwargs)


env = base_env_wrapper_fn(raw_env)

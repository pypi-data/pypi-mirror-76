from .base_atari_env import BaseAtariEnv, base_env_wrapper_fn

avaliable_2p_versions = {
    "classic": 4,
    "two_paddles": 10,
    "soccer": 14,
    "foozpong": 19,
    "hockey": 27,
    "handball": 35,
    "volleyball": 39,
    "basketball": 45,
}
avaliable_4p_versions = {
    "classic": 6,
    "two_paddles": 11,
    "soccer": 16,
    "foozpong": 21,
    "hockey": 29,
    "quadrapong": 32,
    "handball": 37,
    "volleyball": 41,
    "basketball": 49,
}


def raw_env(num_players=2, game_version="classic", **kwargs):
    assert num_players == 2 or num_players == 4
    versions = avaliable_2p_versions if num_players == 2 else avaliable_4p_versions
    assert game_version in versions, f"pong version {game_version} not supported for number of players {num_players}. Avaliable options are {list(versions)}"
    mode = versions[game_version]
    return BaseAtariEnv(game="pong", num_players=num_players, mode_num=mode, **kwargs)


env = base_env_wrapper_fn(raw_env)

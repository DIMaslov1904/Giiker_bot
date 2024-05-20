from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


class SettingsConfig(BaseSettings):
    stickers: tuple[tuple[str, str], tuple[str, str]] = (
        ('X', 'CAACAgIAAxkBAANiZkHMr2KNhEPkI_qzrcnuTCYaIqYAAjZJAAKArhBK1dr1fLtNsWE1BA'),
        ('O', 'CAACAgIAAxkBAANkZkHMs9N82RzQiNNlfV4U82nG1lEAAk1GAAKTaBBKUUO6uV_aT941BA')
    )

    bot_token: SecretStr
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')


config = SettingsConfig()

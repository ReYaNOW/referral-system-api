from typing import Self

from pydantic import PostgresDsn, RedisDsn, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    database_url: PostgresDsn
    redis_url: RedisDsn
    redis_ttl: int = 3600

    secret_key: str
    access_token_expire_minutes: int

    hunterio_api_key: str | None = None

    in_docker: bool = False

    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

    @field_validator('database_url', mode='before')
    @classmethod
    def add_asyncpg_to_url(cls, v: str) -> str:
        return v.replace('postgresql', 'postgresql+asyncpg')

    @model_validator(mode='after')
    def convert_urls_in_docker(self) -> Self:
        if not self.in_docker:
            return self

        db_values = self.database_url.hosts()[0]
        db_host = db_values.get('host')
        db_port = db_values.get('port')

        if db_host:
            self.database_url = PostgresDsn(
                str(self.database_url)
                .replace(db_host, 'db')
                .replace(str(db_port), '5432')
            )

        redis_host = self.redis_url.host
        if redis_host:
            self.redis_url = RedisDsn(
                str(self.redis_url).replace(redis_host, 'redis')
            )

        return self


config = Config()

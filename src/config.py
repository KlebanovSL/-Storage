import functools

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel


class DBSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="DB_",
        env_file=".example.env",
        extra="ignore"
    )

    HOST: str
    PORT: str
    NAME: str
    USER: str
    PASS: str

    @functools.cached_property
    def connection_string(self):
        return (
            f"postgresql+asyncpg://{self.USER}:{self.PASS}@{self.HOST}:"
            f"{self.PORT}/{self.NAME}"
        )


class Settings(BaseModel):
    DB: DBSettings = DBSettings()


settings = Settings()

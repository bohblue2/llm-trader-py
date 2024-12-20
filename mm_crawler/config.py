import os

from pydantic import PostgresDsn, computed_field
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings


class CrawlerSettings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_SERVER: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    
    ALEMBIC_DB_URL: str

    @computed_field  # type: ignore[prop-decorator]
    @property
    def SQLALCHEMY_DATABASE_URL(self) -> PostgresDsn:
        return MultiHostUrl.build(
            scheme="postgresql",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )
    
    def __post_init__(self):
        def display_all_fields(self):
            """
            Display all configuration values.
            """
            for field_name, field_value in self.__dict__.items():
                print(f"{field_name}: {field_value}")
        display_all_fields(self)
    
    class Config:
        env_file = (
            ".env.dev.crawler" if os.getenv("ENVIRONMENT", "DEV") == 'DEV' else
            ".env.stage.crawler" if os.getenv("ENVIRONMENT", "STAGE") == 'STAGE' else
            ".env.prod.crawler" if os.getenv("ENVIRONMENT", "PROD") == 'PROD' else
            ".env.crawler"
        )
        env_file_encoding = "utf-8"

settings = CrawlerSettings() # type: ignore
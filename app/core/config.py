from typing import Any, Optional
from dotenv import load_dotenv

from pydantic import field_validator
from pydantic_settings import BaseSettings

load_dotenv()

class Config(BaseSettings):
    fastapi_app_name:str = "mpymes lite"
    debug:bool = False
    database_username:str
    database_password:str
    database_name:str
    database_host:str = None
    database_port:Optional[int] = None

    @property
    def database_url(self):
        if self.database_host:
            return f"postgresql://{self.database_username}:{self.database_password}@{self.database_host}:{self.database_port}/{self.database_name}?sslmode=require"
        else:
            return f"sqlite:///./temp/{self.database_name}"

    @field_validator("database_port", mode="before")
    @classmethod
    def assemble_database_port(cls, value:Any) -> Any:
        if value == "":
            return None
        return value

config = Config()

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Config(BaseSettings):
    fastapi_app_name:str
    debug:bool = False
    database_username:str
    database_password:str
    database_name:str
    database_host:str = None
    database_port:int = None

    @property
    def database_url(self):
        if self.database_host:
            return f"postgresql://{self.database_username}:{self.database_password}@{self.database_host}:{self.database_port}/{self.database_name}?sslmode=require"
        else:
            return f"sqlite:///./{self.database_name}"

config = Config()

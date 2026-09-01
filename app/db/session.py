from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import config

engine = create_engine(config.database_url, connect_args={"check_same_thread":False})
databse_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Use an absolute path in your home directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Or simply:
# DATABASE_URL = "sqlite://///home/citrixlabph/aml_pa.db"
DATABASE_URL = "sqlite:///./data/aml_pa.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
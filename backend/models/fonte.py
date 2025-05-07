from sqlalchemy import create_engine, Column, Float, TIMESTAMP, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://postgres:postgres@fonte_db:5432/postgres"

Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

class Data(Base):
    __tablename__ = "data"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(TIMESTAMP, index=True)
    wind_speed = Column(Float)
    power = Column(Float)
    ambient_temperature = Column(Float)

def init_db():
    Base.metadata.create_all(bind=engine)

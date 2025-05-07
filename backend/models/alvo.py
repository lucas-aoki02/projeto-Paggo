from sqlalchemy import create_engine, Column, Integer, String, Float, TIMESTAMP, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

DATABASE_URL = "postgresql://postgres:postgres@alvo_db:5432/postgres"

Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

class Signal(Base):
    __tablename__ = "signal"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    timestamp = Column(TIMESTAMP, index=True)
    signal_id = Column(Integer)
    value = Column(Float)

def init_db():
    Base.metadata.create_all(bind=engine)

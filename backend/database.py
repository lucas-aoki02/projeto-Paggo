from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.config import settings
from sqlalchemy.orm import declarative_base

print(f"DATABASE_URL_FONTE em database.py: {settings.DATABASE_URL_FONTE}")
DATABASE_URL_FONTE = settings.DATABASE_URL_FONTE
engine_fonte = create_engine(DATABASE_URL_FONTE)
FonteSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_fonte)

DATABASE_URL_ALVO = settings.TARGET_DATABASE_URL_ALVO
engine_alvo = create_engine(DATABASE_URL_ALVO)
AlvoSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_alvo)

Base = declarative_base()

# Função para obter uma sessão do banco de dados fonte
def get_db_fonte():
    db = FonteSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Função para obter uma sessão do banco de dados alvo
def get_db_alvo():
    db = AlvoSessionLocal()
    try:
        yield db
    finally:
        db.close()
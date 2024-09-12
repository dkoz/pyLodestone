from sqlalchemy import create_engine, Column, String, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./data/ffxivdata.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Character(Base):
    __tablename__ = "characters"
    char_id = Column(String, primary_key=True, index=True)
    data = Column(JSON)

class FreeCompany(Base):
    __tablename__ = "freecompanies"
    fc_id = Column(String, primary_key=True, index=True)
    data = Column(JSON)

class CharacterSearchResult(Base):
    __tablename__ = "character_ids"
    name = Column(String, primary_key=True, index=True)
    data = Column(JSON)

Base.metadata.create_all(bind=engine)

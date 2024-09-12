import time
from sqlalchemy.orm import Session
from utils.models import SessionLocal, Character, FreeCompany, CharacterSearchResult

def cleanup_database():
    db: Session = SessionLocal()
    try:
        db.query(Character).delete()
        db.query(FreeCompany).delete()
        db.query(CharacterSearchResult).delete()
        db.commit()
    finally:
        db.close()

def run_cleanup():
    while True:
        cleanup_database()
        time.sleep(3600)

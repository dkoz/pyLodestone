from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from utils.models import SessionLocal, Character, FreeCompany, CharacterSearchResult
from utils.cleanup import run_cleanup
from lodestone.character import Profile
from lodestone.freecompany import FreeCompany as FCModule
from lodestone.utility import SearchCharacterID, SearchCharacterServer
import utils.settings as settings
import threading
import os
import json
from pathlib import Path

app = FastAPI()

# ITems API
app.mount("/images", StaticFiles(directory="images"), name="images")

items_file = Path(os.path.join('gamedata', 'items.json'))
with items_file.open('r', encoding='utf-8') as f:
    items_data = json.load(f)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def verify_api_key(authorization: str = Header(...)):
    if authorization != f"Bearer {settings.apikey}":
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return authorization

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.get("/character/id/{char_id}", dependencies=[Depends(verify_api_key)])
async def get_character(char_id: str, db: Session = Depends(get_db)):
    db_character = db.query(Character).filter(Character.char_id == char_id).first()
    if db_character:
        return db_character.data
    profile = Profile(char_id, retrieve_data=True)
    char_data = profile.to_json_dict()
    db.add(Character(char_id=char_id, data=char_data))
    db.commit()
    return char_data

@app.get("/freecompany/id/{fc_id}", dependencies=[Depends(verify_api_key)])
async def get_freecompany(fc_id: str, db: Session = Depends(get_db)):
    db_fc = db.query(FreeCompany).filter(FreeCompany.fc_id == fc_id).first()
    if db_fc:
        return db_fc.data
    fc = FCModule(fc_id, retrieve_data=True)
    fc_data = {
        "name": fc.name,
        "tag": fc.tag,
        "members": fc.members
    }
    db.add(FreeCompany(fc_id=fc_id, data=fc_data))
    db.commit()
    return fc_data

@app.get("/search/id/{character_name}", dependencies=[Depends(verify_api_key)])
async def search_character_id(character_name: str, db: Session = Depends(get_db)):
    db_search = db.query(CharacterSearchResult).filter(CharacterSearchResult.name == character_name).first()
    if db_search:
        return db_search.data
    results = SearchCharacterID(character_name)
    if results:
        db.add(CharacterSearchResult(name=character_name, data=results))
        db.commit()
        return results
    else:
        raise HTTPException(status_code=404, detail="No characters found")

@app.get("/character/{character_name}/{server_name}", dependencies=[Depends(verify_api_key)])
async def search_character_server(character_name: str, server_name: str, db: Session = Depends(get_db)):
    character = SearchCharacterServer(character_name, server_name)
    if character:
        char_id = character['character_id']
        db_character = db.query(Character).filter(Character.char_id == char_id).first()
        if db_character:
            return db_character.data

        profile = Profile(char_id, retrieve_data=True)
        char_data = profile.to_json_dict()
        db.add(Character(char_id=char_id, data=char_data))
        db.commit()
        return char_data
    else:
        raise HTTPException(status_code=404, detail="Character not found on specified server")
    
# ffxivclock data pulled from their github
@app.get("/items/resources/{identifier}", dependencies=[Depends(verify_api_key)])
async def get_item(identifier: str):
    for item in items_data['items']:
        if item['id'] == identifier or item['name'].lower() == identifier.lower():
            item['imageUrl'] = f"/images/ffxiv/{item['imageUrl']}"
            return item
    raise HTTPException(status_code=404, detail="Item not found")

# cleans up the database cache
threading.Thread(target=run_cleanup, daemon=True).start()
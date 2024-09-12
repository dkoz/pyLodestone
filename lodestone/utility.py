import requests
from bs4 import BeautifulSoup

def SearchCharacterID(character_name: str):
    url = f"https://na.finalfantasyxiv.com/lodestone/character/?all_search=&search_type=character&q={character_name}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    entries = soup.find_all('div', class_='entry')
    characters = []

    for entry in entries:
        link = entry.find('a', class_='entry__link')
        if link and 'href' in link.attrs:
            character_id = link['href'].split('/')[-2]
            character_name = entry.find('p', class_='entry__name').text.strip()
            world = entry.find('p', class_='entry__world').text.strip().replace(' [', ' - ').replace(']', '')

            characters.append({
                'character_id': character_id,
                'name': character_name,
                'world': world
            })

    return characters

def SearchCharacterServer(character_name: str, server_name: str):
    url = f"https://na.finalfantasyxiv.com/lodestone/character/?all_search=&search_type=character&q={character_name}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    entries = soup.find_all('div', class_='entry')
    characters = []

    for entry in entries:
        link = entry.find('a', class_='entry__link')
        if link and 'href' in link.attrs:
            character_id = link['href'].split('/')[-2]
            name = entry.find('p', class_='entry__name').text.strip()
            world = entry.find('p', class_='entry__world').text.strip().replace(' [', ' - ').replace(']', '')
            
            # Filter by server
            if server_name.lower() in world.lower():
                return {'character_id': character_id, 'name': name, 'world': world}
    return None

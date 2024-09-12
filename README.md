# pyLodestone Scraper
 Python scraper for the FFXIV Lodestone.

 > [!IMPORTANT]  
 > This is still in development and not ready for production use.

## Features
 - Character ID Lookup
 - Freedom Company ID Lookup
 - Cluster ID Lookup
 - Character Name Lookup
 - Data stored in local database
 - Built in documentation
 - API Key Authentication Method

## API Endpoints
 - `/docs`: Displays all the endpoints and a sandbox to run them.
 - `/redoc`: Displays documentation for the API using ReDoc.
 - `/character/{id}`: Fetches character details by ID.
 - `/freecompany/{id}`: Retrieves Free Company details by ID.
 - `/search/id/{character_name}`: Retrieves list of character IDs by name.
 - `/search/character/{character_name}/server/{server_name}`: Fetches character details by name and server.

## Docker Setup
 1. Create your `.env` and set an `API_KEY`.
 2. Build your docker image.
 ```bash
 docker build -t pylodestone-scraper .
 ```
 3. Run your docker container.
 ```bash
 docker run -d -p 8000:8000 -v $(pwd)/data:/app/data --name pylodestone-scraper pylodestone-scraper
 ```

### Credit
 - [cleargelnotes](https://github.com/cleargelnotes) - Writing the logic for the scaper.
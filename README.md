# pyLodestone Scraper
 Python scraper for the FFXIV Lodestone.

 > [!IMPORTANT]  
 > This is still in development and not ready for production use.

## Features
 - Character ID Lookup
 - Freedom Company ID Lookup
 - Cluster ID Lookup
 - Character Name/Server Lookup
 - Item ID/Name Lookup
 - Data stored in local database
 - Built in documentation
 - API Key Authentication Method

## API Endpoints
 - `/docs`: Displays all the endpoints and a sandbox to run them.
 - `/redoc`: Displays documentation for the API using ReDoc.
 - `/health`: Health check for the API.
 - `/character/id/{id}`: Fetches character details by ID.
 - `/freecompany/id/{id}`: Retrieves Free Company details by ID.
 - `/search/id/{character_name}`: Retrieves list of character IDs by name.
 - `/character/{character_name}/{server_name}`: Fetches character details by name and server.
 - `/items/{identifier}`: Search for an item by ID or name.

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
 - [cleargelnotes](https://github.com/cleargelnotes)
 - [ffxivclock-data](https://github.com/9001-Solutions/ffxivclock-data)
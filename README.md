# City-Temperature Management API

This is the Temperature Management API. This project provides necessary set of endpoints to handle changes of temperature in requested cities.

## Features

- FastAPI, SQAlchemy, asyncio, alembic and pydentic as main technologies.
- Full CRUD /cities/ operations.
- GET /temperatures/ endpoint.
- POST /temperatures/update/ endpoint to fetch temperatures for all cities from external API.
- Swagger documentation.
- API Pagination.

## Instalation (Local)


1. **Clone the repository**
   ```sh
   git clone https://github.com/panicua/py-fastapi-city-temperature-management-api.git
   cd py-fastapi-city-temperature-management-api
   ```
   
2. Create and activate **venv** (bash):
   ```sh
   python -m venv venv
   source venv/Scripts/activate
   ```
   
    Windows (Command Prompt)
   ```sh
   python -m venv venv
   venv\Scripts\activate
   ```
   
   Mac / Linux (Unix like systems)
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```
   
3. Create an `.env` file in the root of the project directory. You can use the `.env.example` file as a template
   ```sh
   cp .env.example .env
   ```

4. Install **requirements.txt** to your local **venv**:
   ```sh
   pip install -r requirements.txt
   ```
   
5. Run migrations:
    ```sh
    alembic upgrade head
    ```
6. Start the server:
   ```sh
   fastapi run main.py --reload
   ```
   
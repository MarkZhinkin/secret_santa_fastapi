### ❄❄❄ 🎅 Secret Santa API ❄❄❄

[![N|Solid](https://media.istockphoto.com/vectors/funny-santa-dabbing-quirky-cartoon-comic-character-vector-id1077860784?k=20&m=1077860784&s=612x612&w=0&h=zbuqOKsuCxaL3-8WAuse-lSaymjEqiRiBSfVGVqh4fA=)](https://en.wikipedia.org/wiki/Secret_Santa)

This project show how you can use [FastApi](https://fastapi.tiangolo.com/)
for create simple web-application "Secret Santa" for you team.

#### Requirements
1. [Python 3.8](https://www.python.org/downloads/release/python-380/)
2. [FastApi](https://fastapi.tiangolo.com/)
3. [Fastapi-users](https://github.com/fastapi-users/fastapi-users) - 
include base features for working with users.  
4. [uvicorn](https://www.uvicorn.org/) -
 helper for starting async web servers.
5. [Sendgrid](https://sendgrid.com/) -
 mail postman. 
6. [poetry](https://python-poetry.org/) - 
packages and virtual environment manager. 
7. [alembic](https://alembic.sqlalchemy.org/en/latest/) -
 database versions manager.

#### Features 
- registration and authorization by email or login; 
- verification by email
- personal user cabinet;
- dedicated administrator cabinet. 

#### Usage  
- download project
- add environment: `poetry install`
- copy `cp .env.example .env` and fill .env file
- add tables to database: `poetry run alembic upgrade head`
- run `main.py` file

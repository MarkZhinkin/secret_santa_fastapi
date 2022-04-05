### ❄❄❄ 🎅 Secret Santa API ❄❄❄

[![N|Solid](https://media.istockphoto.com/vectors/funny-santa-dabbing-quirky-cartoon-comic-character-vector-id1077860784?k=20&m=1077860784&s=612x612&w=0&h=zbuqOKsuCxaL3-8WAuse-lSaymjEqiRiBSfVGVqh4fA=)](https://en.wikipedia.org/wiki/Secret_Santa)

This project show how you can use [FastApi](https://fastapi.tiangolo.com/)
for create simple web-application "Secret Santa" for you team.

#### Requirements
1. [Python 3.8](https://www.python.org/downloads/release/python-380/)
2. [Node 12](https://nodejs.org/es/blog/release/v12.13.0/)
3. [FastApi](https://fastapi.tiangolo.com/)
4. [Fastapi-users](https://github.com/fastapi-users/fastapi-users) - 
include base features for working with users.  
5. [uvicorn](https://www.uvicorn.org/) -
 helper for starting async web servers.
6. [Sendgrid](https://sendgrid.com/) -
 mail postman. 
7. [poetry](https://python-poetry.org/) - 
packages and virtual environment manager. 
8. [alembic](https://alembic.sqlalchemy.org/en/latest/) -
 database versions manager.
9. [pm2](https://pm2.keymetrics.io/) - packages manager.

#### Features 
- registration and authorization by email or login; 
- verification by email
- personal user cabinet;
- dedicated administrator cabinet. 

#### Usage  
- download project
- add environments: `poetry install`, `npm ci`
- copy `cp .env.example .env` and fill .env file
- add tables to database: `poetry run alembic upgrade head`
- start application by command `pm2 start pm2-app.config.js`

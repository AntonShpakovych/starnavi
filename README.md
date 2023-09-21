# StarNavi Challenge



## To run the api should be executed
```shell
#
git clone https://github.com/AntonShpakovych/starnavi
#
cd starnavi
#
create .env file with variables example provided in .env.sample
#
docker compose up --build
#
127.0.0.1/api/v1/doc/swagger/ - all endpoints we have
#
```
## To test the api you should run a bot
```shell
INFO: Before starting the bot, the api must also be running
#
python -m venv venv
#
venv\Scripts\activate
#
pip install -r requirements_bot.txt
#
cd bot
#
python main.py (after starting the bot, a folder will be created in which the results will be)
#
```
## Basic Features
    - JWT Authentication
    - Crud for Post, User
    - analytics about how many likes was made
    - user activity an endpoint which will show when user was login
      last time and when he mades a last request to the service.
    - containerization api and db
    - Bot: A bot that demonstrates the operation of the API in the form of file generation


### Presence endpoints:
    api/v1/doc/swagger/

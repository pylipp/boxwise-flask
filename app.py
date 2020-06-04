from flask import Flask
from dotenv import load_dotenv
import os
# flask-peewee bindings
from flask_peewee.db import Database


load_dotenv()

AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
API_AUDIENCE = os.getenv('AUTH0_AUDIENCE')
ALGORITHMS = ["RS256"]

app = Flask(__name__)

app.config['DATABASE'] = {
    "name": os.getenv("MYSQL_DB"),
    "engine": "peewee.MySQLDatabase",
    "user": os.getenv('MYSQL_USER'),
    "host": os.getenv('MYSQL_HOST'),
    "password": os.getenv('MYSQL_PASSWORD'),
    # int, otherwise: TypeError: %d format: a number is required, not str from
    # pymysql.connections
    "port": int(os.getenv('MYSQL_PORT', 0)),
}


mysql = Database(app)


def create_tables():
    Person.create_table()
    Camp.create_table()
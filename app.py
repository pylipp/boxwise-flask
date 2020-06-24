import os

from dotenv import load_dotenv
from flask import Flask
from peewee import *
from playhouse.db_url import connect

load_dotenv()

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
API_AUDIENCE = os.getenv("AUTH0_AUDIENCE")
ALGORITHMS = ["RS256"]

app = Flask(__name__)

# load data for database connection
db_user = os.getenv("MYSQL_USER")
db_password = os.getenv("MYSQL_PASSWORD")
db_name = os.getenv("MYSQL_DB")
db_host = os.getenv("MYSQL_HOST")
# int, otherwise: TypeError: %d format: a number is required, not str from
# pymysql.connections
db_port = int(os.getenv("MYSQL_PORT", 0))
cloud_sql_connection_name = os.getenv("CLOUD_SQL_CONNECTION_NAME", False)

if cloud_sql_connection_name:
    mysql = connect(
        "mysql://{}:{}@/{}?unix_socket=/cloudsql/{}".format(
            db_user, db_password, db_name, cloud_sql_connection_name
        )
    )
else:
    mysql = connect(
        "mysql://{}:{}@{}:{}/{}".format(db_user, db_password, db_host, db_port, db_name)
    )

# This hook ensures that a connection is opened to handle any queries
# generated by the request.
@app.before_request
def _db_connect():
    mysql.connect()


# This hook ensures that the connection is closed when we've finished
# processing the request.
@app.teardown_request
def _db_close(exc):
    if not mysql.is_closed():
        mysql.close()

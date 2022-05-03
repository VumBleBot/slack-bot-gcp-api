import os

import sqlalchemy
from sqlalchemy import engine
from google.cloud.sql.connector import connector

db_user = os.environ["DB_USER"]
db_pass = os.environ["DB_PASS"]
db_name = os.environ["DB_NAME"]
db_host = os.environ["DB_HOST"]
db_driver = os.environ.get("DB_DRIVER", "pymysql")

db_socket_dir = os.environ.get("DB_SOCKET_DIR", "/cloudsql")
instance_connection_name = os.environ["INSTANCE_CONNECTION_NAME"]


def getconn():
    return connector.connect(
        instance_connection_name, db_driver, user=db_user, password=db_pass, db=db_name
    )


db_config = {
    "pool_size": 5,
    "max_overflow": 2,
    "pool_timeout": 30,
    "pool_recycle": 1800,
}


cloud_url = engine.url.URL.create(
    drivername="mysql+pymysql",
    username=db_user,
    password=db_pass,
    host=db_host,
    port=3306,
    database=db_name,
)

print("cloud_url:", cloud_url)

#  sql_engine = sqlalchemy.create_engine(
#      cloud_url,
#      **db_config,
#  )


sql_engine = sqlalchemy.create_engine("mysql+pymysql://", creator=getconn)

query = "select * from slack_bots;"

with sql_engine.begin() as conn:
    print(conn.execute(query).fetchall())

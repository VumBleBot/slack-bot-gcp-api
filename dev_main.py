import json
import logging
import os

import sqlalchemy
from sqlalchemy import engine
from flask import Flask, request
from google.cloud.sql.connector import connector
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler
from slack_bolt.oauth.oauth_settings import OAuthSettings
from slack_sdk.oauth import installation_store
from slack_sdk.oauth.installation_store.sqlalchemy import SQLAlchemyInstallationStore
from slack_sdk.oauth.state_store.sqlalchemy import SQLAlchemyOAuthStateStore

from utils import BlockTemplates, SongRecommender, SQLAlchemyVumblebotStore

logging.basicConfig(format="%(asctime)s %(message)s", level=logging.DEBUG)
logger = logging.getLogger().setLevel(logging.INFO)

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


# local
sql_engine = sqlalchemy.create_engine("mysql+pymysql://", creator=getconn)

oauth_state_store = SQLAlchemyOAuthStateStore(
    expiration_seconds=120, engine=sql_engine, logger=logger
)
installation_store = SQLAlchemyInstallationStore(
    client_id=os.environ["SLACK_CLIENT_ID"], engine=sql_engine, logger=logger
)

vumblebot_store = SQLAlchemyVumblebotStore(engine=sql_engine, logger=logger)

try:
    sql_engine.execute("select count(*) from slack_bots")
except Exception as e:
    installation_store.metadata.create_all(sql_engine)
    oauth_state_store.metadata.create_all(sql_engine)

oauth_settings = OAuthSettings(
    client_id=os.environ["SLACK_CLIENT_ID"],
    client_secret=os.environ["SLACK_CLIENT_SECRET"],
    state_store=oauth_state_store,
)


# process_before_response must be True when running on FaaS
app = App(
    logger=logger,
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET"),
    installation_store=installation_store,
    oauth_settings=oauth_settings,
    process_before_response=True,
)

song_recommender = SongRecommender()


def handle_challenge(request):
    slack_request = json.loads(request.get("body"))
    response = {"statusCode": 200, "body": slack_request.get("challenge")}
    return response


@app.middleware
def log_request(logger, body, next):
    return next()


@app.command("/onboarding")
def handle_onboarding(ack, body, say, logger):
    ack()

    blocks = BlockTemplates.onboarding()

    say(
        text="text",
        blocks=blocks,
        unfurl_links=False,  # 링크 펼치지 않기
        unfurl_media=False,  # 미디어 펼치지 않기
    )


@app.event("app_home_opened")
def update_home_tab(client, event, logger):
    try:
        client.views_publish(
            user_id=event.get("user"),
            view=BlockTemplates.app_home_opened(),
        )

    except Exception as e:
        logger.error(f"Error publishing home tab: {e}")


@app.action("reco_static_select")
def handle_reco_static_select(ack, body, client, logger):
    """Type: 0(Click)"""
    ack()
    vumblebot_store.save_user_feedback(body, 0)


@app.action("like")
def handle_like(ack, body, client, logger):
    """Type: 1(Like)"""
    ack()
    client.reactions_add(
        channel=body["channel"]["id"],
        timestamp=body["message"]["thread_ts"],
        name="thumbsup",
    )
    vumblebot_store.save_user_feedback(body, 1)


@app.action("dislike")
def handle_dislike(ack, body, client, logger):
    """Type: 2(Dislike)"""
    ack()
    client.reactions_add(
        channel=body["channel"]["id"],
        timestamp=body["message"]["thread_ts"],
        name="bow",
    )

    vumblebot_store.save_user_feedback(body, 2)


@app.event("app_mention")
def handle_app_mentions(ack, body, say, logger):
    ack()

    is_thread = True if "thread_ts" in body.get("event", "") else False

    if is_thread:
        return

    user = song_recommender.recommend_song(body)
    blocks = BlockTemplates.app_mention(user.emotion, user.score, user.contents)

    say(
        text="text",
        blocks=blocks,
        channel=user.channel,
        thread_ts=user.event_ts,
        unfurl_links=False,  # 링크 펼치지 않기
        unfurl_media=False,  # 미디어 펼치지 않기
    )

    vumblebot_store.save_user_input(user)


flask_app = Flask(__name__)
bolt_handler = SlackRequestHandler(app)


@flask_app.route("/slack/install", methods=["GET"])
def install():
    return bolt_handler.handle(request)


@flask_app.route("/slack/oauth_redirect", methods=["GET"])
def oauth_redirect():
    return bolt_handler.handle(request)


@flask_app.route("/slack/events", methods=["POST"])
def handler():
    return bolt_handler.handle(request)


if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))

""" slack-bot impleme, nted with google cloud function
Reference:
    - https://github.com/slackapi/bolt-python/blob/main/examples/google_cloud_functions/main.py
    - https://github.com/slackapi/bolt-python/issues/134
"""
import os
import json
import logging

from slack_bolt import App
from flask import Flask, request
from slack_bolt.adapter.flask import SlackRequestHandler
from slack_bolt.oauth.oauth_settings import OAuthSettings
from slack_sdk.oauth.state_store import FileOAuthStateStore
from slack_sdk.oauth.installation_store import FileInstallationStore

from utils import SongRecommender, BlockTemplates

oauth_settings = OAuthSettings(
    client_id=os.environ["SLACK_CLIENT_ID"],
    client_secret=os.environ["SLACK_CLIENT_SECRET"],
    scopes=["app_mentions:read", "im:history", "chat:write", "links:read"],
    redirect_uri=None,
    install_path="/slack/install",
    redirect_uri_path="/slack/oauth_redirect",
    state_store=FileOAuthStateStore(expiration_seconds=600, base_dir="./data"),
)


# process_before_response must be True when running on FaaS
app = App(
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET"),
    installation_store=FileInstallationStore(base_dir="./data"),
    oauth_settings=oauth_settings,
    process_before_response=True,
)

song_recommender = SongRecommender()
logging.basicConfig(format="%(asctime)s %(message)s", level=logging.DEBUG)


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


# maybe this log used by implicit feedback
@app.action("reco_static_select")
def handle_reco_static_select(ack, body, logger):
    ack()


@app.action("like")
def handle_like(ack, body, logger):
    ack()


@app.action("dislike")
def handle_dislike(ack, body, logger):
    ack()


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
        thread_ts=user.ts,
        unfurl_links=False,  # 링크 펼치지 않기
        unfurl_media=False,  # 미디어 펼치지 않기
    )


flask_app = Flask(__name__)
handler = SlackRequestHandler(app)


@flask_app.route("/slack/install", methods=["GET"])
def install():
    return handler.handle(request)


@flask_app.route("/slack/oauth_redirect", methods=["GET"])
def oauth_redirect():
    return handler.handle(request)


@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)


if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))

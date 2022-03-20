""" slack-bot implemented with google cloud function
Reference:
    - https://github.com/slackapi/bolt-python/blob/main/examples/google_cloud_functions/main.py
"""

import json
import logging

from flask import Flask, request
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler
from song_recommender import SongRecommender


# process_before_response must be True when running on FaaS
app = App(process_before_response=True)
bolt_handler = SlackRequestHandler(app)
song_recommender = SongRecommender()

flask_app = Flask(__name__)

logging.basicConfig(format="%(asctime)s %(message)s", level=logging.DEBUG)


def handle_challenge(request):
    slack_request = json.loads(request.get("body"))
    response = {"statusCode": 200, "body": slack_request.get("challenge")}
    return response


@app.event("static_select-action")
def handle_reco_feedback(body, say, logger):
    logger.info("body:", body)


@app.event("app_mention")
def handle_app_mentions(body, say, logger):
    logger.info("body:", body)
    blocks = song_recommender.recommend_song_test(body)
    say(blocks=blocks)


@flask_app.route("/slack/install", methods=["GET"])
def install():
    return bolt_handler.handle(request)


@flask_app.route("/slack/oauth_redirect", methods=["GET"])
def oauth_redirect():
    return bolt_handler.handle(request)


def handler(*args):
    """
    AWS
        - args is event, context
    CloudFunction
        - args is request
    """
    return bolt_handler.handle(*args)

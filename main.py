""" slack-bot implemented with google cloud function
Reference:
    - https://github.com/slackapi/bolt-python/blob/main/examples/google_cloud_functions/main.py
"""

import json
import logging

from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler

from utils import (
    request_song_info,
    extract_user_input,
    parse_urls_from_page,
    request_youtube_search,
)


# process_before_response must be True when running on FaaS
app = App(process_before_response=True)
bolt_handler = SlackRequestHandler(app)

logging.basicConfig(format="%(asctime)s %(message)s", level=logging.DEBUG)


def handle_challenge(request):
    slack_request = json.loads(request.get("body"))
    response = {"statusCode": 200, "body": slack_request.get("challenge")}
    return response


@app.event("app_mention")
def handle_app_mentions(body, say, logger) -> None:
    logger.info("body:", body)

    user_input = extract_user_input(body)
    artist, song_name = request_song_info(user_input)

    page = request_youtube_search(artist, song_name)
    watch_urls = parse_urls_from_page(page)
    reco_url = watch_urls[0]

    msg_ = f"artist: {artist} song_name: {song_name}, reco_url: {reco_url}"
    say(msg_)


def handler(request):
    return bolt_handler.handle(request)

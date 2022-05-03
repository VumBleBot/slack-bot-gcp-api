import json
import os
import re
from dataclasses import dataclass, field
from typing import List

import requests

from utils.youtube_helper import YoutubeHelper


@dataclass
class User:
    user_id: str
    team_id: str
    event_ts: str
    _input: str
    channel: str
    score: float = 0.0
    emotion: str = ""
    contents: List[dict] = field(default_factory=list)

    def mention(self) -> str:
        return f"<@{self.user_id}>"

    @property
    def input(self) -> str:
        return self._input

    @input.setter
    def input(self, text: str) -> None:
        sub_pattern = r":.+?:|\x0a|\n"
        text = re.sub(sub_pattern, "", text)
        text = " ".join(text.split())
        self._input = text

    @staticmethod
    def parsing(body: dict, app_mention_key: str):
        text = body["event"]["text"]
        text = text.replace(app_mention_key, "")
        user = User(
            user_id=body["event"]["user"],
            team_id=body["team_id"],
            event_ts=body["event"]["event_ts"],
            channel=body["event"]["channel"],
            _input="",
        )
        user.input = text
        return user


class SongRecommender:
    def __init__(self, app_mention_key: str = "<@U02V2GG4GF9>"):
        self._app_mention_key = app_mention_key
        self._headers = {"Content-Type": "application/json; charset=utf-8"}

    def _request_recommendations(self, user: User) -> dict:
        datas = {"user_id": user.user_id, "user_input": user.input}

        res = requests.post(
            os.environ["REQUEST_URL"], headers=self._headers, data=json.dumps(datas)
        )

        return res.json()

    def recommend_song(self, body: dict) -> User:
        user = User.parsing(body, self._app_mention_key)
        recommendations = self._request_recommendations(user)

        user.score = recommendations["emotion_score"]
        user.emotion = recommendations["emotion_label"]

        #  user.contents = asyncio.run(
        #      YoutubeHelper.add_youtube_infos(recommendations["contents"])
        #  )

        user.contents = YoutubeHelper.add_youtube_infos_from_db(
            recommendations["contents"]
        )

        return user

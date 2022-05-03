import os
import asyncio
import json
import re
from typing import List

import aiohttp

path = os.path.abspath(os.path.join(__file__, "..", ".."))

with open(os.path.join(path, "youtube_db.json"), "r") as f:
    youtube_db = json.load(f)


class YoutubeHelper:
    title_limit: int = 25
    watch_url: str = "https://www.youtube.com/watch?v={}"
    search_url: str = "https://www.youtube.com/results?search_query={}+-+{}"

    @classmethod
    async def _parsing(cls, session, url):
        async with session.get(url) as resp:
            page = await resp.text()
            data = re.search(r"var ytInitialData = ({.*?});", page).group(1)
            yt_initial_data = json.loads(data)
            yt_songs_data = yt_initial_data["contents"][
                "twoColumnSearchResultsRenderer"
            ]
            yt_songs_data = yt_songs_data["primaryContents"]["sectionListRenderer"]
            yt_songs_data = yt_songs_data["contents"][0]["itemSectionRenderer"][
                "contents"
            ]

            for song_data in yt_songs_data:
                if "videoRenderer" not in song_data:
                    continue

                video_id = song_data["videoRenderer"]["videoId"]
                title = song_data["videoRenderer"]["title"]["runs"][0]["text"]

                if len(title) > cls.title_limit:
                    title = title[: cls.title_limit] + " ..."

                url = cls.watch_url.format(video_id)

                return url, title

    @classmethod
    async def add_youtube_infos(cls, contents: List[dict], topk=5) -> List[dict]:
        async with aiohttp.ClientSession() as session:
            new_contents = []
            tasks = []

            for content in contents[:topk]:
                url = cls.search_url.format(content["artist"], content["song_name"])
                tasks.append(asyncio.ensure_future(cls._parsing(session, url)))

            # 순서대로 스케쥴링됨
            result = await asyncio.gather(*tasks)

            for i, content in enumerate(contents[:topk]):
                content["youtube_url"] = result[i][0]
                content["youtube_title"] = result[i][1]
                new_contents.append(content)

        return new_contents

    @classmethod
    def add_youtube_infos_from_db(cls, contents: List[dict], topk=5) -> List[dict]:
        new_contents = []
        visited = set()

        for content in contents:

            if len(new_contents) >= topk:
                break

            search_key = f"{content['artist']}-{content['song_name']}"
            youtube_url = youtube_db[search_key]["youtube_url"]
            youtube_title = youtube_db[search_key]["youtube_title"]

            if len(youtube_title) > cls.title_limit:
                youtube_title = youtube_title[: cls.title_limit] + " ..."

            if youtube_url in visited:
                continue

            visited.add(youtube_url)

            content["youtube_url"] = youtube_url
            content["youtube_title"] = youtube_title

            new_contents.append(content)

        return new_contents

import re
import json
import aiohttp
import asyncio
import requests

from typing import List


class YoutubeHelper:
    title_limit: int = 25
    watch_url: str = "https://www.youtube.com/watch?v={}"
    search_url: str = "https://www.youtube.com/results?search_query={}+-+{}"

    @classmethod
    def _parsing(cls, page: str) -> dict:
        pattern = "var ytInitialData = ([^;]*);"
        yt_initial_data = json.loads(re.findall(pattern, page)[0])
        yt_songs_data = yt_initial_data["contents"]["twoColumnSearchResultsRenderer"]
        yt_songs_data = yt_songs_data["primaryContents"]["sectionListRenderer"]
        yt_songs_data = yt_songs_data["contents"][0]["itemSectionRenderer"]["contents"]

        song_infos = {}

        for song_data in yt_songs_data:
            try:
                video_id = song_data["videoRenderer"]["videoId"]
                title = song_data["videoRenderer"]["title"]["runs"][0]["text"]
                url = cls.watch_url.format(video_id)

                if len(title) > cls.title_limit:
                    title = title[: cls.title_limit] + " ..."

                song_infos["youtube_url"] = url
                song_infos["youtube_title"] = title
                break
            except KeyError:
                continue
            except Exception:
                continue

        return song_infos

    @classmethod
    async def _search(cls, artist: str, song_name: str) -> str:
        youtube_search_url = cls.search_url.format(artist, song_name)
        page = requests.get(youtube_search_url).text
        return page

    @staticmethod
    def add_youtube_infos(contents: List[dict], topk=5) -> List[dict]:
        new_contents = []
        for k, content in enumerate(contents):
            if k == topk:
                break

            try:
                search_page = YoutubeHelper._search(
                    content["artist"], content["song_name"]
                )
                song_infos = YoutubeHelper._parsing(search_page)
                content["youtube_url"] = song_infos["youtube_url"]
                content["youtube_title"] = song_infos["youtube_title"]

                new_contents.append(content)
            except:
                continue

        return new_contents

import re
import requests

from typing import List, Tuple

APP_MENTION_KEY = "<@U02V2GG4GF9>"

YOUTUBE_SEARCH_URL = "https://www.youtube.com/results?search_query={}+-+{}"
YOUTUBE_WATCH_URL = "https://www.youtube.com/watch?v={}"


def request_youtube_search(artist: str, song_name: str) -> str:
    youtube_search_url = YOUTUBE_SEARCH_URL.format(artist, song_name)
    page = requests.get(youtube_search_url).text
    return page


def parse_urls_from_page(page: str) -> List[str]:
    pattern = r'"videoIds":\["(.+?)"\]'
    watch_keys = list(dict.fromkeys(re.findall(pattern, page)))
    watch_urls = list(map(lambda key: YOUTUBE_WATCH_URL.format(key), watch_keys))
    return watch_urls


def extract_user_input(body: dict) -> str:
    user_input = body.get("event").get("text")
    user_input = user_input.replace(APP_MENTION_KEY, "")  # delete app mention
    user_input = user_input.strip()  # strip
    return user_input


def request_song_info(user_input: str) -> Tuple[str, str]:
    artist, song_name = user_input.split(",")
    artist, song_name = artist.strip(), song_name.strip()
    return artist, song_name

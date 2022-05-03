from typing import List


def youtube_rogo_with_title(watch_url: str, song_title: str, accuracy: float) -> dict:
    return {
        "type": "context",
        "elements": [
            {
                "type": "image",
                "image_url": "https://i.imgur.com/GZk6fXf.png",
                "alt_text": "youtube up logo removebg",
            },
            {
                "type": "mrkdwn",
                "text": f"{accuracy*100:.1f}% <{watch_url}|{song_title}>",
            },
        ],
    }


def youtube_recommendations(contents: List[dict]) -> List[dict]:
    return [
        youtube_rogo_with_title(
            content["watch_url"], content["title"], 1 - (0.02 * (i + 1))
        )
        for i, content in enumerate(contents)
    ]

from typing import List


def static_multiple_select(
    text: str, placeholder: str, action_id: str, song_infos: List[dict]
) -> dict:
    return {
        "type": "section",
        "text": {"type": "mrkdwn", "text": text},
        "accessory": {
            "type": "static_select",
            "placeholder": {
                "type": "plain_text",
                "text": placeholder,
                "emoji": True,
            },
            "options": [  # max options: 100
                {
                    "text": {
                        "type": "plain_text",
                        "text": song_info["title"][:30],
                        "emoji": True,
                    },
                    "value": song_info["watch_url"],
                }
                for song_info in song_infos
            ],
            "action_id": action_id,
        },
    }

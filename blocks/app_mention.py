from typing import List


def recommendation_summary(user_emotion: str, accuracy: float) -> dict:
    return {
        "type": "context",
        "elements": [
            {
                "type": "image",
                "image_url": "https://i.imgur.com/0fhCWsN.png",
                "alt_text": "reco-bot",
            },
            {
                "type": "mrkdwn",
                "text": f"(삐릿삐릿) 사용자의 감정은 `{accuracy*100:.1f}%` 확률로 `{user_emotion}`입니다..!",
            },
        ],
    }


def recommendation_element_of_list(
    watch_url: str, song_title: str, similarity: float
) -> dict:
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
                "text": f"{similarity*100:.1f}% <{watch_url}|{song_title}>",
            },
        ],
    }


def recommendation_list_header():
    return {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "... 사용자의 상황과 감정에 유사한 노래를 추천합니다.",
        },
    }


def recommendation_feedback(
    contents: List[dict], action_id="reco_static_select"
) -> dict:
    return {
        "type": "section",
        "text": {"type": "mrkdwn", "text": "맘에 드는 노래가 있으셨습니까?"},
        "accessory": {
            "type": "static_select",
            "placeholder": {
                "type": "plain_text",
                "text": "곡 선택",
                "emoji": True,
            },
            "options": [  # max options: 100
                {
                    "text": {
                        "type": "plain_text",
                        "text": content["youtube_title"],
                        "emoji": True,
                    },
                    "value": content["youtube_url"],
                }
                for content in contents
            ],
            "action_id": action_id,
        },
    }


BUTTONS = {
    "type": "actions",
    "elements": [
        {
            "type": "button",
            "text": {"type": "plain_text", "emoji": True, "text": "좋아요"},
            "style": "primary",
            "value": "click_me_123",
            "action_id": "like",
        },
        {
            "type": "button",
            "text": {"type": "plain_text", "emoji": True, "text": "싫어요"},
            "style": "danger",
            "value": "click_me_123",
            "action_id": "dislike",
        },
    ],
}

{
    "type": "block_actions",
    "user": {
        "id": "U02E5B0N14K",
        "username": "ggm1207",
        "name": "ggm1207",
        "team_id": "T02DQKA0HM5",
    },
    "api_app_id": "A03005C1ZRT",
    "token": "3Ic4g8Hq1ue0rOO2UuQRb2Nn",
    "container": {
        "type": "message",
        "message_ts": "1648037947.496939",
        "channel_id": "C034R0BSX0E",
        "is_ephemeral": False,
        "thread_ts": "1648037945.465079",
    },
    "trigger_id": "3294912614161.2466656017719.e04940f69faf8bad98bb09837b63deda",
    "team": {"id": "T02DQKA0HM5", "domain": "vumblebot"},
    "enterprise": None,
    "is_enterprise_install": False,
    "channel": {"id": "C034R0BSX0E", "name": "privategroup"},
    "message": {
        "bot_id": "B02VAEV201L",
        "type": "message",
        "text": "text",
        "user": "U02V2GG4GF9",
        "ts": "1648037947.496939",
        "team": "T02DQKA0HM5",
        "blocks": [
            {
                "type": "context",
                "block_id": "2N2i",
                "elements": [
                    {
                        "type": "image",
                        "image_url": "https://i.imgur.com/0fhCWsN.png",
                        "alt_text": "reco-bot",
                    },
                    {
                        "type": "mrkdwn",
                        "text": "(삐릿삐릿) 사용자의 감정은 `8.2%` 확률로 `슬픔-우울한`입니다..!",
                        "verbatim": False,
                    },
                ],
            },
            {
                "type": "section",
                "block_id": "m46t",
                "text": {
                    "type": "mrkdwn",
                    "text": "... 사용자의 상황과 감정에 유사한 노래를 추천합니다.",
                    "verbatim": False,
                },
            },
            {
                "type": "context",
                "block_id": "3hm",
                "elements": [
                    {
                        "type": "image",
                        "image_url": "https://i.imgur.com/GZk6fXf.png",
                        "alt_text": "youtube up logo removebg",
                    },
                    {
                        "type": "mrkdwn",
                        "text": "23.3% <https://www.youtube.com/watch?v=oC0ZdfAdtpw|[MV] OVAN(오반) _ TWENTY(스무 ...>",
                        "verbatim": False,
                    },
                ],
            },
            {
                "type": "context",
                "block_id": "Zz+go",
                "elements": [
                    {
                        "type": "image",
                        "image_url": "https://i.imgur.com/GZk6fXf.png",
                        "alt_text": "youtube up logo removebg",
                    },
                    {
                        "type": "mrkdwn",
                        "text": "22.0% <https://www.youtube.com/watch?v=xldgKraI4qw|가까이 와요 (FEAT. 케이시)>",
                        "verbatim": False,
                    },
                ],
            },
            {
                "type": "context",
                "block_id": "K=LS7",
                "elements": [
                    {
                        "type": "image",
                        "image_url": "https://i.imgur.com/GZk6fXf.png",
                        "alt_text": "youtube up logo removebg",
                    },
                    {
                        "type": "mrkdwn",
                        "text": "20.5% <https://www.youtube.com/watch?v=w1yCFNDVfwc|[MV] GIRIBOY(기리보이) _ You  ...>",
                        "verbatim": False,
                    },
                ],
            },
            {
                "type": "context",
                "block_id": "=RtT6",
                "elements": [
                    {
                        "type": "image",
                        "image_url": "https://i.imgur.com/GZk6fXf.png",
                        "alt_text": "youtube up logo removebg",
                    },
                    {
                        "type": "mrkdwn",
                        "text": "13.5% <https://www.youtube.com/watch?v=s0CWbIv-mQY|날씨가 미쳤어>",
                        "verbatim": False,
                    },
                ],
            },
            {
                "type": "context",
                "block_id": "sHNnV",
                "elements": [
                    {
                        "type": "image",
                        "image_url": "https://i.imgur.com/GZk6fXf.png",
                        "alt_text": "youtube up logo removebg",
                    },
                    {
                        "type": "mrkdwn",
                        "text": "12.0% <https://www.youtube.com/watch?v=Wv3QlRVB6xQ|[MV] ANTS(앤츠) _ Don't Fig ...>",
                        "verbatim": False,
                    },
                ],
            },
            {"type": "divider", "block_id": "aPlB"},
            {
                "type": "section",
                "block_id": "jSI",
                "text": {
                    "type": "mrkdwn",
                    "text": "맘에 드는 노래가 있으셨습니까?",
                    "verbatim": False,
                },
                "accessory": {
                    "type": "static_select",
                    "action_id": "reco_static_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "곡 선택",
                        "emoji": True,
                    },
                    "options": [
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "[MV] OVAN(오반) _ TWENTY(스무 ...",
                                "emoji": True,
                            },
                            "value": "https://www.youtube.com/watch?v=oC0ZdfAdtpw",
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "가까이 와요 (FEAT. 케이시)",
                                "emoji": True,
                            },
                            "value": "https://www.youtube.com/watch?v=xldgKraI4qw",
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "[MV] GIRIBOY(기리보이) _ You  ...",
                                "emoji": True,
                            },
                            "value": "https://www.youtube.com/watch?v=w1yCFNDVfwc",
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "날씨가 미쳤어",
                                "emoji": True,
                            },
                            "value": "https://www.youtube.com/watch?v=s0CWbIv-mQY",
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "[MV] ANTS(앤츠) _ Don't Fig ...",
                                "emoji": True,
                            },
                            "value": "https://www.youtube.com/watch?v=Wv3QlRVB6xQ",
                        },
                    ],
                },
            },
            {
                "type": "actions",
                "block_id": "VMx=k",
                "elements": [
                    {
                        "type": "button",
                        "action_id": "like",
                        "text": {"type": "plain_text", "text": "좋아요", "emoji": True},
                        "style": "primary",
                        "value": "click_me_123",
                    },
                    {
                        "type": "button",
                        "action_id": "dislike",
                        "text": {"type": "plain_text", "text": "싫어요", "emoji": True},
                        "style": "danger",
                        "value": "click_me_123",
                    },
                ],
            },
        ],
        "thread_ts": "1648037945.465079",
        "parent_user_id": "U02E5B0N14K",
    },
    "state": {
        "values": {
            "jSI": {
                "reco_static_select": {
                    "type": "static_select",
                    "selected_option": {
                        "text": {
                            "type": "plain_text",
                            "text": "[MV] OVAN(오반) _ TWENTY(스무 ...",
                            "emoji": True,
                        },
                        "value": "https://www.youtube.com/watch?v=oC0ZdfAdtpw",
                    },
                }
            }
        }
    },
    "response_url": "https://hooks.slack.com/actions/T02DQKA0HM5/3275645490134/p79h44rYHtwSVChpN7EVAsz7",
    "actions": [
        {
            "action_id": "like",
            "block_id": "VMx=k",
            "text": {"type": "plain_text", "text": "좋아요", "emoji": True},
            "value": "click_me_123",
            "style": "primary",
            "type": "button",
            "action_ts": "1648038098.945026",
        }
    ],
}

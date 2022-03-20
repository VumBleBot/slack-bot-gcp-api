ONBOARDING_HEADER = {
    "type": "header",
    "text": {"type": "plain_text", "text": "노래추천봇 (Onboarding)", "emoji": True},
}

ONBOARDING_DESCRIPTION = {
    "type": "section",
    "text": {
        "type": "mrkdwn",
        "text": "안녕하세여, 노래추천봇입니다~ :smile: \n\n 노래추천봇은 사용자의 짧은 발화에서 `상황(Context)`과 `감정(Emotion)`을 분석하여 노래를 추천하는 슬랙봇입니다...! 사용법은 아래와 같습니다 :)",
    },
    "accessory": {
        "type": "image",
        "image_url": "https://i.imgur.com/0fhCWsN.png",
        "alt_text": "reco-bot",
    },
}

ONBOARDING_DETAIL_DESCRIPTION = {
    "type": "section",
    "text": {
        "type": "mrkdwn",
        "text": ":one: `@노래추천봇`을 멘션합니다.\n\n:two: 감정이 드러나는 짧은 문장을 작성합니다. ``` @노래추천봇 이번에 팀장님이 간단한 조사 업무를 부탁했는데 내가 잘못 처리했어.. 상황이 왜 이렇게 꼬이는지.. 너무 힘들당.```\n:three: 추천 받은 노래를 듣습니다. :notes:\n\n :four: (옵션) 좋았던 노래 또는 싫었던 노래를 선택한 후 버튼을 클릭합니다.",
    },
}

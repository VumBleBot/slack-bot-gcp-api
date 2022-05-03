import re
from typing import List

import blocks


def del_paren(text: str):
    return " ".join(re.sub(r"\([^)]*\)", "", text).split())


class BlockTemplates:
    @staticmethod
    def app_mention(user_emotion: str, accuracy: float, contents: List[dict]):
        template = [
            blocks.app_mention.recommendation_summary(user_emotion, accuracy),
            blocks.app_mention.recommendation_list_header(),
            *[
                blocks.app_mention.recommendation_element_of_list(
                    content["youtube_url"],
                    del_paren(f"{content['artist']} - {content['song_name']}")[:50],
                    content["score"],  # score don't used
                    idx + 1,  # idx don't used
                )
                for idx, content in enumerate(contents)
            ],
            blocks.DIVIDER,
            blocks.app_mention.recommendation_feedback(contents),
            blocks.app_mention.BUTTONS,
        ]

        return template

    @staticmethod
    def app_home_opened():
        template = dict()
        template["type"] = "home"
        template["callback_id"] = "home_view"
        template["blocks"] = [
            blocks.app_home_opened.WELCOME,
            blocks.app_home_opened.VUMBLEBOT_DESCRIPTION,
            blocks.DIVIDER,
            blocks.app_home_opened.FLAT_ICON_COPYRIGHT,
            blocks.app_home_opened.VUMBLEBOT_DETAIL_DESCRIPTION,
            blocks.app_home_opened.VUMBLEBOT_SOURCE_DESCRIPTION,
        ]
        return template

    @staticmethod
    def onboarding():
        template = [
            blocks.onboarding.ONBOARDING_HEADER,
            blocks.DIVIDER,
            blocks.onboarding.ONBOARDING_DESCRIPTION,
            blocks.onboarding.ONBOARDING_DETAIL_DESCRIPTION,
            blocks.DIVIDER,
        ]
        return template

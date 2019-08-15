from typing import List

from requests import post
from slack import WebClient

from app import settings


def get_client():
    slack_bot_token = settings.SLACK_BOT_TOKEN
    channel = settings.SLACK_CHANNEL
    return Client(token=slack_bot_token, channel=channel)


class Client:
    _client: WebClient

    def __init__(self, token: str, channel: str) -> None:
        self._client = WebClient(token=token)
        self.channel = channel

    def get_channel_participants(self) -> List[str]:
        response = self._client.conversations_members(channel=self.channel)
        return response.data["members"]

    def post_to_channel(self, message: str) -> None:
        self._client.chat_postMessage(channel=self.channel, text=message)

    def post_to_private(self, receiver_id: str, blocks: List, color=False) -> None:
        message = {"blocks": blocks, "as_user": True}

        if color:
            message["blocks"] = None
            message["attachments"] = [{"color": "#E8E8E8", "blocks": blocks}]

        self._client.chat_postMessage(channel=receiver_id, **message)

    def post_to_response_url(
        self, response_url: str, replace=False, text="", blocks=[], color=False
    ) -> None:
        message = {"replace_original": replace, "text": text, "blocks": blocks}

        if color:
            message["blocks"] = None
            message["attachments"] = [{"color": "#E8E8E8", "blocks": blocks}]

        post(response_url, json=message)

    def is_bot(self, user) -> bool:
        response = self._client.users_info(user=user)
        response_user = response.data["user"]
        return response_user["is_bot"]

    def send_invite(self, receiver_id: str, block_id: str) -> None:
        channel_id = (
            self._client.conversations_open(users=receiver_id)
            .data.get("channel")
            .get("id")
        )
        blocks = [
            {"type": "section", "text": {"type": "mrkdwn", "text": "*Coffee Time!*"}},
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": "Are you free to grab a coffee?"},
            },
            {
                "type": "actions",
                "block_id": str(block_id),
                "elements": [
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "I'm down!"},
                        "style": "primary",
                        "value": "APPROVE",
                    },
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "Nah..."},
                        "style": "danger",
                        "value": "DENY",
                    },
                ],
            },
        ]

        self.post_to_private(receiver_id=channel_id, blocks=blocks)

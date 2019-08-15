from typing import List

from requests import post
from slack import WebClient

from app.settings import SLACK

from .models import Member


def get_client():
    slack_bot_token = SLACK.get("BOT_TOKEN")
    channel = SLACK.get("CHANNEL")

    return Client(token=slack_bot_token, channel=channel)


class Client:
    _client: WebClient

    def __init__(self, token: str, channel: str) -> None:
        self._client = WebClient(token=token)
        self.channel = channel

    def assert_channel_member(self, user_id) -> bool:
        if Member.objects.filter(user_id=user_id, status=Member.STATUS_ACTIVE).exists():
            return True

        conversation = self._client.conversations_info(channel=self.channel)
        channel = conversation.data["channel"]["name"]
        self.post_to_private(
            receiver_id=user_id,
            blocks=[
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"Join #{channel} to start meeting some :coffee: buddies!",
                    },
                }
            ],
        )
        return False

    def post_to_channel(self, message: str) -> None:
        self._client.chat_postMessage(channel=self.channel, text=message)

    def post_to_private(self, receiver_id, blocks=None, text="", color=False):
        message = {"blocks": blocks, "as_user": True}

        if color:
            message["blocks"] = None
            message["attachments"] = [{"color": "#E8E8E8", "blocks": blocks}]

        return self._client.chat_postMessage(channel=receiver_id, text=text, **message)

    def open_dialog(self, dialog, trigger_id):
        return self._client.dialog_open(dialog=dialog, trigger_id=trigger_id)

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

    def send_invite(self, receiver_id: str, block_id: str) -> dict:
        channel_id = (
            self._client.conversations_open(users=receiver_id)
            .data.get("channel")
            .get("id")
        )
        blocks = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Need a little stretch? :ok_woman: Let's grab a coffee?",
                },
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

        return self.post_to_private(receiver_id=channel_id, color=True, blocks=blocks)

    def update(self, channel: str, ts: str, blocks=None, text="", color=False) -> dict:
        message = {"blocks": blocks, "as_user": True}

        if color:
            message["blocks"] = None
            message["attachments"] = [{"color": "#E8E8E8", "blocks": blocks}]

        return self._client.chat_update(channel=channel, ts=ts, text=text, **message)

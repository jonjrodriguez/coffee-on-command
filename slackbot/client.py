from typing import List

from slack import WebClient


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

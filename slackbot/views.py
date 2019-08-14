from app import settings

from rest_framework.views import APIView
from rest_framework.response import Response

from .client import Client


class IndexView(APIView):
    def __init__(self) -> None:
        slack_bot_token = settings.SLACK_BOT_TOKEN
        channel = settings.SLACK_CHANNEL

        self.client = Client(slack_bot_token, channel)

    def get(self, request):
        members = self.client.get_channel_participants()

        return Response(members)

    def post(self, request):
        self.client.post_to_channel("Hi from localhost")

        return Response("Hello, Coffee Buddy!")

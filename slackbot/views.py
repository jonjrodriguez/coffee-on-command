from app import settings

from rest_framework.views import APIView
from rest_framework.response import Response

from match import create_coffee_request
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
        user_id = request.POST.get("user_id")
        response_url = request.POST.get("response_url")

        create_coffee_request(user_id=user_id, response_url=response_url)

        return Response("Hi, we are looking for a coffee buddy for you!")

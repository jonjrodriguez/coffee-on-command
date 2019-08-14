import random

from app import settings

from rest_framework.views import APIView
from rest_framework.response import Response

from slackbot.models import CoffeeRequest
from .client import Client


class IndexView(APIView):
    def __init__(self) -> None:
        slack_bot_token = settings.SLACK_BOT_TOKEN
        channel = settings.SLACK_CHANNEL

        self.client = Client(slack_bot_token, channel)

    def get(self, request):
        members = self.client.get_channel_participants()

        return Response(members)

    def find_a_match(self):
        members = self.client.get_channel_participants()
        member = random.choice(members)

        return member

    def create_coffee_request(self, request):
        user_id = request.POST.get("user_id")
        response_url = request.POST.get("response_url")
        CoffeeRequest.objects.create(user_id=user_id, response_url=response_url)

    def post(self, request):
        self.create_coffee_request(request)
        member = self.find_a_match()

        return Response("Hi, we are looking for a coffee buddy for you!")

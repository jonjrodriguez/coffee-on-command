import json

from app import settings

from rest_framework.views import APIView
from rest_framework.response import Response

from .match import create_coffee_request, accept_match, deny_match
from .models import CoffeeRequest
from .tasks import process_new_request
from .client import Client
from .serializers import Payload


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

        process_new_request.delay(user_id=user_id, response_url=response_url)

        return Response("Hi, we are looking for a coffee buddy for you!")


class ResponseView(APIView):
    def post(self, request):
        data = json.loads(request.data.get("payload"))
        payload = Payload(data=data)
        payload.is_valid()

        user = payload.data.get("user").get("id")
        response_url = payload.data.get("response_url")
        action = payload.data.get("actions")[0]
        block_id = action.get("block_id")

        if action.get("value") == "APPROVE":
            accept_match(user, block_id, response_url)
            return Response("Go get coffee")

        deny_match(user, block_id, response_url)
        return Response("Maybe next time")

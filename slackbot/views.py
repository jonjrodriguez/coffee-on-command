import json

from app.settings import SLACK_BOT_TOKEN, SLACK_CHANNEL

from rest_framework.views import APIView
from rest_framework.response import Response

from .match import create_coffee_request, accept_match, deny_match, find_a_match, on_match_success
from .models import CoffeeRequest
from .tasks import process_new_request
from .client import Client
from .serializers import Payload


class IndexView(APIView):
    def __init__(self) -> None:
        self.client = Client(SLACK_BOT_TOKEN, SLACK_CHANNEL)

    def get(self, request):
        members = self.client.get_channel_participants()

        return Response(members)

    def post(self, request):
        user_id = request.POST.get("user_id")
        response_url = request.POST.get("response_url")

        match = process_new_request.delay(user_id=user_id, response_url=response_url)
        self.client.send_invite(receiver_id=match.user_id, block_id=match.block_id)

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
